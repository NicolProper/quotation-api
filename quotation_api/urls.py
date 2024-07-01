from django.contrib import admin
from django.urls import include, path, register_converter
from departments import views as departamentos_views
from proyects import views as proyectos_views
from proyects.views import get_all_proyects_web
from usuario.views import  actualizar_usuario_view, buscar_usuario_por_dni, crear_usuario_view, send_email_with_attachments

# Definir el convertidor de float
class FloatConverter:
    regex = r'\d+(\.\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

# Registrar el convertidor de float
register_converter(FloatConverter, 'float')

# Definir las URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('proyectos/upload_data/', proyectos_views.upload_data_excel, name="proyectos_upload"),
    path('proyectos/get_all_proyects_web/', get_all_proyects_web, name="get_all_proyects_web"),
    path('departamentos/upload_data/', departamentos_views.upload_data_excel, name="departamentos_upload"),
    path('departamentos/getAllDepartamentos/', departamentos_views.getAllDepas, name="departamentos_upload"),

    path('departamentos/update_all_data/', departamentos_views.update_all_data, name="update_all_data"),
    path('departamentos/info_departamento_proyecto_analyzer/<int:idDepartamento>/<uuid:idCliente>/<float:tasa>/<int:plazoMeses>/', departamentos_views.info_departamento_proyecto_analyzer, name="info_departamento_proyecto"),
    path('departamentos/get_score_crediticio/', departamentos_views.get_score_crediticio, name='get_score_crediticio'),
    path('usuarios/crear/', crear_usuario_view, name='crear_usuario'),
    path('usuarios/actualizar/<str:dni>/', actualizar_usuario_view, name='actualizar-usuario'),
    path('usuarios/buscar/<str:dni>/', buscar_usuario_por_dni, name='buscar_usuario_por_dni'),
    # path('usuarios/actualizar/<str:dni>/', actualizar_usuario, name='actualizar_usuario'),
    path('send-simple-email/', send_email_with_attachments, name='send_simple_email'),

    path('', include("departments.urls")),
    path('', include("usuario.urls")),
    path('', include("proyects.urls")),
]
