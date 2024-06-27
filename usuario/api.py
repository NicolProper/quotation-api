from rest_framework import viewsets , permissions
from .models import User
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # type: ignore
    serializer_class = UsuarioSerializer 
    permission_classes = [permissions.AllowAny]
    ordering_fields = '__all__'