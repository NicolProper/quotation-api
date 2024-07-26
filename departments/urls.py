
from django.urls import path, register_converter

from departments.images import delete_image_view, upload_image_view
from . import views
class FloatConverter:
    regex = r'\d+(\.\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')

urlpatterns = [
    path('upload_data/', views.upload_data_excel, name="departamentos_upload"),
    path('getAllDepartamentos/', views.getAllDepas, name="departamentos_get_all"),
    path('update_all_data/', views.update_all_data, name="update_all_data"),
    path(
        'info_departamento_proyecto_analyzer/<int:idDepartamento>/<uuid:idCliente>/<float:tasa>/<float:plazoMeses>/<float:porcentajeInicial>/',
        views.info_departamento_proyecto_analyzer,
        name="info_departamento_proyecto"
    ),
    path('get_score_crediticio/', views.get_score_crediticio, name='get_score_crediticio'),
# urlpatterns = [
    path('upload-image/', upload_image_view, name='upload_image'),
    path('delete-image/', delete_image_view, name='delete_image'),
    path('create-update/', views.upload_data_department, name="upload_data_department"),
    
    path('edit/', views.edit_data_department, name="upload_data_department"),
    path('stock/', views.edit_data_stock_department, name="stock"),

    path('info-department-by-nro-depa/<str:nro_depa>/<str:slug>/', views.get_info_department_by_nro_depa, name="get_info_department_by_nro_depa"),

    path('get_nro_depa_departments/<str:slug>/', views.get_nro_depas_by_project, name="get_nro_depas_by_project"),

# ]
]
# get_nro_depas_by_project