from rest_framework import serializers
from .models import Bancaria

class BancariaSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Bancaria
        fields = '__all__'

        