

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
    path('upload_data/', views.upload_data_excel, name="proyectos_upload"),
    path('get_all_proyects_web/', views.get_all_proyects_web, name="get_all_proyects_web"),
]
