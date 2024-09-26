from rest_framework.views import Response, Request

from .models import Municipal_district, Settlement, Locality
from .serializers import Municipal_district_serializer, Settlement_serializer, Locality_serializer
from services.crud import get_many, get, create, update
from services.redis import redis_wrapper


def get_all_municipal_district(request: Request):
    return Response(get_many(Municipal_district, Municipal_district_serializer, {}))


def create_municipal_district(request: Request):
    return Response(create(Municipal_district_serializer, request.data))


def update_municipal_district(request: Request, id: int):
    return Response(update(Municipal_district, Municipal_district_serializer, request.data, {"id": id}))


@redis_wrapper("all_settlements")
def get_all_settlements_method(request: Request):
    return get_many(Settlement, Settlement_serializer)


def get_all_settlements(request: Request):
    return Response(get_all_settlements_method(request))


def get_settlement_by_distict_id(request: Request, reg_id: int):
    return Response(get_many(Settlement, Settlement_serializer, {"RegID": reg_id}))


def create_settlement(request: Request):
    return Response(create(Settlement_serializer, request.data))


def update_settlement(request: Request, id: int):
    return Response(update(Settlement, Settlement_serializer, request.data, {"id": id}))


@redis_wrapper("all_locality")
def get_all_locality_method(request: Request):
    return get_many(Locality, Locality_serializer)


def get_all_locality(request: Request):
    return Response(get_all_locality_method(request))


def get_locality_by_settlement_id(request: Request, settlement_id: int):
    return Response(get_many(Locality, Locality_serializer, {"MunicID": settlement_id}))


def get_locality_by_district_id(request: Request, district_id: int):
    return Response(get_many(Locality, Locality_serializer, {"RegID": district_id}))


def get_locality_by_id(request: Request, id: int):
    return Response(get(Locality, Locality_serializer, {"id": id}))


def create_locality(request: Request):
    return Response(create(Locality_serializer, request.data))


def update_locality(request: Request, id):
    return Response(update(Locality, Locality_serializer, request.data, {"id": id}))
