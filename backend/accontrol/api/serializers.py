from rest_framework import serializers
from api.models import Sensors

class SensorsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Sensors
        fields = ["s1", "t1", "h1", "s2", "t2", "h2", "created_at"]


        

