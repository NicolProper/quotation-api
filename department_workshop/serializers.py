from rest_framework import serializers

from .models import Departamento_Workshop


class DepartamentoWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento_Workshop
        fields = '__all__'
    