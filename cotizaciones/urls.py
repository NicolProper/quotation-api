# from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from proyects.views import upload_data_excel
from .api import CotizacionesViewSet  # Asegúrate de que esta importación sea correcta

router = DefaultRouter()
router.register('api/cotizaciones', CotizacionesViewSet, basename="cotizaciones")
# router.register('Cotizacions/upload_data/', upload_data_excel, basename="Cotizacions_upload")

urlpatterns = router.urls
