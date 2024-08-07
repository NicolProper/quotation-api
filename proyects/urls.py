

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
    path('upload_data/', views.upload_data_excel, name="proyectos_upload"),
    path('get_all_projects/', views.get_all_projects, name="get_all_projects"),
    
    path('get_all_projects_slugs/', views.get_all_projects_slugs, name="get_all_projects_slugs"),
    path('get_all_projects_slugs/', views.get_all_projects_slugs, name="get_all_projects_slugs"),
    path('active_project/<str:slug>/', views.active_project, name="active_project"),
    path('desactive_project/<str:slug>/', views.desactive_project, name="desactive_project"),
    path('get_project_by_name/<str:nombre>/', views.get_project_by_name, name="get_project_by_name"),
    path('create-update/', views.upload_data_project, name="create-update"),
    path('get_all_proyects_web/', views.get_all_proyects_web, name="get_all_proyects_web"),
    path('get_all_proyects_web/', views.get_all_proyects_web, name="get_all_proyects_web"),
    path('update_info_inmobiliaria_project/<str:slug>/', views.update_info_inmobiliaria_project, name="update_info_inmobiliaria_project"),
    path('get_info_inmobiliaria_project/<str:slug>/', views.get_info_inmobiliaria_project, name="get_info_inmobiliaria_project")
]
