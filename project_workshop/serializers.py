from rest_framework import serializers
from .models import Proyecto_Workshop

class ProyectoWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto_Workshop
        fields = '__all__'