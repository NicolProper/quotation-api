import datetime
import json
import re
import numpy_financial as npf
from django.http import HttpResponse, JsonResponse
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import requests
import unidecode

from informacion.models import Bancaria
from .models import Departamento
from .serializers import DepartamentoSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from proyects.models import Proyecto
from financiamiento.models import Cliente
from .filters import DepartamentoFilter, DepartamentoFilter2
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .filters import DepartamentoFilter
import xlwings as xw
from django.db import models

from datetime import date, timedelta
from django.db.models import F, Case, When, FloatField, Value
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
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

def calculate_cell_value(cell_value, dataIngresos, plazo, tasa, total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor):
    constants = [
                    [ 'bcp', 'ibk', 'bbva', 'pichincha', 'banbif', 'scotiabank'],
                    [ 1, 0.2, 1, 1, 1, 1],
                    [ 0, 0, 0, 0, 0, 0],
                    [ 1, 0, 0, 0, 0, 0],
                    [ 1, 1, 1, 1, 1, 1],
                    [ 1, 1, 1, 1, 1, 1],
                    [ valor_porcentaje_endeudamiento, valor_porcentaje_endeudamiento, valor_porcentaje_endeudamiento, valor_porcentaje_endeudamiento, valor_porcentaje_endeudamiento, valor_porcentaje_endeudamiento],
                    [ 0, 0, 0, 0, 0, 0]

                ]
   
    
    position=constants[0].index(cell_value)
    data={}
    
    data_ingreso=0
    for index, (x, ingreso) in  enumerate(zip(constants, dataIngresos)):
        print("index", index)
        if index==0:
            data[x[position]]=0
            # print(x[position])
        elif index==1 or index==2 or index==3 or index==4 or index==5:
            data[cell_value]+= float(x[position])*float(ingreso)
            data_ingreso+=float(x[position])*float(ingreso)
        elif index==6:
             data[cell_value]= data[cell_value]*float(x[position])
        elif index==7:
             print("ingreso", ingreso)
             capacidad_endeudamiento=data[cell_value]
             cuota_maxima=data[cell_value]-total_deudas
             data[cell_value]-= float(ingreso)
             


    tasa_mensual = tasa / 12

    
    cuota_mensual = -npf.pv(rate=tasa_mensual, nper=plazo, pmt=data[cell_value])
    real_value=  cuota_mensual if  cuota_mensual > 0 else 0
# return vpn
        
            
            
    print({cell_value:{"financiamiento":real_value, "data_ingreso": data_ingreso, "capacidad_endeudamiento": capacidad_endeudamiento, "total_deudas": total_deudas, "cuota_maxima":cuota_maxima, "interes": tasa, "plazo_meses": plazo }})
    
    nuevo_financiamiento=Cliente(fecha=datetime.date.today(), 
                                             nombre=nombre, apellido=apellido, dni=dni, 
                                             ingresos=data_ingreso,
                                             deudas=total_deudas, tasa_interes=tasa, plazo_meses=plazo, valor_porcentaje_inicial=valor_porcentaje_inicial,valor_porcentaje_capacidad_deuda=valor_porcentaje_endeudamiento,
                                             banco=cell_value,
                                             financiamiento_max=round(real_value, 2),
                                             asesor=asesor
                                             )
    
    print('nuevo_financiamiento')
    print(nuevo_financiamiento)
            
    nuevo_financiamiento.save()
    

    return {cell_value:{"financiamiento":real_value, "data_ingreso": data_ingreso, "capacidad_endeudamiento": capacidad_endeudamiento, "total_deudas": total_deudas, "cuota_maxima":cuota_maxima, "interes": tasa, "plazo_meses": plazo }}
    
    
    
    
    
    
class ClientePostgres(models.Model):
    id= models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipodoc = models.CharField(max_length=100)

    nrodoc = models.CharField(max_length=10)
    email = models.IntegerField()
    edadrango = models.CharField(max_length=100)
    nrocelular = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'cliente'
        managed = False  # Indica que Django no debería gestionar (crear, modificar) esta tabla

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    
def match_user_by_DNI(dni):
    try:
        print(dni)
        # Realiza la consulta a la base de datos secundaria
        usuario = ClientePostgres.objects.using('postgres').filter(nrodoc=dni).first()
        
        # Verifica si se encontraron usuarios
        if not usuario:
            usuario_new = Bancaria.objects.filter(dni=dni).first()
            
            return {
                'nombre':  usuario_new.nombre,
                'apellido': usuario_new.apellido,
                'dni': usuario_new.dni,
                "email": ''
                }
        
        # Crea una lista para almacenar los datos de los usuarios
        usuarios_data = []
        print(usuario)
        # for usuario in usuarios:
        usuarios_data={
                'nombre': usuario.nombre  if usuario.nombre is not None else '',
                'apellido': usuario.apellido  if usuario.apellido is not None else '',
                'dni': usuario.nrodoc if usuario.nrodoc is not None else '',
                "email": usuario.email if usuario.email is not None else ''
            }
        
        # Devuelve la lista de usuarios como una respuesta JSON
        return  usuarios_data

    except Exception as e:
        print(e)
        return {
                'nombre':  '',
                'apellido': '',
                'dni': '',
                "email": ''
                }
    
    
    
