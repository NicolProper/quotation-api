from rest_framework import viewsets , permissions
from .models import Cotizacion
from .serializers import CotizacionSerializer


class CotizacionViewSet(viewsets.ModelViewSet):
    queryset = Cotizacion.objects.all() # type: ignore
    serializer_class = CotizacionSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'