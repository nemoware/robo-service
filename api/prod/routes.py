import datetime
import json
import logging
import os

import bson
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from api import doc_loader, schemas
from api.common import validate_schema, get_mongodb_connection, env_var, update_status
from api.doc_loader import load_docs

api = Blueprint('prod', __name__)
logger = logging.getLogger(__name__)


def json_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    # else:
    #     raise TypeError(x)


@api.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@api.errorhandler(409)
def conflict(e):
    return jsonify(error=str(e)), 409


@api.errorhandler(501)
def not_iplemented(e):
    return jsonify(error=str(e)), 501


@api.route('/robot/new_tasks', methods=['GET'])
def new_tasks():
    logger.info('/robot/new_tasks')
    db = get_mongodb_connection()
    tasks = list(db['audits'].aggregate([{'$match': {'status': 'New'}},
                                         {'$project': {'_id': 0, 'id': '$_id',
                                                       'task_start': '$auditStart',
                                                       'task_end': '$auditEnd',
                                                       'subsidiary': '$subsidiary.name',
                                                       'inspector_name': '$author.name',
                                                       'inspector_email': '$author.userPrincipalName'}}]))
    response_json = {
        "tasks": tasks,
        "message": "ok"
    }
    return json.dumps(response_json, default=json_handler, ensure_ascii=False)


@api.route('/robot/curator_request', methods=['POST'])
@validate_schema(schemas.input_curator_request)
def curator_request():
    logger.info('/robot/curator_request')
    return jsonify(dict(message=update_status(request.json['id'])))


@api.route('/robot/confirmed', methods=['POST'])
@validate_schema(schemas.input_confirmed)
def confirmed():
    logger.info('/robot/confirmed')
    return jsonify(dict(message=update_status(request.json['id'])))


@api.route('/robot/manual_register_status', methods=['POST'])
@validate_schema(schemas.input_manual_register_status)
def manual_register_status():
    logger.info('/robot/manual_register_status')
    return jsonify(dict(message=update_status(request.json['id'])))


@api.route('/robot/register_status', methods=['POST'])
@validate_schema(schemas.input_register_status)
def register_status():
    logger.info('/robot/register_status')
    return jsonify(dict(message=update_status(request.json['id'])))


@api.route('/robot/registers_mapping', methods=['POST'])
@validate_schema(schemas.input_registers_mapping)
def register_mapping():
    logger.info('/robot/registers_mapping')
    return jsonify(dict(message=update_status(request.json['id'])))


@api.route('/robot/recognition', methods=['POST'])
@validate_schema(schemas.input_recognition)
def recognition():
    logger.info('/robot/recognition')
    if request.json['audit_start']:
        resp = update_status(request.json['id'], status='Loading')
        if os.path.isabs(request.json['directory_path']):
            root = request.json['directory_path']
        else:
            root = os.path.join(env_var('GPN_DOC_ROOT'), request.json['directory_path'])
        doc_loader.pool.apply_async(load_docs, (request.json['id'], root))
    else:
        resp = update_status(request.json['id'])
    return jsonify(dict(message=resp))


@api.route('/robot/active_tasks', methods=['GET'])
def active_tasks():
    logger.info('/robot/new_tasks')
    db = get_mongodb_connection()
    tasks = list(db['audits'].aggregate([{'$match': {'status': {'$ne': 'Approved'}}},
                                         {'$project': {'_id': 0, 'id': '$_id', 'status': 1}}]))
    response_json = {
        "active_tasks": tasks,
        "message": "ok"
    }
    return json.dumps(response_json, default=json_handler, ensure_ascii=False)


@api.route('/robot/reanalysis', methods=['POST'])
@validate_schema(schemas.input_reanalysis)
def reanalysis():
    abort(501, "Not implemented")
