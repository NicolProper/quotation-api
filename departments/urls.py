
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
    path('upload_data/', views.upload_data_excel, name="departamentos_upload"),
    path('getAllDepartamentos/', views.getAllDepas, name="departamentos_get_all"),
    path('update_all_data/', views.update_all_data, name="update_all_data"),
    path(
        'info_departamento_proyecto_analyzer/<int:idDepartamento>/<uuid:idCliente>/<float:tasa>/<float:plazoMeses>/<float:porcentajeInicial>/',
        views.info_departamento_proyecto_analyzer,
        name="info_departamento_proyecto"
    ),
    path('get_score_crediticio/', views.get_score_crediticio, name='get_score_crediticio'),
]
