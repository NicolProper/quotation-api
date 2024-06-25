from argparse import Action
from base64 import b64decode
import datetime
from io import BytesIO
import json
import math
import numpy_financial as npf

import os
from django.http import HttpResponse, JsonResponse
import numpy as np
from .models import Departamento
from .serializers import DepartamentoSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from proyects.models import Proyecto
from .filters import DepartamentoFilter, DepartamentoFilter2
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .filters import DepartamentoFilter
from rest_framework.decorators import action
import xlwings as xw
from rest_framework.viewsets import ModelViewSet
from django.db.models import Min, F
from django.conf import settings  # Importa la configuración de Django
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
class DepartamentoViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['proyecto', 'nro_banos', 'nro_dormitorios']
    filterset_class = DepartamentoFilter  # Use the custom filter set

    ordering_fields = '__all__'
    
    
    

class DepartamentoViewSet2(ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    filterset_class = DepartamentoFilter2

    def list(self, request, proyecto=None):
        queryset = self.get_queryset().filter(proyecto=proyecto)
        filter_params = request.GET.dict()
        # tir_values = []
        # Obtener los valores de tir y roi para todos los departamentos
        
        nombre_campo_relacionado  = Proyecto.objects.filter(id=proyecto).values_list('nombre', flat=True).first()

        

        # for departamento in queryset:
            # tir, roi, cuota_credito_hipotecario = analyze(departamento.precio, departamento.valor_alquiler)
            # departamento.tir=tir
            # departamento.roi=roi
            # departamento.cuota_credito_hipotecario =cuota_credito_hipotecario
            # departamento.gross_yield = gross_yield
            # departamento.valor_alquiler =22222222222222222222
            
         

        if filter_params:
            # Aplicar filtro por precio
             # Filtro por tir
            if 'tir_min' in filter_params and 'tir_max' in filter_params:
                tir_min = float(filter_params.get('tir_min', 0))
                tir_max = float(filter_params.get('tir_max', float('inf')))
                queryset = [departamento for departamento in queryset if tir_min <= departamento.tir <= tir_max]
                print(queryset)
                
            if 'roi_min' in filter_params and 'roi_max' in filter_params:
                roi_min = float(filter_params.get('roi_min', 0))
                roi_max = float(filter_params.get('roi_max', float('inf')))
                queryset = [departamento for departamento in queryset if roi_min <= departamento.roi <= roi_max]
                
                
            if 'cuota_credito_hipotecario_min' in filter_params and 'cuota_credito_hipotecario_max' in filter_params:
                cuota_credito_hipotecario_min = float(filter_params.get('cuota_credito_hipotecario_min', 0))
                cuota_credito_hipotecario_max = float(filter_params.get('cuota_credito_hipotecario_max', float('inf')))
                queryset = [departamento for departamento in queryset if cuota_credito_hipotecario_min <= departamento.cuota_credito_hipotecario <= cuota_credito_hipotecario_max]

        

        # Iterar sobre los objetos filtrados y realizar operaciones si es necesario
        departamentos_data = []
        for departamento in queryset:
            departamento_data = {
                'nombre': departamento.nombre,
                'nro_banos': departamento.nro_banos,
                'nro_dormitorios': departamento.nro_dormitorios,
                'unit_area': departamento.unit_area,
                'valor_alquiler': departamento.valor_alquiler,
                'precio': departamento.precio,
                'tir': departamento.tir,
                'cuota_credito_hipotecario': departamento.cuota_credito_hipotecario,
                'roi': departamento.roi,
                "proyecto_nombre": nombre_campo_relacionado,
                # "gross_yield":departamento.gross_yield
            }
            departamentos_data.append(departamento_data)

        # Devolver los datos en forma de respuesta JSON
        return Response(departamentos_data)








@api_view(['POST'])
def upload_data_excel(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            departamentos_data = pd.read_excel(file)
            list_departments = []
            wb = xw.Book('calc.xlsx')
            for index, row in departamentos_data.iterrows():
                
                
                proyecto =  row['proyecto'].lower() if not pd.isna(row['proyecto']) else None
                nombre = row['nombre'] if not pd.isna(row['nombre']) else None
                nro_depa = row['nro_depa'] if not pd.isna(row['nro_depa']) else None
                valor_descuento_preventa = row['valor_descuento_preventa'] if not pd.isna(row['valor_descuento_preventa']) else None
                tipo_inventario = row['tipo_inventario'] if not pd.isna(row['tipo_inventario']) else None
                tipo_moneda=row['tipo_moneda'].lower() if not pd.isna(row['tipo_moneda']) else None

                
                proyecto =  row['proyecto'].lower() if not pd.isna(row['proyecto']) else None
                nombre = row['nombre'] if not pd.isna(row['nombre']) else None
                fecha_entrega = row['fecha_entrega'] if not pd.isna(row['fecha_entrega']) else None
                nro_depa = row['nro_depa'] if not pd.isna(row['nro_depa']) else None
                unit_area = row['unit_area'] if not pd.isna(row['unit_area']) else None
                nro_dormitorios =row['nro_dormitorios'] if not pd.isna(row['nro_dormitorios']) else None
                nro_banos = row['nro_banos'] if not pd.isna(row['nro_banos']) else None
                valor_alquiler = row['valor_alquiler'] if not pd.isna(row['valor_alquiler']) else None
                valor_cuota = row['valor_cuota'] if not pd.isna(row['valor_cuota']) else None
                piso = row['piso'] if not pd.isna(row['piso']) else None
                vista = row['vista'].lower() if not pd.isna(row['vista']) else None
                precio = row['precio'] if not pd.isna(row['precio']) else None
                precio_workshop = row['precio_workshop'] if not pd.isna(row['precio_workshop']) else None
                valor_descuento_preventa = row['valor_descuento_preventa'] if not pd.isna(row['valor_descuento_preventa']) else None
                tipo_inventario = row['tipo_inventario'] if not pd.isna(row['tipo_inventario']) else None
                tipo_moneda=row['tipo_moneda'].lower() if not pd.isna(row['tipo_moneda']) else None
                tipo_departamento= row['tipo_departamento'] if not pd.isna(row['tipo_departamento']) else None
                fecha_actualizacion = row['fecha_actualizacion'] if not pd.isna(row['fecha_actualizacion']) else None
                estatus = row['estatus'].lower() if not pd.isna(row['estatus']) else None
 

                tir_=0
                roi_=0
                valor_cuota_=0
                renta_=0
                tasa= 0.075
                patrimonio_inicial_ =  0
                patrimonio_anio_5_ =  0
                patrimonio_anio_10_ =  0
                patrimonio_anio_20_ =  0
                patrimonio_anio_30_ =  0
                proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                fecha_entrega_updated=datetime.date.today().replace(day=1) if proyecto_obj.etapa =="inmediata" else proyecto_obj.fecha_entrega


                if precio and valor_alquiler and unit_area and proyecto_obj.valor_porcentaje_inicial and proyecto_obj.fecha_entrega and fecha_entrega_updated:
                     
                    newprecio= precio*3.8 if tipo_moneda =="usd" else precio
                    precio_dolar= precio if tipo_moneda =="usd" else None
                    proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                    print('proyecto:', proyecto_obj.nombre)
                    
                    roi, tir, cuota_credito_hipotecario, gross_yield, valor_patrimonio_compra , valor_patrimonio_5, valor_patrimonio_10, valor_patrimonio_20, valor_patrimonio_30 = analyze( proyecto_obj.tasa_credito, newprecio, valor_alquiler, unit_area, proyecto_obj.valor_porcentaje_inicial, fecha_entrega_updated,  proyecto_obj.costo_porcentaje_instalacion, proyecto_obj.descuento_porcentaje_preventa, proyecto_obj.costo_porcentaje_operativo, proyecto_obj.costo_porcentaje_administrativo, proyecto_obj.corretaje, proyecto_obj.plazo_meses, proyecto_obj.dias_vacancia, proyecto_obj.costo_porcentaje_capex_reparaciones ,wb)
                    tir_ = round(tir,4)
                    roi_ = round(roi,4)
                    renta_= round(gross_yield,4)
                    valor_cuota_= round(cuota_credito_hipotecario,4)
                    patrimonio_inicial_ =  round(valor_patrimonio_compra,4)
                    patrimonio_anio_5_ =  round(valor_patrimonio_5,4)
                    patrimonio_anio_10_ =  round(valor_patrimonio_10,4)
                    patrimonio_anio_20_ =  round(valor_patrimonio_20,4)
                    patrimonio_anio_30_ =  round(valor_patrimonio_30,4)


       


                fields = {
                    'tasa': tasa,
                    'nombre': nombre,
                    "fecha_actualizacion":fecha_actualizacion,
                    "estatus":estatus,
                    'fecha_entrega': fecha_entrega,
                    'nro_depa': nro_depa,
                    'unit_area': unit_area,
                    'nro_dormitorios': nro_dormitorios,
                    'nro_banos': nro_banos,
                    'valor_alquiler': valor_alquiler,
                    'valor_cuota': valor_cuota,
                    'piso': piso,
                    'vista': vista,
                    'precio': newprecio,
                    "precio_dolar":precio_dolar,
                    'precio_workshop': precio_workshop,
                    'valor_descuento_preventa': valor_descuento_preventa,
                    'tipo_moneda': tipo_moneda,
                    "tipo_departamento":tipo_departamento,
                    "tipo_inventario":tipo_inventario,
                    'patrimonio_inicial': patrimonio_inicial_,
                    "patrimonio_anio_5":patrimonio_anio_5_,
                    "patrimonio_anio_10":patrimonio_anio_10_,
                    'patrimonio_anio_20': patrimonio_anio_20_,
                    'patrimonio_anio_30': patrimonio_anio_30_,
                    "tir":tir_,
                    "roi":roi_,
                    "valor_cuota":valor_cuota_,
                    "renta": renta_
                }
                # print(fields)

                # Filtrar los campos que tienen valores diferentes de None
                fields_not_none = {key: value for key, value in fields.items() if value is not None}

                if fields_not_none:
                    if  tipo_inventario == "proyecto":
                        proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                        
                        if proyecto_obj:
                            nro_depa = fields_not_none.get('nro_depa')  # Obtener el número de departamento
                            existing_department = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto_obj).first()
                            
                            if existing_department:
                                # Si ya existe un departamento con el mismo número y proyecto, actualizar sus campos
                                for key, value in fields_not_none.items():
                                    setattr(existing_department, key, value)
                                existing_department.save()
                                print('updated')
                            else:
                                # Si no existe, crear un nuevo departamento
                                departamento = Departamento.objects.create(proyecto=proyecto_obj, **fields_not_none)
                                list_departments.append(fields_not_none)
                    elif tipo_inventario == "c/inquilino":

                        nombre_depa = fields_not_none.get('nombre')  # Obtener el número de departamento
                        existing_department = Departamento.objects.filter(nombre=nombre_depa).first()
                        
                        if existing_department:
                            # Si ya existe un departamento con el mismo número y proyecto, actualizar sus campos
                            for key, value in fields_not_none.items():
                                setattr(existing_department, key, value)
                            existing_department.save()
                        else:
                            # Si no existe, crear un nuevo departamento
                            Departamento.objects.create(**fields_not_none)
                            list_departments.append(fields_not_none)


            # Llamar a la función para procesar departamentos
                    # process_departments(tipo_inventario, proyecto, fields_not_none, list_departments)

            return Response(list_departments, status=200)

        except Exception as e:
            # print(row)
            print(f'error: {e}')
            return Response({'message': 'Error on file upload'}, status=400)



        
@api_view(['GET'])
def update_all_data(request):
    # if request.method == 'POST':
        try:
            proyecto=Proyecto.objects.filter(nombre="surquillo2").first()
            departamentos= Departamento.objects.filter(estatus="disponible",        
            proyecto=proyecto,                                           
          
            )
            list_departments = []
            wb = xw.Book('calc.xlsx')
            for departamento in departamentos:

                print(departamento.proyecto.id)  

                tir_=0
                roi_=0
                valor_cuota_=0
                renta_=0
                patrimonio_inicial_ =  0
                patrimonio_anio_5_ =  0
                patrimonio_anio_10_ =  0
                patrimonio_anio_20_ =  0
                patrimonio_anio_30_ =  0
                proyecto_obj = Proyecto.objects.filter(id=departamento.proyecto.id).first()
                fecha_entrega=datetime.date.today().replace(day=1) if proyecto_obj.etapa =="inmediata" else proyecto_obj.fecha_entrega

                if departamento.precio and departamento.valor_alquiler and departamento.unit_area and proyecto_obj.valor_porcentaje_inicial and fecha_entrega:
                     
                    print('proyecto:', proyecto_obj.nombre)   
                    print(departamento.precio) 
                    roi, tir, cuota_credito_hipotecario, gross_yield, valor_patrimonio_compra , valor_patrimonio_5, valor_patrimonio_10, valor_patrimonio_20, valor_patrimonio_30 = analyze( proyecto_obj.tasa_credito, departamento.precio, departamento.valor_alquiler, departamento.unit_area, proyecto_obj.valor_porcentaje_inicial, fecha_entrega,  proyecto_obj.costo_porcentaje_instalacion, proyecto_obj.descuento_porcentaje_preventa, proyecto_obj.costo_porcentaje_operativo, proyecto_obj.costo_porcentaje_administrativo, proyecto_obj.corretaje, proyecto_obj.plazo_meses, proyecto_obj.dias_vacancia, proyecto_obj.costo_porcentaje_capex_reparaciones ,wb)
                    tir_ = round(tir,4)
                    roi_ = round(roi,4)
                    renta_= round(gross_yield,4)
                    valor_cuota_= round(cuota_credito_hipotecario,4)
                    patrimonio_inicial_ =  round(valor_patrimonio_compra,4)
                    patrimonio_anio_5_ =  round(valor_patrimonio_5,4)
                    patrimonio_anio_10_ =  round(valor_patrimonio_10,4)
                    patrimonio_anio_20_ =  round(valor_patrimonio_20,4)
                    patrimonio_anio_30_ =  round(valor_patrimonio_30,4)


       


                fields = {
                    "nro_depa": departamento.nro_depa,
                    'patrimonio_inicial': patrimonio_inicial_,
                    "patrimonio_anio_5":patrimonio_anio_5_,
                    "patrimonio_anio_10":patrimonio_anio_10_,
                    'patrimonio_anio_20': patrimonio_anio_20_,
                    'patrimonio_anio_30': patrimonio_anio_30_,
                    "tir":tir_,
                    "roi":roi_,
                    "valor_cuota":valor_cuota_,
                    "renta": renta_
                }




                fields_not_none = {key: value for key, value in fields.items() if value is not None}

                if fields_not_none:
                        
                        if proyecto_obj:
                            nro_depa = fields_not_none.get('nro_depa')  # Obtener el número de departamento
                            existing_department = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto_obj).first()
                            
                            if existing_department:
                                # Si ya existe un departamento con el mismo número y proyecto, actualizar sus campos
                                for key, value in fields_not_none.items():
                                    setattr(existing_department, key, value)
                                existing_department.save()
                                print('updated')
                            else:
                                # Si no existe, crear un nuevo departamento
                                departamento = Departamento.objects.create(proyecto=proyecto_obj, **fields_not_none)
                                list_departments.append(fields_not_none)



            # Llamar a la función para procesar departamentos
                    # process_departments(tipo_inventario, proyecto, fields_not_none, list_departments)

            return Response(list_departments, status=200)

        except Exception as e:
            # print(row)
            print(f'error: {e}')
            return Response({'message': 'Error on file upload'}, status=400)






