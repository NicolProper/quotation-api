# from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from proyects.views import upload_data_excel
from .api import UsuarioViewSet  # Asegúrate de que esta importación sea correcta

router = DefaultRouter()
router.register('api/usuario', UsuarioViewSet, basename="usuario")
# router.register('proyectos/upload_data/', upload_data_excel, basename="proyectos_upload")

urlpatterns = router.urls
