

from django.urls import path, register_converter
from . import views

class FloatConverter:
    regex = r'\d+(\.\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')
# get_project_by_name
urlpatterns = [
    path('create-update/', views.upload_data_department_rent, name="upload_data_department"),

]
