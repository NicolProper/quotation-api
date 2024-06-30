from rest_framework import serializers
from .models import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'edad': {'required': False},
            'residencia': {'required': False},
            'primera_vivienda': {'required': False},
            'ingreso_primera_categoria': {'required': False},
            'ingreso_segunda_categoria': {'required': False},
            'ingreso_tercera_categoria': {'required': False},
            'ingreso_cuarta_categoria': {'required': False},
            'ingreso_quinta_categoria': {'required': False},
            'cuota_vehicular': {'required': False},
            'cuota_personal': {'required': False},
            'cuota_tarjeta_credito': {'required': False},
            'cuota_inicial': {'required': False},
            'cuota_hipotecaria': {'required': False},
        }