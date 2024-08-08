from rest_framework import serializers
from .models import Departamento_Alquiler


class DepartamentoAlquilerSerializer (serializers.ModelSerializer):
    class Meta:
        model = Departamento_Alquiler
        fields = '__all__'        
