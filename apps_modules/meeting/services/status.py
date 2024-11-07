from ..models import Status
from ..serializers import Meeting_status_serializer
from apps.constructor.services.status import Base_status_services


class Meeting_status_services(Base_status_services):
    model = Status
    serializer = Meeting_status_serializer
