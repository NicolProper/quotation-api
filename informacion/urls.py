# from django.urls import path, include
from rest_framework.routers import DefaultRouter

from informacion.views import BancariaViewSet

# from proyects.views import upload_data_excel

router = DefaultRouter()
router.register('api/bancario', BancariaViewSet, basename="bancario")
# router.register('proyectos/upload_data/', upload_data_excel, basename="proyectos_upload")

urlpatterns = router.urls
