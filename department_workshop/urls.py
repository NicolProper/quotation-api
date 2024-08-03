
from django.urls import path, register_converter

from department_workshop.images import delete_image_view, upload_image_view

# from department.images import delete_image_view, upload_image_view
from . import views
class FloatConverter:
    regex = r'\d+(\.\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')

urlpatterns = [

    path('create-update/', views.upload_data_department, name="upload_data_department"),
    path('info-department-by-nro-depa/<str:nro_depa>/<int:id>/', views.get_info_department_by_nro_depa, name="get_info_department_by_nro_depa"),
    path('delete_department/<str:nro_depa>/<int:id>/', views.delete_department, name="delete_department"),
    path('get_nro_depas_by_project_workshop/<int:id>/', views.get_nro_depas_by_project_workshop, name="get_nro_depas_by_project"),
    path('upload-image/', upload_image_view, name='upload_image'),
    path('delete-image/', delete_image_view, name='delete_image'),
    path('get_departments_workshop/', views.get_departments_workshop, name="get_departments_workshop")
]
# get_nro_depas_by_project