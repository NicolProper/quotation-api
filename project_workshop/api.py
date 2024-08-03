from rest_framework import viewsets , permissions
from .models import Proyecto_Workshop

from .serializers import ProyectoWorkshopSerializer


class ProyectoWorkshopViewSet(viewsets.ModelViewSet):
    queryset = Proyecto_Workshop.objects.all() # type: ignore
    serializer_class = ProyectoWorkshopSerializer 
    permission_classes = [permissions.AllowAny]
    
    ordering_fields = '__all__'