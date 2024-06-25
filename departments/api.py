from rest_framework import viewsets , permissions
from .models import Departamento
from .serializers import DepartamentoSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all() # type: ignore
    serializer_class = DepartamentoSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'