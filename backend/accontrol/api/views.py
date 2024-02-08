from django.shortcuts import render

from api.serializers import SensorsSerializer
from rest_framework import viewsets, permissions
from api.models import Sensors

from django.http import JsonResponse
from django.views import View


class SensorsViewSet(viewsets.ModelViewSet):
    queryset = Sensors.objects.all()
    serializer_class = SensorsSerializer
    # permission_classes = [permissions.IsAuthenticated]


class LastNRecordView(View):
    def get(self, request, n):

        last_n_records = Sensors.objects.all().order_by('-id')[:n]

        data = [{"id": records.id, "s1": records.s1, "t1": records.t1, "h1": records.h1, "s2": records.s2, "t2": records.t2, "h2": records.h2, "created_at": records.created_at} for records in last_n_records]

        return JsonResponse({"data": data})







