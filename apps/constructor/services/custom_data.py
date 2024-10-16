from rest_framework.views import Request
from copy import deepcopy
from jsonschema import validate, ValidationError, draft7_format_checker

from ..services.current import get_current_schema
from .current import get_current_new_status
from ..models import Status


class CustomDataValidationError(Exception):
    pass


class SchemaNotFoundError(Exception):
    pass


def validate_custom_data(request: Request):
    data = deepcopy(request.data)
    status = data.get("status", None)
    if status is None:
        raise CustomDataValidationError({"status": "Статус обязатен к заполнению."})
    required = status != get_current_new_status(Status, request).id
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
        validate(instance=obj, schema=schema, format_checker=draft7_format_checker)
    except ValidationError as e:
        raise CustomDataValidationError({"custom_data": str(e)})

    return obj
