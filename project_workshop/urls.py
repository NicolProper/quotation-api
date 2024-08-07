

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
    path('active-project/', views.active_project, name="proyectos_upload"),
    path('get_all_projects/', views.get_all_projects, name="get_all_projects"),
    path('create-update/', views.upload_data_proyecto, name="create-update"),
    path('get_all_proyects_name_id/', views.get_all_projects_name_id, name="get_all_projects_name_id"),
    path('get_info_project/<int:id>/', views.get_info_project, name="get_info_project"),
    path('update_info_project/<int:id>/', views.update_info_project, name="update_info_project"),
    path('get_all_projects_workshop/', views.get_all_projects_workshop, name="get_all_projects_workshop"),
    path('active_project/<str:nombre>/', views.active_project, name="active_project"),
    path('desactive_project/<str:nombre>/', views.desactive_project, name="desactive_project"),
]
