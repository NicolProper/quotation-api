
from django.urls import path, register_converter
from . import views

class FloatConverter:
    regex = r'\d+(\.\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')

urlpatterns = [

     path('crear_cotizacion/', views.crear_cotizacion, name="crear_cotizacion"),
]
