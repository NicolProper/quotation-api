from rest_framework import viewsets , permissions

from department_workshop.serializers import DepartamentoWorkshopSerializer
from .models import Departamento_Workshop


class DepartamentoWorkshopViewSet(viewsets.ModelViewSet):
    queryset = Departamento_Workshop.objects.all() # type: ignore
    serializer_class = DepartamentoWorkshopSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'