import logging
import os
from functools import wraps

import jsonschema
from bson import ObjectId
from flask import request, jsonify
from jsonschema import Draft7Validator
from pymongo import MongoClient
from werkzeug.exceptions import abort

_db_client = None
logger = logging.getLogger(__name__)


def validate_schema(schema):
    validator = Draft7Validator(schema, format_checker=jsonschema.FormatChecker())

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            input = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(input)]
            if errors:
                response = jsonify(dict(message="invalid input", errors=errors))
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)
        return wrapped
    return wrapper


def env_var(vname, default_val=None):
    if vname not in os.environ:
        msg = f'MongoDB : define {vname} environment variable! defaulting to {default_val}'
        logger.warning(msg)
        return default_val
    else:
        return os.environ[vname]


def get_mongodb_connection():
    global _db_client
    db_name = env_var('GPN_DB_NAME', 'gpn')
    if _db_client is None:
        try:
            host = env_var('GPN_DB_HOST', 'localhost')
            port = env_var('GPN_DB_PORT', 27017)
            _db_client = MongoClient(f'mongodb://{host}:{port}/')
            _db_client.server_info()

        except Exception as err:
            _db_client = None
            msg = f'cannot connect Mongo {err}'
            logger.warning(msg)
            return None

    return _db_client[db_name]


def update_status(id, status: str = 'Collecting', valid_statuses=None, http=True):
    if valid_statuses is None:
        valid_statuses = ['New', 'Collecting']
    audits = get_mongodb_connection()['audits']
    audit = audits.find_one({'_id': ObjectId(id)}, {'status': 1})
    if audit is None:
        if http:
            abort(404, description='Task not found')
        else:
            logger.error('Task not found')
    if audit['status'] in valid_statuses:
        if http:
            json_data = request.json
            json_data['request_path'] = request.path
            update = {'$set': {'status': status}, '$push': {'robot': json_data}}
        else:
            update = {'$set': {'status': status}}
        audits.update_one({'_id': audit['_id']}, update)
    else:
        if http:
            abort(409, description='Invalid task status=' + audit['status'])
        else:
            logger.error('Invalid task status=' + audit['status'])
    return 'ok'
