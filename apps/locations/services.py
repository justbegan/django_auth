from rest_framework.views import Response, Request
from django.db.models import Q

from .models import Municipal_district, Settlement, Locality
from .serializers import Municipal_district_serializer, Settlement_serializer, Locality_serializer
from services.crud_services import Base_crud
from services.current import get_current_section


class Locallity_services:
    @staticmethod
    def get_all_municipal_district(request: Request):
        params = request.GET.dict()
        return Response(Base_crud.get_many(Municipal_district, Municipal_district_serializer, params))

    @staticmethod
    def create_municipal_district(request: Request):
        return Response(Base_crud.create(Municipal_district_serializer, request.data))

    @staticmethod
    def update_municipal_district(request: Request, id: int):
        return Response(Base_crud.update(Municipal_district, Municipal_district_serializer, request.data, {"id": id}))

    @staticmethod
    def get_all_settlements_method(request: Request):
        params = request.GET.dict()
        return Base_crud.get_many(Settlement, Settlement_serializer, params)

    @staticmethod
    def get_all_settlements(request: Request):
        return Response(Locallity_services.get_all_settlements_method(request))

    @staticmethod
    def get_settlement_by_distict_id(request: Request, reg_id: int):
        return Response(Base_crud.get_many(Settlement, Settlement_serializer, {"RegID": reg_id}))

    @staticmethod
    def create_settlement(request: Request):
        return Response(Base_crud.create(Settlement_serializer, request.data))

    @staticmethod
    def update_settlement(request: Request, id: int):
        return Response(Base_crud.update(Settlement, Settlement_serializer, request.data, {"id": id}))

    @staticmethod
    def get_all_locality_method(request: Request):
        obj = Locality.objects.filter(
            Q(sections__isnull=True) | Q(sections=get_current_section(request))
        ).distinct()
        return Base_crud.get_many(
            model=Locality,
            serializer=Locality_serializer,
            custom_obj=obj
        )

    @staticmethod
    def get_all_locality(request: Request):
        return Response(Locallity_services.get_all_locality_method(request))

    @staticmethod
    def get_locality_by_settlement_id(request: Request, settlement_id: int):
        return Response(Base_crud.get_many(Locality, Locality_serializer, {"MunicID": settlement_id}))

    @staticmethod
    def get_locality_by_district_id(request: Request, district_id: int):
        return Response(Base_crud.get_many(Locality, Locality_serializer, {"RegID": district_id}))

    @staticmethod
    def get_locality_by_id(request: Request, id: int):
        return Response(Base_crud.get(Locality, Locality_serializer, {"id": id}))

    @staticmethod
    def create_locality(request: Request):
        return Response(Base_crud.create(Locality_serializer, request.data))

    @staticmethod
    def update_locality(request: Request, id):
        return Response(Base_crud.update(Locality, Locality_serializer, request.data, {"id": id}))