def sum_product(arr1, arr2):
    return sum(val1 * val2 for val1, val2 in zip(arr1, arr2))

# En un archivo util.py (por ejemplo)

def calcular_van(pago_periodico, tasa_interes, valor_presente):
    """
    Calcula el Valor Actual Neto (VAN) de una inversión.
    
    Args:
    - pago_periodico (float): Pago periódico.
    - tasa_interes (float): Tasa de interés por período (por ejemplo, 5% se ingresa como 0.05).
    - valor_presente (float): Valor presente o inversión inicial.
    
    Returns:
    - float: Valor Actual Neto (VAN) calculado.
    """
    tasa_interes = tasa_interes / 100.0  # Convertir la tasa de interés a decimal si es necesario
    
    # Calcular VAN
    van = -valor_presente  # Valor presente inicial (negativo por ser un desembolso)
    for i in range(1, 13):  # Suponiendo 12 períodos
        van += pago_periodico / (1 + tasa_interes) ** i
    
    return van

def calculate_cell_value(cell_value, dataIngresos, plazo, tasa):
    constants = [
                    [ 'bcp', 'ibk', 'bbva', 'pichincha', 'banbif', 'scotiabank'],
                    [ 1, 0.2, 1, 1, 1, 1],
                    [ 0, 0, 0, 0, 0, 0],
                    [ 1, 0, 0, 0, 0, 0],
                    [ 1, 1, 1, 1, 1, 1],
                    [ 1, 1, 1, 1, 1, 1],
                    [ 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                    [ 0, 0, 0, 0, 0, 0]

                ]
   
    
    position=constants[0].index(cell_value)
    data={}
    
    for index, (x, ingreso) in  enumerate(zip(constants, dataIngresos)):
        print("index", index)
        if index==0:
            data[x[position]]=0
            # print(x[position])
        elif index==1 or index==2 or index==3 or index==4 or index==5:
            data[cell_value]+= float(x[position])*float(ingreso)
        elif index==6:
             data[cell_value]= data[cell_value]*float(x[position])
        elif index==7:
             print("ingreso", ingreso)
             data[cell_value]-= float(ingreso)

    tasa_mensual = tasa / 12

    
    cuota_mensual = -npf.pv(rate=tasa_mensual, nper=plazo, pmt=data[cell_value])
# return vpn
        
            
            
    print(cuota_mensual)
    

    return {cell_value:cuota_mensual}
    
@api_view(['POST'])
def get_score_crediticio(request):
    if request.method == 'POST':
        try:


            data_ = request.body
            data = json.loads(data_)

            
            nombre_completo= data.get('nombre_completo')
            DNI=data.get('DNI')
            edad=data.get('edad')
            residencia= data.get('residencia') #Perú , Extranjero
            ingreso_primera_categoria=data.get('ingreso_primera_categoria')
            ingreso_segunda_categoria=data.get('ingreso_segunda_categoria')
            ingreso_tercera_categoria=data.get('ingreso_tercera_categoria')
            ingreso_cuarta_categoria=data.get('ingreso_cuarta_categoria')
            ingreso_quinta_categoria=data.get('ingreso_quinta_categoria')
            primera_vivienda=data.get('primera_vivienda') #SÍ/NO
            cuota_hipotecaria=data.get('cuota_hipotecaria') 
            cuota_vehicular=data.get('cuota_vehicular')
            cuota_personal=data.get('cuota_personal')
            cuota_tarjeta_credito=data.get('cuota_tarjeta_credito')
            cuota_inicial=data.get('cuota_inicial')
            tasa=data.get('tasa')

            total_deudas=0
            
            print(00)
           
            #¿INGRESO SOLO 3ER CATEGORIA?        
            ingreso_solo_tercera_categoria= getIngresoSoloTerceraCategoria(ingreso_primera_categoria, ingreso_segunda_categoria,ingreso_tercera_categoria , ingreso_cuarta_categoria,ingreso_quinta_categoria)
            
            # TOTAL DEUDAS
            total_deudas=total_deudas + cuota_hipotecaria + cuota_vehicular+cuota_personal + cuota_tarjeta_credito
               
            # EDAD
            plazo_meses= getPlazoMese(edad, primera_vivienda)

 
            dataIngresos=[
                0,
            ingreso_primera_categoria,
            ingreso_segunda_categoria,
            ingreso_tercera_categoria,
            ingreso_cuarta_categoria,
            ingreso_quinta_categoria,
            0,
            total_deudas
            ]
      
            
            BCP = calculate_cell_value('bcp', dataIngresos, plazo_meses, tasa)
            IBK = calculate_cell_value('ibk',dataIngresos, plazo_meses, tasa)
            BBVA = calculate_cell_value('bbva', dataIngresos, plazo_meses, tasa)
            PICHINCHA = calculate_cell_value('pichincha', dataIngresos, plazo_meses, tasa)
            BANBIF = calculate_cell_value('banbif', dataIngresos, plazo_meses, tasa)
            SCOTIABANK = calculate_cell_value('scotiabank', dataIngresos, plazo_meses, tasa)
            
            
            context = [
                 BCP,
                 IBK,
                 BBVA,
                 PICHINCHA,
                 BANBIF,
                 SCOTIABANK,
            ]
            
            print('CONTEXT')
            print(context)
            result= map(lambda x : list(x.values())[0], context)
            min_value=sorted(result)
            
            resultadoDepartamentos=[]
            
            resultado_final=getDepasAprobados(resultadoDepartamentos,ingreso_solo_tercera_categoria,residencia,primera_vivienda, cuota_inicial, context, min_value)                 
            print(resultadoDepartamentos)
                        
            return JsonResponse({ "size":len(resultado_final), "data":resultado_final}, safe=False)
        except Exception as e:
            print(f'Error: {e}')
            return Response({'message': 'Error en el procesamiento'}, status=400)

    return Response({'message': 'Método no permitido'}, status=405)


def getPrecioReal(precio, tipo_moneda):

            if tipo_moneda == "pen":
                precio_real = precio
            else:
                precio_real = precio * 3.8
            
            return precio_real


def getPlazoMese(edad, primera_vivienda):
    if int(edad) >= 55:
        return 196
    elif primera_vivienda == "NO":
        return 240
    return 300




def getIngresoSoloTerceraCategoria(ingreso_primera_categoria, ingreso_segunda_categoria,ingreso_tercera_categoria , ingreso_cuarta_categoria,ingreso_quinta_categoria ):
    
    if ingreso_tercera_categoria > 0 and all(x == 0 for x in [ingreso_primera_categoria, ingreso_segunda_categoria, ingreso_cuarta_categoria, ingreso_quinta_categoria]):       
        return "SI"  
    
    return "NO" 




def getPorcentajeCuotaInicial(ingreso_solo_tercera_categoria, residencia,valor_porcentaje_inicial ):
        if ingreso_solo_tercera_categoria=="SI" or residencia=="Extranjero":
            return 0.3

        return valor_porcentaje_inicial




def getMontoFinanciado(precio,tipo_moneda, BONO, MONTO_INICAL):
                    
                precio_real=getPrecioReal(precio, tipo_moneda)

                return  precio_real-BONO-MONTO_INICAL
    




def getMontoIncial(precio, tipo_moneda, cuota_inicial, valor_porcentaje_inicial):
                
                precio_real=getPrecioReal(precio, tipo_moneda)

                # Multiplicación
                monto_financiamiento_inicial = valor_porcentaje_inicial * precio_real

                # Evaluar la condición final y obtener el resultado
                if monto_financiamiento_inicial < cuota_inicial:
                    resultado_final = cuota_inicial
                else:
                    resultado_final = monto_financiamiento_inicial
            
                return resultado_final
            
            
def getBono(precio, tipo_moneda, primera_vivienda):
    
                limite_precio_bono_verde_primero=239800
                limite_precio_bono_verde_segundo=355100
                
                bono_verde_primero=26500
                bono_verde_segundo=13600


                # Evaluar la condición del BONO
                precio_real=getPrecioReal(precio, tipo_moneda)
                    
                # Evaluar la primera condición
                if primera_vivienda == "SÍ" and precio_real <= limite_precio_bono_verde_primero:
                    BONO = bono_verde_primero
                else:
                    # Evaluar la segunda condición `SI`
                    if primera_vivienda == "SÍ" and precio_real <= limite_precio_bono_verde_segundo:
                        BONO = bono_verde_segundo
                    else:
                        BONO = 0

                # print("BONO:", BONO)
                
                return BONO



def getDepasAprobados(resultadoDepartamentos,ingreso_solo_tercera_categoria,residencia,primera_vivienda, cuota_inicial, context, min_value):
            proyectos = Proyecto.objects.filter(web=True, slug="canada")

            for proyecto in proyectos:
                
                
                valor_porcentaje_inicial_real=getPorcentajeCuotaInicial(ingreso_solo_tercera_categoria, residencia,proyecto.valor_porcentaje_inicial )
        
                departamentos= Departamento.objects.filter(
                proyecto_id=proyecto.id,
                estatus="disponible")
                
                for depa in departamentos:
     
                    BONO= getBono(depa.precio_venta, depa.tipo_moneda, primera_vivienda)
                    MONTO_INICAL=getMontoIncial(depa.precio_venta, depa.tipo_moneda, cuota_inicial, valor_porcentaje_inicial_real)
                    MONTO_FINANCIADO = getMontoFinanciado(depa.precio_venta,depa.tipo_moneda,BONO, MONTO_INICAL)
                    
                         
                    for resu in context:
                             
                        if  proyecto.banco in resu and cuota_inicial>=MONTO_INICAL and float(resu[proyecto.banco]) >=float(MONTO_FINANCIADO) :
                           
                            resultadoDepartamentos.append({
                                "nro_depa":depa.nro_depa,
                                "proyecto":proyecto.nombre,
                                "precio": depa.precio_venta,
                                "bono": BONO,
                                "monto_inicial": MONTO_INICAL,
                                "monto_financiado": MONTO_FINANCIADO
                            })
                         
                            print(resu[proyecto.banco])
                            


                        
                    if  proyecto.banco=="todos" and cuota_inicial>=MONTO_INICAL:

                        if float(min_value[0]) >= float(MONTO_FINANCIADO):
                            resultadoDepartamentos.append({
                            "nro_depa":depa.nro_depa,
                            "proyecto":proyecto.nombre,
                            "precio": depa.precio_venta,
                            "bono": BONO,
                            "monto_inicial": MONTO_INICAL,
                            "monto_financiado": MONTO_FINANCIADO
                        })
                        
                            print(depa)
                            
            return resultadoDepartamentos