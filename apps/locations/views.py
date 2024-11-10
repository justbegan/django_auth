from rest_framework.views import APIView, Response, Request
import json
from drf_yasg.utils import swagger_auto_schema

from .models import (Municipal_district, Settlement, Settlement_type, Locality_type, Locality)
from .services import Locallity_services
from services.decorators import Decorators
from .serializers import Municipal_district_serializer, Settlement_serializer, Locality_serializer


class CreateRa(APIView):
    def get(self, request):
        with open('ra.json', 'r', encoding='utf-8-sig') as file:
            ra: list = json.load(file)

        for r in ra:
            obj = {
                "RegionName": r["RegionName"],
                "RegionNameE": r["RegionNameE"],
                "OKTMO": r["OKTMO"],
                "Population": r["Population"],
                "RegOKTMO": r["RegOKTMO"],
                "RegIsNorthern": r["RegIsNorthern"]
            }
            a = Municipal_district.objects.create(**obj)
            a.save()
        return Response(True)


class CreateSettlements(APIView):
    def get(self, request):
        with open('sett.json', 'r', encoding='utf-8-sig') as file:
            ra: list = json.load(file)

        for r in ra:
            obj = {
                "RegID": Municipal_district.objects.get(id=r['RegID'] - 1),
                "MunicTypeID": Settlement_type.objects.get(id=r['MunicTypeID']),
                "MunicName": r["MunicName"],
                "MunicNameE": r["MunicNameE"],
                "Population": r.get("Population", None),
                "OKTMO": r["OKTMO"],
                "OKATO": r["OKATO"],
            }
            a = Settlement.objects.create(**obj)
            a.save()
        return Response(True)


class DeleteLocality(APIView):
    def get(self, request):
        Locality.objects.all().delete()
        return Response(True)


class CreateLocality(APIView):
    def get(self, request):
        with open('loc.json', 'r', encoding='utf-8-sig') as file:
            ra: list = json.load(file)

        for r in ra:
            obj = {
                "MunicID": Settlement.objects.get(id=r["MunicID"]),
                "RegID": Municipal_district.objects.get(id=r['RegID'] - 1),
                "OKTMO": r["OKTMO"],
                "LocName": r["LocName"],
                "LocNameE": r["LocNameE"],
                "LocPopulation": r["LocPopulation"],
                "LocTypeID": Locality_type.objects.get(id=r["LocTypeID"]),
                "Latitude": r["Latitude"],
                "Longitude": r["Longitude"]
            }
            a = Locality.objects.create(**obj)
            a.save()
        return Response(True)


class Municipal_district_main(APIView):
    model_used = Municipal_district

    def get(self, request: Request):
        return Locallity_services.get_all_municipal_district(request)

    @swagger_auto_schema(request_body=Municipal_district_serializer)
    @Decorators.role_required_v2()
    def post(self, request: Request):
        return Locallity_services.create_municipal_district(request)


class Municipal_district_detail(APIView):
    model_used = Municipal_district

    @swagger_auto_schema(request_body=Municipal_district_serializer)
    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return Locallity_services.update_municipal_district(request, id)


class Settlement_main(APIView):
    model_used = Settlement

    def get(self, request: Request):
        return Locallity_services.get_all_settlements(request)

    @swagger_auto_schema(request_body=Settlement_serializer)
    @Decorators.role_required_v2()
    def post(self, request: Request):
        return Locallity_services.create_settlement(request)


class Settlement_detail(APIView):
    model_used = Settlement

    def get(self, request: Request, id: int):
        return Locallity_services.get_settlement_by_distict_id(request, id)

    @swagger_auto_schema(request_body=Settlement_serializer)
    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return Locallity_services.update_settlement(request, id)


class Locality_detail(APIView):
    model_used = Locality
    """
    Описание\n
    получить по id поселения type=1\n
    получить по id района type=2\n
    получить по id type=3
    """
    def get(self, request: Request, id: int):
        request_type = request.GET.get("type")
        if request_type == "1":
            return Locallity_services.get_locality_by_settlement_id(request, id)
        elif request_type == "2":
            return Locallity_services.get_locality_by_district_id(request, id)
        else:
            return Locallity_services.get_locality_by_id(request, id)

    @swagger_auto_schema(request_body=Locality_serializer)
    @Decorators.role_required_v2()
    def put(self, request: Request, id: int):
        return Locallity_services.update_locality(request, id)


class Locality_main(APIView):
    model_used = Locality

    def get(self, request: Request):
        return Locallity_services.get_all_locality(request)

    @swagger_auto_schema(request_body=Locality_serializer)
    @Decorators.role_required_v2()
    def post(self, request: Request):
        return Locallity_services.create_locality(request)
