from rest_framework.views import Response, Request

from .models import Municipal_district, Settlement, Locality
from .serializers import Municipal_district_serializer, Settlement_serializer, Locality_serializer
from apps.constructor.api.services.crud import get_many


def get_all_municipal_district(request: Request):
    return Response(get_many(Municipal_district, Municipal_district_serializer, {}))


def get_settlement_by_distict_id(request: Request, reg_id: int):
    return Response(get_many(Settlement, Settlement_serializer, {"RegID": reg_id}))


def get_locality_by_settlement_id(request: Request, settlement_id: int):
    return Response(get_many(Locality, Locality_serializer, {"MunicID": settlement_id}))
