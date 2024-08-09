import json
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.decorators import api_view

from cotizaciones.models import Proyectos
from cotizaciones.serializers import CotizacionesSerializer
from departments.models import Departamento
from proyects.models import Proyecto

# Create your views here.
class CotizacionViewSet(viewsets.ModelViewSet):
    queryset = Proyectos.objects.all().order_by('id')  # Ordenar por el campo 'id' u otro campo adecuado
    serializer_class = CotizacionesSerializer 
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = USE  # Usar el filtro personalizado
    ordering_fields = '__all__'
    
    
def save_cotizacion(fecha, asesor, correo_asesor,cliente, dni, proyecto, proyecto_nombre, departamento, departamento_nro):

    # Crear un nuevo usuario
    nueva_cotizacion = Proyectos(fecha=fecha, asesor=asesor, correo_asesor=correo_asesor,cliente=cliente, dni=dni, proyecto=proyecto, proyecto_nombre=proyecto_nombre, departamento=departamento, departamento_nro=departamento_nro)
    nueva_cotizacion.save()

    return nueva_cotizacion

                # proyecto =  row['proyecto'].lower() if not pd.isna(row['proyecto']) else None

# usuario/views.py
@api_view(['POST'])
def crear_cotizacion(request):
    if request.method == 'POST':
        data_ = request.body
        data = json.loads(data_)
        
        fecha= data.get('fecha')
        asesor= data.get('asesor')
        correo_asesor=data.get('correo_asesor')
        cliente=data.get('cliente')
        dni= data.get('dni') 
        proyecto=None
        # proyecto=Proyecto.objects.get(id=data.get('proyecto')) if data.get('proyecto')!=0 else None
        proyecto_nombre=data.get('proyecto_nombre')
        # departamento=Departamento.objects.get(id=data.get('departamento')) if not data.get('departamento')!=0 else None
        departamento_nro=data.get('departamento_nro')
        departamento=None
        print(fecha, asesor, correo_asesor,cliente, dni, proyecto, proyecto_nombre, departamento, departamento_nro)

        try:
            cotizacion_creada = save_cotizacion(fecha, asesor, correo_asesor,cliente, dni, proyecto, proyecto_nombre, departamento, departamento_nro)
            return JsonResponse({'mensaje': 'Usuario creado exitosamente', 'id': cotizacion_creada.id}, status=201)
        except ValueError as e:
            return JsonResponse({'mensaje': str(e)}, status=201)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)