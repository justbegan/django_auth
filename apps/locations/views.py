from rest_framework.views import APIView, Response, Request
import json

from .models import (Municipal_district, Settlement, Settlement_type, Locality_type, Locality)
from .services import (get_all_municipal_district, get_settlement_by_distict_id, get_locality_by_settlement_id,
                       get_locality_by_district_id, get_locality_by_id)


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
                "LocTypeID": Locality_type.objects.get(id=r["LocTypeID"])
            }
            a = Locality.objects.create(**obj)
            a.save()
        return Response(True)


class Municipal_district_main(APIView):
    def get(self, request: Request):
        return get_all_municipal_district(request)


class Settlement_detail(APIView):
    def get(self, request: Request, reg_id: int):
        return get_settlement_by_distict_id(request, reg_id)


class Locality_detail(APIView):
    """
    Описание\n
    получить по id поселения type=1\n
    получить по id района type=2\n
    получить по id type=3
    """
    def get(self, request: Request, id: int):
        request_type = request.GET.get("type")
        print(request_type)
        if request_type == "1":
            return get_locality_by_settlement_id(request, id)
        elif request_type == "2":
            return get_locality_by_district_id(request, id)
        else:
            return get_locality_by_id(request, id)
