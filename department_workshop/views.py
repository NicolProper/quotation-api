import datetime
import json
import re
import numpy_financial as npf
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import requests
import unidecode
from departments.models import Departamento
from department_workshop.models import Departamento_Workshop
from informacion.models import Bancaria
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from project_workshop.models import Proyecto_Workshop
from proyects.models import Proyecto
from financiamiento.models import Cliente
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import generics
from rest_framework.filters import OrderingFilter
import xlwings as xw
from django.db import models

from datetime import date, timedelta
from django.db.models import F, Case, When, FloatField, Value
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


@api_view(['POST'])
def upload_data_department(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            print(data)
            fecha_workshop = data.get('fecha_workshop') if not pd.isna(data.get('fecha_workshop')) else None
            proyecto = data.get('proyecto').lower() if not pd.isna(data.get('proyecto')) else None
            nro_depa = str(data.get('nro_depa')) if not pd.isna(data.get('nro_depa')) else None
            precio = data.get('precio') if not pd.isna(data.get('precio')) else None
            precio_workshop = data.get('precio_workshop') if not pd.isna(data.get('precio_workshop')) else None

            fields = {
                'proyecto': proyecto,
                'precio_workshop': precio_workshop,
                'fecha_workshop': fecha_workshop,
                'nro_depa': nro_depa,
                'precio': precio,
            }
            print(Departamento_Workshop.objects.all())

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            if fields_not_none:
                proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                
                if proyecto_obj:
                    existing_department = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto_obj).first()
                    
                    if existing_department:
                        # Crear o actualizar el registro en departments_workshop
                        department_workshop, created = Departamento_Workshop.objects.update_or_create(
                            nro_depa=nro_depa, proyecto=proyecto_obj,  fecha_workshop=fecha_workshop,
                            defaults={
                                'precio_workshop': precio_workshop,
                                'fecha_workshop': fecha_workshop,
                                'precio': precio,
                            }
                        )
                        if created:
                            print('Registro creado en departments_workshop')
                        else:
                            print('Registro actualizado en departments_workshop')

            return Response({'message': 'Datos procesados correctamente'}, status=200)

        except Exception as e:
            print(f'Error: {e}')
            return Response({'message': 'Error en la carga de datos'}, status=400)
        

@api_view(['POST'])
def get_departments_workshop(request):
    try:
        data_ = request.body
        data = json.loads(data_)
        print(data)
        
        fecha_workshop_str = data.get('fecha_workshop')
        fecha_workshop = None
        if fecha_workshop_str and not pd.isna(fecha_workshop_str):
            fecha_workshop = datetime.datetime.strptime(fecha_workshop_str, '%Y-%m-%d').date()

        departamentos = Departamento_Workshop.objects.filter(fecha_workshop=fecha_workshop)
        data = []
        for depa in departamentos:
            data.append({
                "proyecto": depa.proyecto.nombre,
                "nro_depa": depa.nro_depa,
                "precio": depa.precio,
                "precio_workshop": depa.precio_workshop,
                "proyecto_id": depa.proyecto.id
            })
                
        return Response({'data': data}, status=200)
    except Exception as e:
        print(f'Error: {e}')
        return Response({'error': []}, status=400)
    
    
    
@api_view(['GET'])
def get_nro_depas_by_project_workshop(request, id):
    try:
        # Filtrar el proyecto por slug
        # proyecto = Proyecto_Workshop.objects.filter(proyecto_id=id).first()

            nro_depas = Departamento_Workshop.objects.filter(proyecto_id=id).values_list('nro_depa', flat=True)
            
            return Response({'data': list(nro_depas)}, status=200)
        # else:
        #     return Response({'message': 'Proyecto no encontrado', "data":[]}, status=404)
    
    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error al obtener los departamentos',"data":[]}, status=500)
    
    
@api_view(['GET'])
def get_info_department_by_nro_depa(request, nro_depa, id):
    
    try:
        data = Departamento_Workshop.objects.filter(nro_depa=nro_depa, proyecto_id=id).first()
        if data:
            obj = {
                "proyecto": data.proyecto.nombre,
                "fecha_workshop": data.fecha_workshop,
                "precio": data.precio,
                "nro_depa": data.nro_depa,
                "precio_workshop": data.precio_workshop
                
            }
            return Response({'data': obj}, status=200)
        else:
            return Response({'message': 'Departamento no encontrado', "data": {}}, status=404)
    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error al obtener los departamentos', "data": {}}, status=500)
    
    
    
@api_view(['POST'])
def delete_department(request, nro_depa, id):
    try:
        print(nro_depa,id)

        data = Departamento_Workshop.objects.filter(nro_depa=nro_depa, proyecto_id=id).first()
        if data:
            data.delete()
            return Response({'message': 'Departamento eliminado exitosamente', 'data': True}, status=200)
        else:
            return Response({'message': 'Departamento no encontrado', 'data': False}, status=201)
        
    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error al eliminar el departamento', 'data': False}, status=201)