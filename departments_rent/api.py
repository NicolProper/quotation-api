from rest_framework import viewsets , permissions
from .models import Departamento_Alquiler
from .serializers import DepartamentoAlquilerSerializer


class DepartamentoAlquilerViewSet(viewsets.ModelViewSet):
    queryset = Departamento_Alquiler.objects.all() # type: ignore
    serializer_class = DepartamentoAlquilerSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'