from rest_framework import viewsets , permissions
from .models import Proyectos
from .serializers import CotizacionesSerializer


class CotizacionesViewSet(viewsets.ModelViewSet):
    queryset = Proyectos.objects.all() # type: ignore
    serializer_class = CotizacionesSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'