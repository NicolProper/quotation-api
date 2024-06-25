# from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from departments.views import upload_data_excel
from .api import DepartamentoViewSet  # Asegúrate de que esta importación sea correcta

router = DefaultRouter()
router.register('api/departamentos', DepartamentoViewSet, basename="departamentos")
# router.register('departamentos/upload_data/', upload_data_excel, basename="proyectos_upload")


urlpatterns = router.urls
