from rest_framework.routers import DefaultRouter
from api.views import SensorsViewSet, LastNRecordView

from django.urls import path


app_name = "api"
router = DefaultRouter(trailing_slash=False)
# router.register(r'sensors', SensorsViewSet)

urlpatterns = [path("sensors/last_n/<int:n>", LastNRecordView.as_view(), name="last_n_records")]
