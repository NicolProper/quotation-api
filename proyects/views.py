import datetime
import re
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import unidecode
from django.db.models import Q
from .models import Proyecto
from .serializers import ProyectoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ProyectosFilter
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all().order_by('id')  # Ordenar por el campo 'id' u otro campo adecuado
    serializer_class = ProyectoSerializer 
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProyectosFilter  # Usar el filtro personalizado
    ordering_fields = '__all__'

# API View to upload excel and save data to database
@api_view(['POST'])
def upload_data_excel(request):
    print(request)
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            print(file)
            proyecto_data = pd.read_excel(file)
            for index, row in proyecto_data.iterrows():
                print(row)

                nombre = row['nombre'].lower()
                # estatus = row['estatus'].lower()
                texto_sin_tildes = unidecode.unidecode(nombre)    
                slug =  re.sub(r'\s+', '-', texto_sin_tildes.lower())
                distrito = row['distrito'].lower()

                print("09")
                fecha_entrega = row['fecha_entrega'] if not pd.isna(row['fecha_entrega']) else None
                # fecha_actualizacion = row['fecha_actualizacion'] if not pd.isna(row['fecha_actualizacion']) else None
                # precio_desde = row['precio_desde'] if not pd.isna(row['precio_desde']) else None
                etapa =  row['etapa'].lower() if not pd.isna(row['etapa']) else None
                nro_pisos = row['nro_pisos'] if not pd.isna(row['nro_pisos']) else None
                nro_dptos = row['nro_dptos'] if not pd.isna(row['nro_dptos']) else None
                valor_de_separacion = row['valor_de_separacion'] if not pd.isna(row['valor_de_separacion']) else None
                print("09")
                valor_inicial = row['valor_inicial'] if not pd.isna(row['valor_inicial']) else None
                print(1)
                valor_financiado = row['valor_financiado'] if not pd.isna(row['valor_financiado']) else None
                print(2)
                valor_porcentaje_inicial = row['valor_porcentaje_inicial'] if not pd.isna(row['valor_porcentaje_inicial']) else None
                print(3)
                valor_porcentaje_financiado = row['valor_porcentaje_financiado'] if not pd.isna(row['valor_porcentaje_financiado']) else None
                print("09")
                areas_comunes =True if row['areas_comunes'] == "SI" else False
                piscina=True if row['piscina'] == "SI" else False
                gym =True if row['gym'] == "SI" else False
                coworking =True if row['coworking'] == "SI" else False
                cine =True if row['cine'] == "SI" else False
                parrilla =True if row['parrilla'] == "SI" else False
                sum =True if row['sum'] == "SI" else False
                bicicleta =True if row['bicicleta'] == "SI" else False
                bar =True if row['bar'] == "SI" else False
                print(4444)


                banco=row['banco'].lower() if not pd.isna(row['banco']) else None
                renta= row['renta'] if not pd.isna(row['renta']) else None
                roi= row['roi'] if not pd.isna(row['roi']) else None
                tir= row['tir'] if not pd.isna(row['tir']) else None
                valor_alquiler= row['valor_alquiler'] if not pd.isna(row['valor_alquiler']) else None
                valor_cuota= row['valor_cuota'] if not pd.isna(row['valor_cuota']) else None
                tipo_moneda=row['tipo_moneda'].lower() if not pd.isna(row['tipo_moneda']) else None
                
                print('11')

                dias_vacancia=row['dias_vacancia'] if not pd.isna(row['dias_vacancia']) else None
                costo_porcentaje_operativo=row['costo_porcentaje_operativo'] if not pd.isna(row['costo_porcentaje_operativo']) else None
                costo_porcentaje_administrativo=row['costo_porcentaje_administrativo'] if not pd.isna(row['costo_porcentaje_administrativo']) else None
                costo_porcentaje_instalacion=row['costo_porcentaje_instalacion'] if not pd.isna(row['costo_porcentaje_instalacion']) else None
                corretaje= True if row['corretaje'] == "SI" else False
                tasa_credito= row['tasa_credito'] if not pd.isna(row['tasa_credito']) else None
                plazo_meses = row['plazo_meses'] if not pd.isna(row['plazo_meses']) else None
                descuento_porcentaje_preventa=row['descuento_porcentaje_preventa'] if not pd.isna(row['descuento_porcentaje_preventa']) else None
                coordenada_A=row['coordenada_A'] if not pd.isna(row['coordenada_A']) else None
                coordenada_B=row['coordenada_B'] if not pd.isna(row['coordenada_B']) else None
                print(8888888)
                costo_porcentaje_capex_reparaciones=row['costo_porcentaje_capex_reparaciones'] if not pd.isna(row['costo_porcentaje_capex_reparaciones']) else None
                costo_porcentaje_administrativos_venta=row['costo_porcentaje_administrativos_venta'] if not pd.isna(row['costo_porcentaje_administrativos_venta']) else None
                projects_created = []
               
                fields = {
                    "nombre":nombre,
                    "distrito":distrito,
                    "banco":banco,
                    "tipo_moneda":tipo_moneda,
                    "areas_comunes" :areas_comunes,
                    "piscina":piscina,
                    "gym" :gym,
                    "coworking" :coworking,
                    "cine" :cine,
                    "parrilla" :parrilla,
                    "sum" :sum,
                    "bicicleta" :bicicleta,
                    "bar" :bar,
                    # "precio_desde":precio_desde,
                    "slug":slug,
                    "fecha_entrega":fecha_entrega,
                    "etapa":etapa,
                    "nro_pisos":nro_pisos,
                    "nro_dptos":nro_dptos,
                    "valor_de_separacion":valor_de_separacion,
                    "valor_inicial":valor_inicial,
                    "valor_financiado":valor_financiado,
                    "valor_porcentaje_inicial":valor_porcentaje_inicial,
                    "valor_porcentaje_financiado":valor_porcentaje_financiado,

                    "valor_alquiler": valor_alquiler,
                    "valor_cuota": valor_cuota,
                    "dias_vacancia":dias_vacancia,
                    "costo_porcentaje_operativo":costo_porcentaje_operativo,
                    "costo_porcentaje_administrativo":costo_porcentaje_administrativo,
                    "costo_porcentaje_instalacion":costo_porcentaje_instalacion,
                    "corretaje": corretaje,
                    "tasa_credito": tasa_credito,
                    "plazo_meses" : plazo_meses,
                    "descuento_porcentaje_preventa":descuento_porcentaje_preventa,
                    "costo_porcentaje_capex_reparaciones":costo_porcentaje_capex_reparaciones,
                    "costo_porcentaje_administrativos_venta":costo_porcentaje_administrativos_venta,
                    "coordenada_A":coordenada_A,
                    "coordenada_B":coordenada_B
                    
                }
                print(fields)

                fields_not_none = {key: value for key, value in fields.items() if value is not None}

                if fields_not_none:
                    proyecto, created = Proyecto.objects.update_or_create(
                        nombre=fields_not_none['nombre'],
                        defaults=fields_not_none
                    )
                    if created:
                        projects_created.append(fields_not_none)
                    else:
                        print('updated' , nombre)    

            return Response(projects_created, status=200)

        except KeyError:
            print(KeyError)
            return Response({'error': 'Archivo no válido'}, status=400)
        except pd.errors.EmptyDataError:
            return Response({'error': 'El archivo está vacío'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


    

    
    
    
    
    
    
@api_view(['GET'])
def get_all_proyects_web(reques):
    proyectos = Proyecto.objects.filter(web=True)
    departamentos_data = []
    for proyecto in proyectos:
        departamentos_data.append(proyecto.slug)
    
    # Devolver los departamentos como JSON
    return Response({'data': departamentos_data})
        



            
              
        
    


        
