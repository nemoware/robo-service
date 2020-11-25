input_confirmed = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 24, "maxLength": 24},
        "confirmation_date": {"type": "string", "format": "date-time"},
        "confirmed": {"type": "boolean"}
    },
    "required": ["id", "confirmation_date", "confirmed"]
}

input_curator_request = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 24, "maxLength": 24},
        "sending_date": {"type": "string", "format": "date-time"},
        "request_sent": {"type": "boolean"}
    },
    "required": ["id", "sending_date", "request_sent"]
}

input_manual_register_status = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 24, "maxLength": 24},
        "register_date": {"type": "string", "format": "date-time"},
        "request_provided": {"type": "boolean"}
    },
    "required": ["id", "register_date", "request_provided"]
}

input_register_status = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 24, "maxLength": 24},
        "register_date": {"type": "string", "format": "date-time"},
        "documents_collected": {"type": "boolean"}
    },
    "required": ["id", "register_date", "documents_collected"]
}

input_registers_mapping = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 24, "maxLength": 24},
        "all_data_collected": {"type": "boolean"},
        "lack_of_data": {"type": "integer", "minimum": 0},
        "new_deadline": {"type": "string", "format": "date-time"},
        "extra_data": {"type": "boolean"},
        "recognition_started": {"type": "boolean"}
    },
    "required": ["id", "all_data_collected", "lack_of_data", "new_deadline", "extra_data", "recognition_started"]
}

input_recognition = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 24, "maxLength": 24},
        "all_data_recognized": {"type": "boolean"},
        "lack_of_data": {"type": "integer", "minimum": 0},
        "new_deadline": {"type": "string", "format": "date-time"},
        "audit_start": {"type": "boolean"},
        "directory_path": {"type": "string"},
        "warnings": {"type": "array"},
        "errors": {"type": "array"}
    },
    "required": ["id", "all_data_recognized", "lack_of_data", "new_deadline", "audit_start", "directory_path"]
}