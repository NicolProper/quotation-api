from rest_framework import viewsets , permissions
from .models import Proyecto

from .serializers import ProyectoSerializer


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all() # type: ignore
    serializer_class = ProyectoSerializer 
    permission_classes = [permissions.AllowAny]
    
    ordering_fields = '__all__'