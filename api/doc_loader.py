import base64
import json
import os

import requests
from bson import ObjectId

from common import get_mongodb_connection, env_var, logger, update_status

pool = None


def save_doc(task_id, document, filename, parser_response_code, parser_version, parent_doc_id=None) -> ObjectId:
    if document.get('version') is None:
        document['version'] = parser_version
    audit_id = ObjectId(task_id)
    db = get_mongodb_connection()
    insert = {'filename': filename, 'parse': document, 'parserResponseCode': parser_response_code, 'documentType': document['documentType']}
    if document['documentType'] != 'CHARTER':
        insert['auditId'] = audit_id
    insert_result = db['documents'].insert_one(insert)

    if document['documentType'] == 'CHARTER':
        db['audits'].update_one({"_id": audit_id},
                                    {"$push": {"charters": insert_result.inserted_id}})

    if document['documentType'] == 'ANNEX':
        db['audits'].update_one({"_id": audit_id},
                                    {"$push": {"links": {"fromId": insert_result.inserted_id, "toId": parent_doc_id, "type": "parser"}}})
    logger.info(f'Document {filename} successfully loaded.')
    return insert_result.inserted_id


def load_docs(audit_id, root: str):
    try:
        paths = []
        for directory, _, files in os.walk(root):
            for file in files:
                paths.append(os.path.join(directory, file))
        parser_url = env_var('GPN_PARSER_URL') + '/document-parser'
        headers = {'Content-Type': 'application/json'}
        for path in paths:
            with open(path, "rb") as doc_file:
                encoded_string = base64.b64encode(doc_file.read()).decode('ascii')
            _, file_extension = os.path.splitext(path)
            data = {'base64Content': encoded_string, 'documentFileType': file_extension[1:].upper()}
            relative_path = os.path.relpath(path, root)
            response = requests.post(parser_url, headers=headers, data=json.dumps(data))
            response_json = response.json()
            contract_id = None
            for document in response_json['documents']:
                if document['documentType'] == 'ANNEX':
                    save_doc(audit_id, document, relative_path, response.status_code, response_json['version'], contract_id)
                else:
                    inserted_id = save_doc(audit_id, document, relative_path, response.status_code, response_json['version'])
                    if document['documentType'] == 'CONTRACT':
                        contract_id = inserted_id
        update_status(audit_id, 'InWork', ['Loading'], http=False)
    except Exception as e:
        logger.exception(e)
        update_status(audit_id, 'LoadingFailed', ['Loading'], http=False)