@api_view(['POST'])
def get_score_crediticio(request):
    if request.method == 'POST':
        try:


            data_ = request.body
            data = json.loads(data_)

            
            nombre= data.get('nombre')
            apellido= data.get('apellido')
            asesor= data.get('asesor')
            dni=data.get('dni')
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
            plazo_meses=data.get('plazo_meses')
            valor_porcentaje_inicial= data.get('valor_porcentaje_inicial')
            valor_porcentaje_endeudamiento= data.get('valor_porcentaje_endeudamiento')
            total_deudas=0
            
            print(00)
           
            #¿INGRESO SOLO 3ER CATEGORIA?        
            # ingreso_solo_tercera_categoria= getIngresoSoloTerceraCategoria(ingreso_primera_categoria, ingreso_segunda_categoria,ingreso_tercera_categoria , ingreso_cuarta_categoria,ingreso_quinta_categoria)
            
            # TOTAL DEUDAS
            total_deudas=total_deudas + cuota_hipotecaria 
            # + cuota_vehicular+cuota_personal + cuota_tarjeta_credito
               
            # EDAD
            # plazo_meses= getPlazoMese(edad, primera_vivienda)

 
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
      
            
            BCP = calculate_cell_value('bcp', dataIngresos, plazo_meses, tasa,total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor)
            IBK = calculate_cell_value('ibk',dataIngresos, plazo_meses, tasa, total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor)
            BBVA = calculate_cell_value('bbva', dataIngresos, plazo_meses, tasa,total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor)
            PICHINCHA = calculate_cell_value('pichincha', dataIngresos, plazo_meses, tasa, total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor)
            BANBIF = calculate_cell_value('banbif', dataIngresos, plazo_meses, tasa, total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor)
            SCOTIABANK = calculate_cell_value('scotiabank', dataIngresos, plazo_meses, tasa, total_deudas, valor_porcentaje_endeudamiento, nombre, apellido, dni, valor_porcentaje_inicial,asesor)
            
            print(BCP)
            
            context = [
                {"bcp": BCP['bcp']['financiamiento']},
                {"ibk":IBK['ibk']['financiamiento']},
                {"bbva":BBVA['bbva']['financiamiento']},
                {"pichincha":PICHINCHA['pichincha']['financiamiento']},
                {"banbif":BANBIF['banbif']['financiamiento']},
                {"scotiabank":SCOTIABANK['scotiabank']['financiamiento']},
            ]
            
 
            # for data in context:

                 
            

            
            
            dataTable=[
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
            resultadoAllDepartamentos=[]
            
            # resultado_final=getDepasAprobados(resultadoDepartamentos,ingreso_solo_tercera_categoria,residencia,primera_vivienda, cuota_inicial, context, min_value)           
            resultado_final= getDepasAprobados(resultadoDepartamentos,valor_porcentaje_inicial,primera_vivienda, cuota_inicial, context, min_value)
            print(resultadoDepartamentos)
            
            resultado_all_departamentos= getAllDepartamentos(resultadoAllDepartamentos,valor_porcentaje_inicial,primera_vivienda, cuota_inicial, context, min_value)
            print(resultadoDepartamentos)
                        
            cliente_info= match_user_by_DNI(dni)
            print("cliente______________________info")
            print(cliente_info)
            return JsonResponse({ "size":len(resultado_final),"bancos":context , "data":resultado_final,"data_table":dataTable, "allData":resultado_all_departamentos, "cliente": cliente_info },safe=False)
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




# def getIngresoSoloTerceraCategoria(ingreso_primera_categoria, ingreso_segunda_categoria,ingreso_tercera_categoria , ingreso_cuarta_categoria,ingreso_quinta_categoria ):
    
#     if ingreso_tercera_categoria > 0 and all(x == 0 for x in [ingreso_primera_categoria, ingreso_segunda_categoria, ingreso_cuarta_categoria, ingreso_quinta_categoria]):       
#         return "SI"  
    
#     return "NO" 




# def getPorcentajeCuotaInicial(ingreso_solo_tercera_categoria, residencia,valor_porcentaje_inicial, primera_vivienda ):
#         if ingreso_solo_tercera_categoria=="SI" or residencia=="Extranjero":
#             return 0.3
#         elif primera_vivienda=="NO":
#             return 0.15

#         return valor_porcentaje_inicial




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



def getDepasAprobados(resultadoDepartamentos,valor_porcentaje_inicial,primera_vivienda, cuota_inicial, context, min_value):
            proyectos = Proyecto.objects.filter(Q(web=True) | Q(nombre="parodi"))

            print(proyectos)
            for proyecto in proyectos:
                
                
                # valor_porcentaje_inicial_real=getPorcentajeCuotaInicial(ingreso_solo_tercera_categoria, residencia,proyecto.valor_porcentaje_inicial , primera_vivienda)
                valor_porcentaje_inicial_real =valor_porcentaje_inicial if valor_porcentaje_inicial >= proyecto.valor_porcentaje_inicial else proyecto.valor_porcentaje_inicial
                departamentos= Departamento.objects.filter(
                proyecto_id=proyecto.id,
                ocultar=False,

                estatus="disponible")
                
                for depa in departamentos:
     
                    BONO= getBono(depa.precio_venta, depa.tipo_moneda, primera_vivienda)
                    MONTO_INICAL=getMontoIncial(depa.precio_venta, depa.tipo_moneda, cuota_inicial, valor_porcentaje_inicial_real)
                    MONTO_FINANCIADO = getMontoFinanciado(depa.precio_venta,depa.tipo_moneda,BONO, MONTO_INICAL)
                    
                         
                    for resu in context:
                             
                        if  proyecto.banco in resu and cuota_inicial>=MONTO_INICAL and float(resu[proyecto.banco]) >=float(MONTO_FINANCIADO) :
                            precio= depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta
                            sumatoria=cuota_inicial+BONO+float(resu[proyecto.banco])
                            resultadoDepartamentos.append({
                                "nro_depa":depa.nro_depa,
                                "proyecto":proyecto.nombre,
                                "precio": depa.precio_venta,
                                "tipo_moneda": depa.tipo_moneda,
                                "cuota_inicial": cuota_inicial,
                                "max_financiamiento": resu[proyecto.banco],
                                "precio_real": depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta ,
                                "porcentaje": sumatoria/precio,
                                "bono": BONO,
                                "monto_inicial": MONTO_INICAL ,
                                "monto_financiado": MONTO_FINANCIADO,
                                "id": depa.id
                            })
                         
                            print(resu[proyecto.banco])
                            


                        
                    if  proyecto.banco=="todos" and cuota_inicial>=MONTO_INICAL:

                        if float(max(min_value)) >= float(MONTO_FINANCIADO):
                            precio2=depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta
                            sumatoria2=cuota_inicial+BONO+float(max(min_value))                            
                            resultadoDepartamentos.append({
                            "nro_depa":depa.nro_depa,
                            "proyecto":proyecto.nombre,
                            "precio": depa.precio_venta,
                            "tipo_moneda": depa.tipo_moneda,
                            "cuota_inicial": cuota_inicial,
                            "max_financiamiento": float(max(min_value))  ,

                            "precio_real": depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta ,
                            "porcentaje": sumatoria2/precio2,
                            "bono": BONO,
                            "monto_inicial": MONTO_INICAL,
                            "monto_financiado": MONTO_FINANCIADO,
                            "id": depa.id

                        })
                        
                            print(depa)
                            
            return resultadoDepartamentos
        

def getAllDepartamentos(resultado_all_departamentos,valor_porcentaje_inicial,primera_vivienda, cuota_inicial, context, min_value):
            proyectos = Proyecto.objects.filter(Q(web=True) | Q(nombre="parodi"))

            print(proyectos)
            for proyecto in proyectos:
                
                
                # valor_porcentaje_inicial_real=getPorcentajeCuotaInicial(ingreso_solo_tercera_categoria, residencia,proyecto.valor_porcentaje_inicial , primera_vivienda)
                valor_porcentaje_inicial_real =valor_porcentaje_inicial if valor_porcentaje_inicial >= proyecto.valor_porcentaje_inicial else proyecto.valor_porcentaje_inicial
                departamentos= Departamento.objects.filter(
                proyecto_id=proyecto.id,
                ocultar=False,
                estatus="disponible")
                
                for depa in departamentos:
     
                    BONO= getBono(depa.precio_venta, depa.tipo_moneda, primera_vivienda)
                    MONTO_INICAL=getMontoIncial(depa.precio_venta, depa.tipo_moneda, cuota_inicial, valor_porcentaje_inicial_real)
                    MONTO_FINANCIADO = getMontoFinanciado(depa.precio_venta,depa.tipo_moneda,BONO, MONTO_INICAL)
                    
                         
                    for resu in context:
                             
                        if  proyecto.banco in resu :
                            
                            precio=depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta 
                            sumatoria=cuota_inicial+BONO+float(resu[proyecto.banco])
                           
                            resultado_all_departamentos.append({
                                "nro_depa":depa.nro_depa,
                                "proyecto":proyecto.nombre,
                                "precio": depa.precio_venta,
                                "tipo_moneda": depa.tipo_moneda,
                                "cuota_inicial": cuota_inicial,
                                "max_financiamiento": float(resu[proyecto.banco])  ,

                                "precio_real": precio ,
                                "porcentaje": sumatoria/precio,
                                "bono": BONO,
                                "monto_inicial": MONTO_INICAL,
                                "monto_financiado": MONTO_FINANCIADO,
                                "id": depa.id
                            })
                         
                            print(resu[proyecto.banco])
                            


                        
                    if  proyecto.banco=="todos":

                        # if float(min_value[0]) >= float(MONTO_FINANCIADO):
                            precio2=depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta 
                            sumatoria2=cuota_inicial+BONO+float(max(min_value))
                            resultado_all_departamentos.append({
                            "nro_depa":depa.nro_depa,
                            "proyecto":proyecto.nombre,
                            "precio": depa.precio_venta,
                            "tipo_moneda": depa.tipo_moneda,
                            "cuota_inicial": cuota_inicial,
                            "max_financiamiento": float(max(min_value))  ,

                            "precio_real": depa.precio_venta*3.8 if depa.tipo_moneda =="usd" else depa.precio_venta ,
                            "porcentaje": sumatoria2/precio2,
                            "bono": BONO,
                            "monto_inicial": MONTO_INICAL,
                            "monto_financiado": MONTO_FINANCIADO,
                            "id": depa.id

                        })
                        
                            print(depa)
                            
            return resultado_all_departamentos
        
            
        
def getFecha(depa:Departamento):

    # nueva_fecha = fecha_actual - relativedelta(months=1)
    
    if depa.proyecto.etapa=="inmediata":
        return date.today().replace(day=1)

    elif  depa.proyecto.etapa=="planos" or depa.proyecto.etapa=="construccion" or depa.proyecto.etapa=="preventa":
        return depa.proyecto.fecha_entrega - relativedelta(months=1)
    
    else:
        return depa.proyecto.fecha_entrega
    
@api_view(['GET'])
def info_departamento_proyecto_analyzer(reques, idDepartamento, idCliente, tasa, plazoMeses, porcentajeInicial):
    print('ingrese')
    departamento = Departamento.objects.get(id=idDepartamento)
    cliente=Bancaria.objects.get(id=idCliente)
    print(cliente.cuota_inicial)
    print(departamento.precio_venta)
    print(departamento.proyecto.valor_porcentaje_inicial)
   # Obtener la fecha actual

    
    departamento_data = {
        "proyecto": departamento.proyecto.nombre.upper(),
        "nombre_proyecto": departamento.proyecto.nombre,
        "etapa":  departamento.proyecto.etapa,
        "idProyecto":  str(departamento.proyecto.id),
        "tipologia":  departamento.tipo_departamento,
        "numero_depa":  departamento.nombre,
        "valor_inmueble":departamento.precio_venta if departamento.tipo_moneda=="pen" else departamento.precio_venta*3.8, #update
        "tipo_moneda": departamento.tipo_moneda,
        "precio_lista": departamento.precio,
        "inicial_porc": porcentajeInicial if porcentajeInicial >= departamento.proyecto.valor_porcentaje_inicial*100 else departamento.proyecto.valor_porcentaje_inicial*100 , #update
        "fecha_entrega":  date.today().replace(day=1)  if departamento.proyecto.etapa =="inmediata"  else  departamento.proyecto.fecha_entrega,
        "alcabala": 'no',
        "apreciacion_anual_porc": 2,
        "costo_administracion_porc": 0,
        "meses_de_gracia": 0,
        "renta_mensual": departamento.valor_alquiler,
        "seguro_desgravamen_mensual_porc": 0.0281,
        "meses_dobles": {
            "mes1": "-1",
            "mes2": "-1"
        },
        "seguro_todo_riesgo_mensual_porc": 0.02,
        "fecha_del_prestamo": getFecha(departamento),
        "tamanio_m2":departamento.unit_area,
        "nro_habitaciones": departamento.nro_dormitorios,
        "nro_banos": departamento.nro_banos,
        "url": "https://proyects-image.s3.us-east-2.amazonaws.com/" + departamento.proyecto.slug + "/tipologias/" + departamento.tipo_departamento.upper() + ".jpg",
        
        "nro_depa": departamento.nro_depa,

        "corretaje": 'si' if departamento.proyecto.corretaje else "no",
        "tasa_int_credito_hip_porc": tasa*100 ,#update
        "descuento_preventa_porc": departamento.proyecto.descuento_porcentaje_preventa*100,
        "plazo_en_meses_cred_hip": plazoMeses, #update
        "costo_instalar_porc": departamento.proyecto.costo_porcentaje_instalacion*100,
        "capex_reparaciones_anual_porc": departamento.proyecto.costo_porcentaje_capex_reparaciones*100,
        "vista": departamento.vista,
        "piso": departamento.piso,


        "vacancia_dias_anio": departamento.proyecto.dias_vacancia,
        "costo_operacional_prom_porc":departamento.proyecto.costo_porcentaje_operativo*100,
        "costo_de_administracion_porc":departamento.proyecto.costo_porcentaje_administrativo*100,
        "costos_administrativos_venta_porc":departamento.proyecto.costo_porcentaje_administrativos_venta*100

        }
        # departamentos_data.append(departamento_data)
    
    # Devolver los departamentos como JSON
    return Response({'data': departamento_data})
    
@api_view(['GET'])
def getAllDepas(request):
    Depas = (Departamento.objects
             .filter(estatus="disponible")
             .select_related('proyecto')
             .annotate(
                 proyecto_nombre=F('proyecto__nombre'),
                 precio_real=Case(
                     When(tipo_moneda="usd", then=F('precio_venta') * Value(3.8)),
                     default=F('precio_venta'),
                     output_field=FloatField()
                 )
             )
             .values(
                 'nro_depa',
                 'proyecto_nombre',
                 'precio_venta',
                 'tipo_moneda',
                 'precio_real',
                 'id'
             ))

    return Response({'data': list(Depas)})


@api_view(['GET'])
def get_nro_depas_by_project(request, slug):
    try:
        # Filtrar el proyecto por slug
        proyecto = Proyecto.objects.filter(slug=slug).first()
        
        if proyecto:
            # Obtener solo los nro_depa de los departamentos asociados al proyecto
            nro_depas = Departamento.objects.filter(proyecto=proyecto).values_list('nro_depa', flat=True)
            
            return Response({'data': list(nro_depas)}, status=200)
        else:
            return Response({'message': 'Proyecto no encontrado', "data":[]}, status=404)
    
    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error al obtener los departamentos',"data":[]}, status=500)


def analyze_api(tasa_credito, newprecio, valor_alquiler, unit_area, valor_porcentaje_inicial, fecha_entrega_updated, costo_porcentaje_instalacion, descuento_porcentaje_preventa, costo_porcentaje_operativo, costo_porcentaje_administrativo, corretaje, plazo_meses, dias_vacancia, costo_porcentaje_capex_reparaciones, costo_porcentaje_administrativos_venta, etapa, tipo_moneda):
    url = 'https://8sv61pfob7.execute-api.us-east-2.amazonaws.com/develop/calculate'
    data_to_send = {
        "configOri": {
            "proyecto": 'proyecto',
            "etapa": etapa,
            "tipologia": '',
            "numero_depa": '',
            "valor_inmueble": round(newprecio),
            "inicial_porc": valor_porcentaje_inicial * 100,
            "fecha_entrega": date.today().replace(day=1).isoformat() if etapa == "inmediata" else fecha_entrega_updated.isoformat(),
            "alcabala": 'no',
            "apreciacion_anual_porc": 3,
            "costo_administracion_porc": 0,
            "meses_de_gracia": 0,
            "renta_mensual": valor_alquiler,
            "seguro_desgravamen_mensual_porc": 0.0281,
            "meses_dobles": {
                "mes1": "-1",
                "mes2": "-1"
            },
            "seguro_todo_riesgo_mensual_porc": 0.02,
            "fecha_del_prestamo": date.today().replace(day=1).isoformat() if etapa == "inmediata" else (fecha_entrega_updated - relativedelta(months=1)).isoformat(),
            "tamanio_m2": unit_area,
            "nro_habitaciones": 0,
            "nro_banos": 0,
            "url": "https://proyects-image.s3.us-east-2.amazonaws.com/",
            "corretaje": 'si' if corretaje else "no",
            "tasa_int_credito_hip_porc": tasa_credito * 100,
            "descuento_preventa_porc": descuento_porcentaje_preventa * 100,
            "plazo_en_meses_cred_hip": plazo_meses,
        },
        "constantsOri": {
            "dia_pago_elegido": 8,
            "total_meses": 360,
            "factor_de_ajuste": 0.999846868287209,
            "incremento_alquiler_anual_porc": 2,
            "costo_operacional_personalizado_soles": 0,
            "capex_reparaciones_personalizado_soles": 0,
            "costo_de_administracion_personalizado_soles": 0,
            "duracion_promedio_contrato_alquiler_meses": 24,
            "costos_de_salida_personalizado_soles": 0,
            "capex_reparaciones_anual_porc": costo_porcentaje_capex_reparaciones * 100,
            "vacancia_dias_anio": dias_vacancia,
            "costo_operacional_prom_porc": costo_porcentaje_operativo * 100,
            "costo_de_administracion_porc": costo_porcentaje_administrativo * 100,
            "costos_administrativos_venta_porc": costo_porcentaje_administrativos_venta * 100,
            "costo_instalar_porc": costo_porcentaje_instalacion * 100,
            "tipo_moneda": tipo_moneda,
        }
    }
    
    response = requests.post(url, json=data_to_send)
    
    if response.status_code == 200:
        return response.json()
    else:
        print('Error en la solicitud POST:', response.status_code)
        return {}



def ocultarDef(data):
    if not pd.isna(data):
        return True  if data.lower() =="ocultar" else False
    else: 
        return None

@api_view(['POST'])
def upload_data_department(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            fecha_actualizacion = data.get('fecha_actualizacion') if not pd.isna(data.get('fecha_actualizacion')) else None

            proyecto = data.get('proyecto').lower() if not pd.isna(data.get('proyecto')) else None
            tipo_inventario = data.get('tipo_inventario') if not pd.isna(data.get('tipo_inventario')) else None

            nro_depa = str(data.get('nro_depa')) if not pd.isna(data.get('nro_depa')) else None
            nombre = nro_depa
            tipo_moneda = data.get('tipo_moneda').lower() if not pd.isna(data.get('tipo_moneda')) else None
            precio = data.get('precio') if not pd.isna(data.get('precio')) else None
            precio_venta = data.get('precio_venta') if not pd.isna(data.get('precio_venta')) else None
            nro_dormitorios = data.get('nro_dormitorios') if not pd.isna(data.get('nro_dormitorios')) else None
            nro_banos = data.get('nro_banos') if not pd.isna(data.get('nro_banos')) else None
            valor_alquiler = data.get('valor_alquiler') if not pd.isna(data.get('valor_alquiler')) else None
            unit_area = data.get('unit_area') if not pd.isna(data.get('unit_area')) else None
            vista = data.get('vista').lower() if not pd.isna(data.get('vista')) else None
            piso = data.get('piso') if not pd.isna(data.get('piso')) else None
            tipo_departamento = data.get('tipo_departamento') if not pd.isna(data.get('tipo_departamento')) else None
            estatus = data.get('estatus').lower() if not pd.isna(data.get('estatus')) else None
            ocultar = ocultarDef(data.get('ocultar'))

            precio_workshop = 0
            valor_descuento_preventa = 0

            tir_ = 0
            roi_ = 0
            valor_cuota_ = 0
            renta_ = 0
            patrimonio_inicial_ = 0
            patrimonio_anio_5_ = 0
            patrimonio_anio_10_ = 0
            patrimonio_anio_20_ = 0
            patrimonio_anio_30_ = 0

            proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
            fecha_entrega_updated = datetime.date.today().replace(day=1) if proyecto_obj and proyecto_obj.etapa == "inmediata" else proyecto_obj.fecha_entrega if proyecto_obj else None

            if proyecto_obj and precio and valor_alquiler and unit_area and proyecto_obj.valor_porcentaje_inicial and fecha_entrega_updated:
                newprecio = precio * 3.8 if tipo_moneda == "usd" else precio
                precio_dolar = precio if tipo_moneda == "usd" else 0

                data = analyze_api(
                    proyecto_obj.tasa_credito, newprecio, valor_alquiler, unit_area, proyecto_obj.valor_porcentaje_inicial, 
                    fecha_entrega_updated, proyecto_obj.costo_porcentaje_instalacion, proyecto_obj.descuento_porcentaje_preventa, 
                    proyecto_obj.costo_porcentaje_operativo, proyecto_obj.costo_porcentaje_administrativo, proyecto_obj.corretaje, 
                    proyecto_obj.plazo_meses, proyecto_obj.dias_vacancia, proyecto_obj.costo_porcentaje_capex_reparaciones, 
                    proyecto_obj.costo_porcentaje_administrativos_venta,
                    proyecto_obj.etapa, tipo_moneda)
                
                print(data)
                
                print(data['resultado'])

                tir_ = round(data['resultado']['tir'], 8)
                roi_ = round(data['resultado']['roi'], 8)
                renta_ = round(data['resultado']['renta'], 8)
                valor_cuota_ = round(data['resultado']['valor_cuota'], 8)
                patrimonio_inicial_ = round(data['resultado']['patrimonio_inicial'], 8)
                patrimonio_anio_5_ = round(data['resultado']['patrimonio_anio_5'], 8)
                patrimonio_anio_10_ = round(data['resultado']['patrimonio_anio_10'], 8)
                patrimonio_anio_20_ = round(data['resultado']['patrimonio_anio_20'], 8)
                patrimonio_anio_30_ = round(data['resultado']['patrimonio_anio_30'], 8)

            fields = {
                'ocultar':ocultar,
                'nombre': nombre,
                "fecha_actualizacion": fecha_actualizacion,
                "estatus": estatus,
                'nro_depa': nro_depa,
                'unit_area': unit_area,
                'nro_dormitorios': nro_dormitorios,
                'nro_banos': nro_banos,
                'valor_alquiler': valor_alquiler,
                'piso': piso,
                'vista': vista,
                'precio': newprecio,
                "precio_venta":precio_venta,
                "precio_dolar": precio_dolar,
                'precio_workshop': precio_workshop,
                'valor_descuento_preventa': valor_descuento_preventa,
                'tipo_moneda': tipo_moneda,
                "tipo_departamento": tipo_departamento,
                "tipo_inventario": tipo_inventario,
                'patrimonio_inicial': patrimonio_inicial_,
                "patrimonio_anio_5": patrimonio_anio_5_,
                "patrimonio_anio_10": patrimonio_anio_10_,
                'patrimonio_anio_20': patrimonio_anio_20_,
                'patrimonio_anio_30': patrimonio_anio_30_,
                "tir": tir_,
                "roi": roi_,
                "valor_cuota": valor_cuota_,
                "renta": renta_
            }

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            def parse_date(date_str):
                if isinstance(date_str, str):
                    try:
                        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
                return date_str

            if fields_not_none:
                if tipo_inventario == "proyecto":
                    proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                    
                    if proyecto_obj:
                        nro_depa = fields_not_none.get('nro_depa')
                        existing_department = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto_obj).first()
                        
                        if existing_department:
                            updated_fields = {}
                            for key, value in fields_not_none.items():
                                old_value = getattr(existing_department, key)
                                if isinstance(old_value, str) and isinstance(value, str):
                                    old_value = old_value.lower()
                                    value = value.lower()
                                elif key == "fecha_actualizacion":
                                    # Parse both dates to datetime.date for comparison
                                    old_value = parse_date(old_value)
                                    value = parse_date(value)
                                if old_value != value:
                                    updated_fields[key] = {'old': old_value, 'new': value}
                                    setattr(existing_department, key, value)
                            existing_department.save()
                            return Response({'message': 'Departamento actualizado con éxito', 'updated_fields': updated_fields, "nro_depa":existing_department.nro_depa, "proyecto":existing_department.proyecto.nombre, "isUpdated":True if len(updated_fields)>0 else False  }, status=200)
                        else:
                            departamento = Departamento.objects.create(proyecto=proyecto_obj, **fields_not_none)
                            return Response({'message': 'Departamento creado con éxito',"nro_depa":departamento.nro_depa, "proyecto":departamento.proyecto.nombre, "isUpdated":False }, status=200)

            return Response({'message': 'Data processed successfully'}, status=200)

        except Exception as e:
            print(f'error: {e}')
            return Response({'message': 'Error on file upload'}, status=400)




@api_view(['POST'])
def edit_data_stock_department(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            fecha_actualizacion = data.get('fecha_actualizacion') if not pd.isna(data.get('fecha_actualizacion')) else None
            proyecto = data.get('proyecto').lower() if not pd.isna(data.get('proyecto')) else None
            nro_depa = data.get('nro_depa') if not pd.isna(data.get('nro_depa')) else None
            estatus = data.get('estatus').lower() if not pd.isna(data.get('estatus')) else None



            fields = {

                "fecha_actualizacion": fecha_actualizacion,
                'nro_depa': nro_depa,
                "estatus":estatus

            }

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            if fields_not_none:
                
                    proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                    
                    if proyecto_obj:
                        nro_depa = fields_not_none.get('nro_depa')
                        existing_department = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto_obj).first()
                        
                        if existing_department:
                            for key, value in fields_not_none.items():
                                setattr(existing_department, key, value)
                            existing_department.save()
                            return Response({'message': 'Departamento actualizado con éxito'}, status=200)

            return Response({'message': 'Data processed successfully'}, status=200)

        except Exception as e:
            print(f'error: {e}')
            return Response({'message': 'Error on file upload'}, status=400)

@api_view(['POST'])
def edit_data_department(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            fecha_actualizacion = data.get('fecha_actualizacion') if not pd.isna(data.get('fecha_actualizacion')) else None

            proyecto = data.get('proyecto').lower() if not pd.isna(data.get('proyecto')) else None
            tipo_inventario = data.get('tipo_inventario') if not pd.isna(data.get('tipo_inventario')) else None

            nro_depa = data.get('nro_depa') if not pd.isna(data.get('nro_depa')) else None
            nombre = nro_depa
            tipo_moneda = data.get('tipo_moneda').lower() if not pd.isna(data.get('tipo_moneda')) else None
            precio = data.get('precio') if not pd.isna(data.get('precio')) else None
            precio_venta = data.get('precio_venta') if not pd.isna(data.get('precio_venta')) else None
            nro_dormitorios = data.get('nro_dormitorios') if not pd.isna(data.get('nro_dormitorios')) else None
            nro_banos = data.get('nro_banos') if not pd.isna(data.get('nro_banos')) else None
            valor_alquiler = data.get('valor_alquiler') if not pd.isna(data.get('valor_alquiler')) else None
            unit_area = data.get('unit_area') if not pd.isna(data.get('unit_area')) else None
            vista = data.get('vista').lower() if not pd.isna(data.get('vista')) else None
            piso = data.get('piso') if not pd.isna(data.get('piso')) else None
            tipo_departamento = data.get('tipo_departamento') if not pd.isna(data.get('tipo_departamento')) else None
            ocultar = ocultarDef(data.get('ocultar'))
            precio_workshop = 0
            valor_descuento_preventa = 0

            tir_ = 0
            roi_ = 0
            valor_cuota_ = 0
            renta_ = 0
            patrimonio_inicial_ = 0
            patrimonio_anio_5_ = 0
            patrimonio_anio_10_ = 0
            patrimonio_anio_20_ = 0
            patrimonio_anio_30_ = 0

            proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
            fecha_entrega_updated = datetime.date.today().replace(day=1) if proyecto_obj and proyecto_obj.etapa == "inmediata" else proyecto_obj.fecha_entrega if proyecto_obj else None

            if proyecto_obj and precio and valor_alquiler and unit_area and proyecto_obj.valor_porcentaje_inicial and fecha_entrega_updated:
                newprecio = precio * 3.8 if tipo_moneda == "usd" else precio
                precio_dolar = precio if tipo_moneda == "usd" else 0

                data = analyze_api(
                    proyecto_obj.tasa_credito, newprecio, valor_alquiler, unit_area, proyecto_obj.valor_porcentaje_inicial, 
                    fecha_entrega_updated, proyecto_obj.costo_porcentaje_instalacion, proyecto_obj.descuento_porcentaje_preventa, 
                    proyecto_obj.costo_porcentaje_operativo, proyecto_obj.costo_porcentaje_administrativo, proyecto_obj.corretaje, 
                    proyecto_obj.plazo_meses, proyecto_obj.dias_vacancia, proyecto_obj.costo_porcentaje_capex_reparaciones, 
                    proyecto_obj.costo_porcentaje_administrativos_venta,
                    proyecto_obj.etapa, tipo_moneda)
                
                print(data['resultado'])

                tir_ = round(data['resultado']['tir'], 8)
                roi_ = round(data['resultado']['roi'], 8)
                renta_ = round(data['resultado']['renta'], 8)
                valor_cuota_ = round(data['resultado']['valor_cuota'], 8)
                patrimonio_inicial_ = round(data['resultado']['patrimonio_inicial'], 8)
                patrimonio_anio_5_ = round(data['resultado']['patrimonio_anio_5'], 8)
                patrimonio_anio_10_ = round(data['resultado']['patrimonio_anio_10'], 8)
                patrimonio_anio_20_ = round(data['resultado']['patrimonio_anio_20'], 8)
                patrimonio_anio_30_ = round(data['resultado']['patrimonio_anio_30'], 8)

            fields = {
                'ocultar':ocultar,
                'nombre': nombre,
                "fecha_actualizacion": fecha_actualizacion,
                'nro_depa': nro_depa,
                'unit_area': unit_area,
                'nro_dormitorios': nro_dormitorios,
                'nro_banos': nro_banos,
                'valor_alquiler': valor_alquiler,
                'piso': piso,
                'vista': vista,
                'precio': newprecio,
                "precio_venta":precio_venta,
                "precio_dolar": precio_dolar,
                'precio_workshop': precio_workshop,
                'valor_descuento_preventa': valor_descuento_preventa,
                'tipo_moneda': tipo_moneda,
                "tipo_departamento": tipo_departamento,
                "tipo_inventario": tipo_inventario,
                'patrimonio_inicial': patrimonio_inicial_,
                "patrimonio_anio_5": patrimonio_anio_5_,
                "patrimonio_anio_10": patrimonio_anio_10_,
                'patrimonio_anio_20': patrimonio_anio_20_,
                'patrimonio_anio_30': patrimonio_anio_30_,
                "tir": tir_,
                "roi": roi_,
                "valor_cuota": valor_cuota_,
                "renta": renta_
            }

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            if fields_not_none:
                if tipo_inventario == "proyecto":
                    proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                    
                    if proyecto_obj:
                        nro_depa = fields_not_none.get('nro_depa')
                        existing_department = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto_obj).first()
                        
                        if existing_department:
                            for key, value in fields_not_none.items():
                                setattr(existing_department, key, value)
                            existing_department.save()
                            return Response({'message': 'Departamento actualizado con éxito'}, status=200)
                        else:
                            departamento = Departamento.objects.create(proyecto=proyecto_obj, **fields_not_none)
                            return Response({'message': 'Departamento creado con éxito'}, status=201)

            return Response({'message': 'Data processed successfully'}, status=200)

        except Exception as e:
            print(f'error: {e}')
            return Response({'message': 'Error on file upload'}, status=400)


@api_view(['GET'])
def get_info_department_by_nro_depa(request, nro_depa, slug):
    
    try:
        proyecto= Proyecto.objects.filter(slug=slug).first()
        data = Departamento.objects.filter(nro_depa=nro_depa, proyecto=proyecto).first()
        if data:
            obj = {
                "fecha_actualizacion": data.fecha_actualizacion,
                "proyecto": data.proyecto.nombre,
                "tipo_inventario": data.tipo_inventario,
                "nro_depa": data.nro_depa,
                "tipo_moneda": data.tipo_moneda,
                "precio":  round(data.precio_dolar) if data.tipo_moneda == "usd" else  round(data.precio),
                "precio_venta":round(data.precio_venta),
                "nro_dormitorios": data.nro_dormitorios,
                "nro_banos": data.nro_banos,
                "valor_alquiler": round(data.valor_alquiler),
                "unit_area": data.unit_area,
                "vista": data.vista,
                "piso": data.piso,
                "tipo_departamento": data.tipo_departamento,
                "estatus": data.estatus,
                "ocultar":"ocultar" if data.ocultar else "no ocultar",
            }
            return Response({'data': obj}, status=200)
        else:
            return Response({'message': 'Proyecto no encontrado', "data": []}, status=404)
    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error al obtener los departamentos', "data": []}, status=500)
    
    
    
@api_view(['GET'])
def get_typologies_by_project(request, slug):
    try:
        proyecto = Proyecto.objects.filter(slug=slug).first()
        if not proyecto:
            return Response({'message': 'Proyecto no encontrado', "data": []}, status=404)
        
        departments = Departamento.objects.filter(proyecto=proyecto, estatus="disponible").values('tipo_departamento').distinct()
        data=map(lambda x : x['tipo_departamento'], departments)
        # print(list(data))
        return Response({'data': list(data)}, status=200)
        
    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error al obtener los departamentos', "data": []}, status=500)