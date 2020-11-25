import jsonschema as jsonschema
from flask import request, jsonify, Blueprint

from api import schemas
from api.common import validate_schema

api = Blueprint('stub', __name__)


@api.route('/robot/new_tasks', methods=['GET'])
def new_tasks():
    response_json = {
        "tasks": [
            {"id": "5fbbe464a2b4551c06107ab8",
             "task_start": "2018-12-31T00:00:00Z",
             "task_end": "2020-11-22T00:00:00Z",
             "subsidiary": "Арктика Медиа",
             "inspector_name": "Иванов Иван Иванович",
             "inspector_email": "example@gazprom-neft.ru"
             },
            {"id": "5fb278bed8c9df1ed1236d28",
             "task_start": "2017-12-31T00:00:00Z",
             "task_end": "2020-11-15T00:00:00Z",
             "subsidiary": "Газпромнефть НТЦ",
             "inspector_name": "Петров Петр Петрович",
             "inspector_email": "example2@gazprom-neft.ru"
             }
        ],
        "message": "ok"
    }
    return response_json


@api.route('/robot/curator_request', methods=['POST'])
@validate_schema(schemas.input_curator_request)
def curator_request():
    return jsonify(dict(message='ok'))


@api.route('/robot/confirmed', methods=['POST'])
@validate_schema(schemas.input_confirmed)
def confirmed():
    return jsonify(dict(message='ok'))


@api.route('/robot/manual_register_status', methods=['POST'])
@validate_schema(schemas.input_manual_register_status)
def manual_register_status():
    return jsonify(dict(message='ok'))


@api.route('/robot/register_status', methods=['POST'])
@validate_schema(schemas.input_register_status)
def register_status():
    return jsonify(dict(message='ok'))


@api.route('/robot/registers_mapping', methods=['POST'])
@validate_schema(schemas.input_registers_mapping)
def register_mapping():
    return jsonify(dict(message='ok'))


@api.route('/robot/recognition', methods=['POST'])
@validate_schema(schemas.input_recognition)
def recognition():
    return jsonify(dict(message='ok'))


@api.route('/robot/active_tasks', methods=['GET'])
def active_tasks():
    response_json = {
        "active_tasks": [
            {
                "id": "5fb278bed8c9df1ed1236d28",
                "status": "Done"
            },
            {
                "id": "5fb278bed8c9df1ed1236d57",
                "status": "InWork"
            }
        ],
        "message": "ok"
    }
    return response_json
