from rest_framework import viewsets , permissions
from .serializers import BancariaSerializer
from .models import Bancaria


class BancariaSerializerViewSet(viewsets.ModelViewSet):
    queryset = Bancaria.objects.all() # type: ignore
    serializer_class = BancariaSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'