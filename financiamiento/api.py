from rest_framework import viewsets , permissions
from .models import Cliente
from .serializers import FinanciamientoSerializer


class FinanciamientoViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all() # type: ignore
    serializer_class = FinanciamientoSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'