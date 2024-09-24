from rest_framework.views import Request
from copy import deepcopy
from jsonschema import validate, ValidationError

from ..services.current import get_current_schema
from .current import get_current_new_status


class CustomDataValidationError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


def validate_custom_data(request: Request):
    data = deepcopy(request.data)
    status = data.get("status")
    required = status != get_current_new_status(request)

    custom_data = data.get("custom_data")
    if not isinstance(custom_data, dict):
        raise CustomDataValidationError({"custom_data": f"Ожидалось dict, получено {type(custom_data).__name__}."})
    schema = get_current_schema(request)
    if not schema:
        raise SchemaNotFoundError({"schema": "Schema could not be found."})

    schema = deepcopy(schema)
    if not required:
        schema['required'] = []

    obj = {
        key: value for key, value in custom_data.items()
        if key in schema.get("properties", {}) and value != ''
    }

    try:
        validate(instance=obj, schema=schema)
    except ValidationError as e:
        raise CustomDataValidationError({"custom_data": str(e)})

    return obj
