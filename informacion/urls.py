
from django.urls import path, register_converter
from .views import (
    actualizar_usuario_view, 
    buscar_usuario_por_dni, 
    crear_usuario_view, 
    send_email_with_attachments
)

class FloatConverter:
    regex = r'\d+(\.\d+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConverter, 'float')

urlpatterns = [
    path('crear/', crear_usuario_view, name='crear_usuario'),
    path('actualizar/<str:dni>/', actualizar_usuario_view, name='actualizar-usuario'),
    
    path('buscar/<str:dni>/', buscar_usuario_por_dni, name='buscar_usuario_por_dni'),
    path('send-simple-email/', send_email_with_attachments, name='send_simple_email'),
]
