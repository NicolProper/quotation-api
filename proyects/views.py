import datetime
import json
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import unidecode
from django.db.models import Q

from departments.models import Departamento
from .models import Proyecto
from .serializers import ProyectoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import ProyectosFilter
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from rest_framework import status

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
        



            
              
        
    
# API View to upload excel and save data to database
@api_view(['POST'])
def upload_data_project(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            
            nombre = data.get('nombre').lower()
            nombre_real = data.get('nombre_real').lower()
            texto_sin_tildes = unidecode.unidecode(nombre)
            slug = re.sub(r'\s+', '-', texto_sin_tildes.lower())
            distrito = data.get('distrito').lower()
            fecha_entrega = data.get('fecha_entrega') if not pd.isna(data.get('fecha_entrega')) else None
            fecha_ingreso = data.get('fecha_entrega') if not pd.isna(data.get('fecha_entrega')) else None
            banco = data.get('banco').lower() if not pd.isna(data.get('banco')) else None

            etapa = data.get('etapa').lower() if not pd.isna(data.get('etapa')) else None
            nro_pisos = data.get('nro_pisos') if not pd.isna(data.get('nro_pisos')) else None
            nro_dptos = data.get('nro_dptos') if not pd.isna(data.get('nro_dptos')) else None
            valor_de_separacion = data.get('valor_de_separacion') if not pd.isna(data.get('valor_de_separacion')) else None
            valor_porcentaje_inicial = data.get('valor_porcentaje_inicial') if not pd.isna(data.get('valor_porcentaje_inicial')) else None
            valor_porcentaje_financiado = data.get('valor_porcentaje_financiado') if not pd.isna(data.get('valor_porcentaje_financiado')) else None
            areas_comunes = True if data.get('areas_comunes') == "SI" else False
            piscina = True if data.get('piscina') == "SI" else False
            gym = True if data.get('gym') == "SI" else False
            coworking = True if data.get('coworking') == "SI" else False
            cine = True if data.get('cine') == "SI" else False
            parrilla = True if data.get('parrilla') == "SI" else False
            sum = True if data.get('sum') == "SI" else False
            bicicleta = True if data.get('bicicleta') == "SI" else False
            bar = True if data.get('bar') == "SI" else False
            coordenada_A = data.get('coordenada_A') if not pd.isna(data.get('coordenada_A')) else None
            coordenada_B = data.get('coordenada_B') if not pd.isna(data.get('coordenada_B')) else None
            
            
            dias_vacancia = data.get('dias_vacancia') if not pd.isna(data.get('dias_vacancia')) else None
            costo_porcentaje_operativo = data.get('costo_porcentaje_operativo') if not pd.isna(data.get('costo_porcentaje_operativo')) else None
            costo_porcentaje_administrativo = data.get('costo_porcentaje_administrativo') if not pd.isna(data.get('costo_porcentaje_administrativo')) else None
            costo_porcentaje_instalacion = data.get('costo_porcentaje_instalacion') if not pd.isna(data.get('costo_porcentaje_instalacion')) else None
            
            costo_porcentaje_capex_reparaciones = data.get('costo_porcentaje_capex_reparaciones') if not pd.isna(data.get('costo_porcentaje_capex_reparaciones')) else None
            costo_porcentaje_administrativos_venta = data.get('costo_porcentaje_administrativos_venta') if not pd.isna(data.get('costo_porcentaje_administrativos_venta')) else None
            corretaje = True if data.get('corretaje') == "SI" else False
            tasa_credito = data.get('tasa_credito') if not pd.isna(data.get('tasa_credito')) else None
            plazo_meses = data.get('plazo_meses') if not pd.isna(data.get('plazo_meses')) else None
            descuento_porcentaje_preventa = data.get('descuento_porcentaje_preventa') if not pd.isna(data.get('descuento_porcentaje_preventa')) else None


            correo_1 = data.get('correo_1').lower() if not pd.isna(data.get('correo_1')) else None
            crm = data.get('crm').lower() if not pd.isna(data.get('crm')) else None
            inmobiliaria = data.get('inmobiliaria').lower() if not pd.isna(data.get('inmobiliaria')) else None
            persona_contacto_1 = data.get('persona_contacto_1').lower() if not pd.isna(data.get('persona_contacto_1')) else None
            tipo_envio_leads = data.get('tipo_envio_leads').lower() if not pd.isna(data.get('tipo_envio_leads')) else None
 

            fields = {
                "nombre": nombre,
                "correo_1":correo_1,
                "crm":crm,
                "inmobiliaria":inmobiliaria,
                "persona_contacto_1": persona_contacto_1,
                "tipo_envio_leads": tipo_envio_leads,
                "nombre_real":nombre_real,
                "distrito": distrito,
                "banco": banco,
                "fecha_ingreso": fecha_ingreso,
                "areas_comunes": areas_comunes,
                "piscina": piscina,
                "gym": gym,
                "coworking": coworking,
                "cine": cine,
                "parrilla": parrilla,
                "sum": sum,
                "bicicleta": bicicleta,
                "bar": bar,
                "slug": slug,
                "fecha_entrega": fecha_entrega,
                "etapa": etapa,
                "nro_pisos": nro_pisos,
                "nro_dptos": nro_dptos,

                "valor_de_separacion": valor_de_separacion,
                "valor_porcentaje_inicial": valor_porcentaje_inicial,
                "valor_porcentaje_financiado": valor_porcentaje_financiado,
                "dias_vacancia": dias_vacancia,
                "costo_porcentaje_operativo": costo_porcentaje_operativo,
                "costo_porcentaje_administrativo": costo_porcentaje_administrativo,
                "costo_porcentaje_instalacion": costo_porcentaje_instalacion,
                "corretaje": corretaje,
                "tasa_credito": tasa_credito,
                "plazo_meses": plazo_meses,
                "descuento_porcentaje_preventa": descuento_porcentaje_preventa,
                "costo_porcentaje_capex_reparaciones": costo_porcentaje_capex_reparaciones,
                "costo_porcentaje_administrativos_venta": costo_porcentaje_administrativos_venta,
                "coordenada_A": coordenada_A,
                "coordenada_B": coordenada_B
            }

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            if fields_not_none:
                proyecto, created = Proyecto.objects.update_or_create(
                    nombre=fields_not_none['nombre'],
                    defaults=fields_not_none
                )
                if created:
                    return Response({'message': 'Proyecto Cargado'}, status=200)
                else:
                    return Response({'message': 'Proyecto Actualizado'}, status=200)

        except KeyError:
            return Response({'message': 'Archivo no válido'}, status=400)
        except pd.errors.EmptyDataError:
            return Response({'message': 'El archivo está vacío'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=500)



@api_view(['POST'])
def active_project(request, slug):
    if not slug:
        return Response({'message': 'El campo "slug" es obligatorio'}, status=201)

    try:
        proyecto = Proyecto.objects.filter(slug=slug).first()
        
        if not proyecto:
            return Response({'message': 'Proyecto no encontrado'}, status=201)
        
        filters_first = {
            'proyecto': proyecto,
            'estatus': "disponible",
            "ocultar": False
        }
        
        departamentos_first = Departamento.objects.filter(**filters_first).exists()
        
        if not departamentos_first:
            return Response({'message': 'No hay departamentos disponibles'}, status=201)
        
        filters = {
            'proyecto': proyecto,
            'roi__gt': 0,
            'tir__gt': 0,
            'renta__gt': 0,
            'estatus': "disponible",
            "ocultar": False
        }
        
        departamentos = Departamento.objects.filter(**filters).exists()

        if departamentos:
            proyecto.web = True
            proyecto.save()
            return Response({'message': 'Success'}, status=200)
        else:
            return Response({'message': 'No hay departamentos con índices positivos disponibles'}, status=201)

    except Exception as e:
        return Response({'message': 'Algo salió mal', 'details': str(e)}, status=400)

        

@api_view(['POST'])
def desactive_project(request, slug):
    if not slug:
        return Response({'error': 'El campo "slug" es obligatorio'}, status=400)

    try:
        proyecto = Proyecto.objects.get(slug=slug)
        proyecto.web = False
        proyecto.save()
        return Response({'message': 'Success'}, status=200)

    except Proyecto.DoesNotExist:
        return Response({'message': 'Something went wrong'}, status=400)
    
@api_view(['GET'])
def get_all_projects(request):
    # Utiliza values_list para obtener solo los nombres de los proyectos
    departamentos_data = Proyecto.objects.values_list('nombre', flat=True)

    # Devolver los departamentos como JSON
    return Response({'data': list(departamentos_data)})
        
@api_view(['GET'])
def get_all_projects_slugs(request):
    # Utiliza values_list para obtener solo los nombres de los proyectos
    departamentos_data = Proyecto.objects.values('nombre', 'slug')
    # Devolver los departamentos como JSON
    return Response({'data': list(departamentos_data)})
        
@api_view(['GET'])
def get_project_by_name(request, nombre):
    try:
        proyecto = Proyecto.objects.get(nombre=nombre)
        proyecto_data = {
            'nombre': proyecto.nombre,
            'nombre_real': proyecto.nombre_real,

            'distrito': proyecto.distrito,
            'banco': proyecto.banco,
            'fecha_entrega': proyecto.fecha_entrega,
            'fecha_ingreso': proyecto.fecha_ingreso,
            'etapa': proyecto.etapa,
            'banco': proyecto.banco,
            'nro_pisos': proyecto.nro_pisos,
            'nro_dptos': proyecto.nro_dptos,
            "valor_de_separacion": proyecto.valor_de_separacion,
            "valor_porcentaje_inicial" : proyecto.valor_porcentaje_inicial,
            "valor_porcentaje_financiado" : proyecto.valor_porcentaje_financiado,
    
            "areas_comunes": "SI" if proyecto.areas_comunes else "NO",
            "piscina":   "SI" if proyecto.piscina else "NO",
            "gym":  "SI" if proyecto.gym  else "NO",
            "coworking" :  "SI" if proyecto.coworking else "NO",
            "cine" :  "SI" if proyecto.cine else "NO",
            "parrilla" :  "SI" if  proyecto.parrilla else "NO",
            "sum" :   "SI" if proyecto.sum else "NO",
            "bicicleta":  "SI" if proyecto.bicicleta  else "NO",
            "workshop" :  "SI" if proyecto.workshop else "NO",
            "web":  "SI" if proyecto.web else "NO",
            "bar":  "SI" if proyecto.workshop else "NO",
            
            "dias_vacancia":proyecto.dias_vacancia,
            "costo_porcentaje_operativo":proyecto.costo_porcentaje_operativo,
            "costo_porcentaje_administrativo":proyecto.costo_porcentaje_administrativo,
            "costo_porcentaje_instalacion":proyecto.costo_porcentaje_instalacion,
            "corretaje": proyecto.corretaje ,
            "tasa_credito": proyecto.tasa_credito,
            "costo_porcentaje_capex_reparaciones":proyecto.costo_porcentaje_capex_reparaciones, #gastos de capital
            "plazo_meses" :proyecto.plazo_meses,
            "descuento_porcentaje_preventa":proyecto.descuento_porcentaje_preventa  ,
            "costo_porcentaje_administrativos_venta":proyecto.costo_porcentaje_administrativos_venta, #costo de cierre
            "coordenada_A":proyecto.coordenada_A if proyecto.coordenada_A else 0,
            "coordenada_B":proyecto.coordenada_B if proyecto.coordenada_B else 0,
            "correo_1": proyecto.correo_1,
            "crm": proyecto.crm,
            "inmobiliaria": proyecto.inmobiliaria,
            "persona_contacto_1": proyecto.persona_contacto_1,
            "tipo_envio_leads": proyecto.tipo_envio_leads            
            
            # Agrega más campos según sea necesario
        }
        return Response({'data': proyecto_data}, status=status.HTTP_200_OK)
    except Proyecto.DoesNotExist:
        return Response({'error': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
def updateDepartmentsDisponible(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            fecha_actualizacion = data.get('fecha_actualizacion')

            if fecha_actualizacion:
                # Convertir la fecha de entrada al formato adecuado
                fecha_actualizacion_db = datetime.strptime(fecha_actualizacion, '%d-%m-%Y').strftime('%Y-%m-%d')
                
                # Filtra los departamentos cuya fecha_actualizacion es diferente a la enviada
                departamentos_a_actualizar = Departamento.objects.exclude(fecha_actualizacion=fecha_actualizacion_db)
                
                # Actualiza el campo estatus a "no disponible"
                departamentos_a_actualizar.update(estatus='no disponible')

                return Response({'message': 'Departamentos actualizados exitosamente'}, status=200)
            else:
                return Response({'message': 'Fecha de actualización no proporcionada'}, status=400)
        except Exception as e:
            print(f'error: {e}')
            return Response({'message': 'Error al actualizar los departamentos'}, status=400)
        
        
@api_view(['GET'])
def get_info_inmobiliaria_project(request, slug):
    proyecto = Proyecto.objects.filter(slug=slug).first()
    if proyecto:
        data = {
            "correo_1": proyecto.correo_1,
            "crm": proyecto.crm,
            "inmobiliaria": proyecto.inmobiliaria,
            "persona_contacto_1": proyecto.persona_contacto_1,
            "tipo_envio_leads": proyecto.tipo_envio_leads,
        }
        return Response({'data': data})
    else:
        return Response({'data': {}}, status=404)
    
    
    
@api_view(['POST'])
def update_info_inmobiliaria_project(request, slug):
    try:

        data_ = request.body
        data = json.loads(data_)
        
        correo_1 = data.get('correo_1').lower() if not pd.isna(data.get('correo_1')) else None
        crm = data.get('crm').lower() if not pd.isna(data.get('crm')) else None
        inmobiliaria = data.get('inmobiliaria').lower() if not pd.isna(data.get('inmobiliaria')) else None
        persona_contacto_1 = data.get('persona_contacto_1').lower() if not pd.isna(data.get('persona_contacto_1')) else None
        tipo_envio_leads = data.get('tipo_envio_leads').lower() if not pd.isna(data.get('tipo_envio_leads')) else None
        
        project = Proyecto.objects.filter(slug=slug).first()
        
        
        if project:
            project.correo_1 = correo_1
            project.crm = crm
            project.inmobiliaria = inmobiliaria
            project.persona_contacto_1 = persona_contacto_1
            project.tipo_envio_leads = tipo_envio_leads
            
            project.save()
            return Response({'message': 'Datos actualizados correctamente'}, status=200)
        else:
            return Response({'message': 'Proyecto no encontrado'}, status=404)

    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error en la carga de datos'}, status=400)