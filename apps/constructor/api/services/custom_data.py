from rest_framework.views import Request
from jsonschema import validate
from rest_framework.exceptions import ValidationError

from ..services.current import get_current_schema


def validate_custom_data(request: Request):
    custom_data = request.data.get("custom_data")

    if custom_data is None:
        raise Exception({"custom_data": "This field is required."})

    try:
        schema = get_current_schema(request)
        if schema is None:
            raise Exception({"schema": "Schema could not be found."})

        data = {
            key: value for key, value in custom_data.items()
            if key in schema.get("properties", {}) and value != ''
        }
        validate(instance=data, schema=schema)
        return data
    except ValidationError as e:
        raise Exception({"custom_data": str(e)})
    except Exception as e:
        raise Exception({"error": str(e)})
