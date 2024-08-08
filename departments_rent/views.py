
import json
import re
from django.shortcuts import get_object_or_404
import requests
import unidecode
from analyzer.models import Analyzer
# from departments.utils import analyze
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import xlwings as xw
from departments_rent.models import Departamento_Alquiler
from datetime import date, datetime



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

@api_view(['POST'])
def upload_data_excel(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            departamentos_data = pd.read_excel(file)
            list_departments = []
            wb = xw.Book('calc.xlsx')
            for index, row in departamentos_data.iterrows():
                fecha_actualizacion = row['fecha_actualizacion'] if not pd.isna(row['fecha_actualizacion']) else None
                nombre = row['nombre'].lower() if not pd.isna(row['nombre']) else None
                texto_sin_tildes = unidecode.unidecode(nombre)    
                slug =  re.sub(r'\s+', '-', texto_sin_tildes.lower())
                codigo = row['codigo'].lower() if not pd.isna(row['codigo']) else None
                anio_construccion = row['anio_construccion'] if not pd.isna(row['anio_construccion']) else None
                
                distrito = row['distrito'].lower() if not pd.isna(row['distrito']) else None
                tipo_moneda=row['tipo_moneda'].lower() if not pd.isna(row['tipo_moneda']) else None
                tipo_inventario='c/inquilino'

                banco="todos"
                edificio=row['edificio'].lower() if not pd.isna(row['edificio']) else None
                unit_area = row['unit_area'] if not pd.isna(row['unit_area']) else None
                nro_dormitorios =row['nro_dormitorios'] if not pd.isna(row['nro_dormitorios']) else None
                nro_banos = row['nro_banos'] if not pd.isna(row['nro_banos']) else None
                valor_alquiler = row['valor_alquiler'] if not pd.isna(row['valor_alquiler']) else None
                piso = row['piso'] if not pd.isna(row['piso']) else None
                vista = row['vista'].lower() if not pd.isna(row['vista']) else None
                precio = row['precio'] if not pd.isna(row['precio']) else None

                estatus = row['estatus'].lower() if not pd.isna(row['estatus']) else None

                valor_porcentaje_inicial  = row['valor_porcentaje_inicial'] if not pd.isna(row['valor_porcentaje_inicial']) else None
                valor_porcentaje_financiado   = row['valor_porcentaje_financiado'] if not pd.isna(row['valor_porcentaje_financiado']) else None



                areas_comunes =True if row['areas_comunes'] == "SI" else False
                piscina=True if row['piscina'] == "SI" else False
                gym =True if row['gym'] == "SI" else False
                coworking =True if row['coworking'] == "SI" else False
                cine =True if row['cine'] == "SI" else False
                parrilla =True if row['parrilla'] == "SI" else False
                sum =True if row['sum'] == "SI" else False
                bicicleta =True if row['bicicleta'] == "SI" else False
                bar =True if row['bar'] == "SI" else False




                descuento_porcentaje_preventa=row['descuento_porcentaje_preventa'] if not pd.isna(row['descuento_porcentaje_preventa']) else None
                coordenada_A=row['coordenada_A'] if not pd.isna(row['coordenada_A']) else None
                coordenada_B=row['coordenada_B'] if not pd.isna(row['coordenada_B']) else None



                tir_=0
                roi_=0
                valor_cuota_=0
                renta_=0
                patrimonio_inicial_ =  0
                patrimonio_anio_5_ =  0
                patrimonio_anio_10_ =  0
                patrimonio_anio_20_ =  0
                patrimonio_anio_30_ =  0
                
                analyzer=Analyzer.objects.get(id=1)
                fecha_entrega_updated=date.today().replace(day=1)

                if precio and valor_alquiler and unit_area and valor_porcentaje_inicial and fecha_entrega_updated:
                     
                    newprecio= precio*3.8 if tipo_moneda =="usd" else precio
                    precio_dolar= precio if tipo_moneda =="usd" else None

                    
                    data = analyze_api(
                    analyzer.tasa_credito, newprecio, valor_alquiler, unit_area, valor_porcentaje_inicial, 
                    fecha_entrega_updated, analyzer.costo_porcentaje_instalacion, descuento_porcentaje_preventa, 
                    analyzer.costo_porcentaje_operativo, analyzer.costo_porcentaje_administrativo, analyzer.corretaje, 
                    analyzer.plazo_meses, analyzer.dias_vacancia, analyzer.costo_porcentaje_capex_reparaciones, 
                    analyzer.costo_porcentaje_administrativos_venta,
                    "inmediata", tipo_moneda)
                    
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
                    "codigo":codigo,
                    "edificio":edificio,
                    "anio_construccion":anio_construccion,
                    'nombre': nombre,
                    "fecha_actualizacion":fecha_actualizacion,
                    "estatus":estatus,
                    'unit_area': unit_area,
                    'nro_dormitorios': nro_dormitorios,
                    'nro_banos': nro_banos,
                    'valor_alquiler': valor_alquiler,
                    'piso': piso,
                    'vista': vista,
                    'precio': newprecio,
                    "precio_dolar":precio_dolar,
                    'tipo_moneda': tipo_moneda,
                    "tipo_inventario":tipo_inventario,
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
                    "slug":slug,
                    "valor_porcentaje_inicial":valor_porcentaje_inicial,
                    "valor_porcentaje_financiado":valor_porcentaje_financiado,
                    "precio_dolar":precio_dolar,
                    "valor_alquiler": valor_alquiler,
                    "descuento_porcentaje_preventa":descuento_porcentaje_preventa,

                    "coordenada_A":coordenada_A,
                    "coordenada_B":coordenada_B,
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

  # Filtrar los campos que tienen valores diferentes de None
                fields_not_none = {key: value for key, value in fields.items() if value is not None}

                if fields_not_none:
                    if  tipo_inventario == "c/inquilino":

                        nombre_depa = fields_not_none.get('nombre')  # Obtener el número de departamento
                        existing_department = Departamento_Alquiler.objects.filter(nombre=nombre_depa).first()
                        
                        if existing_department:
                            # Si ya existe un departamento con el mismo número y proyecto, actualizar sus campos
                            for key, value in fields_not_none.items():
                                setattr(existing_department, key, value)
                            existing_department.save()
                        else:
                            # Si no existe, crear un nuevo departamento
                            Departamento_Alquiler.objects.create(**fields_not_none)
                            list_departments.append(fields_not_none)

            return Response(list_departments, status=200)

        except Exception as e:
            # print(row)
            print(f'error: {e}')
            return Response({'message': 'Error on file upload'}, status=400)


@api_view(['GET'])
def get_all_entrega_inmediata_web(reques):
    proyectos = Departamento_Alquiler.objects.filter(web=True)
    departamentos_data = []
    for proyecto in proyectos:
        departamentos_data.append(proyecto.slug)
    
    # Devolver los departamentos como JSON
    return Response({'data': departamentos_data})
  
  
@api_view(['GET'])
def entrega_inmedita_profile(reques, slug):
    # proyecto = get_object_or_404(Proyecto, slug=nombre)  # Asegura que el proyecto exista
    entrega_inmediata = Departamento_Alquiler.objects.filter(
        slug=slug,
   
        estatus="no disponible"
    ).first()


    
    data={
        "precio_desde":entrega_inmediata.precio,
        "area_desde":entrega_inmediata.unit_area,
        "area_hasta":entrega_inmediata.unit_area,
        "dorms_desde":entrega_inmediata.nro_dormitorios,
        "dorms_hasta":entrega_inmediata.nro_dormitorios,
        "slug":entrega_inmediata.slug,
        "nombre": entrega_inmediata.nombre,
        "distrito":  entrega_inmediata.distrito,
        "parrilla":  entrega_inmediata.nombre,
        # "valor_de_separacion": entrega_inmediata.valor_de_separacion,
        "valor_porcentaje_inicial" :  entrega_inmediata.valor_porcentaje_inicial,
        "valor_porcentaje_financiado" : entrega_inmediata.valor_porcentaje_financiado,
        "etapa" :  entrega_inmediata.etapa,
        # "fecha_entrega":  entrega_inmediata.fecha_entrega,
        "edificio" : entrega_inmediata.edificio,
        "anio_construccion": entrega_inmediata.anio_construccion,  
        "areas_comunes" :  entrega_inmediata.areas_comunes,
        "piscina" :  entrega_inmediata.piscina,
        "gym"  :  entrega_inmediata.gym,
        "coworking"  :  entrega_inmediata.coworking,
        "cine"  :  entrega_inmediata.cine,
        "parrilla"  :  entrega_inmediata.parrilla,
        "sum"  :  entrega_inmediata.sum,
        "bicicleta"  :  entrega_inmediata.bicicleta,
        "coordenada_A":entrega_inmediata.coordenada_A,
        "coordenada_B":entrega_inmediata.coordenada_B
    }
    print(data)
    return Response({"proyecto":data})
    
    # Aquí obtienes tus proyectos, probablemente desde la base de datos
    # return Response(proyecto)
def ocultarDef(data):
    if not pd.isna(data):
        return True  if data.lower() =="ocultar" else False
    else: 
        return None

@api_view(['POST'])
def upload_data_department_rent(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            
            nombre = str(data.get('nombre')) if not pd.isna(data.get('nombre')) else None
            texto_sin_tildes = unidecode.unidecode(nombre)    
            slug =  re.sub(r'\s+', '-', texto_sin_tildes.lower())
            nro_depa = nombre
            tipo_inventario = "c/inquilino"
            tipo_moneda = data.get('tipo_moneda').lower() if not pd.isna(data.get('tipo_moneda')) else None
            vista = data.get('vista').lower() if not pd.isna(data.get('vista')) else None
            estatus = data.get('estatus').lower() if not pd.isna(data.get('estatus')) else None
            ocultar = ocultarDef(data.get('ocultar'))
            nro_dormitorios = data.get('nro_dormitorios') if not pd.isna(data.get('nro_dormitorios')) else None
            nro_banos = data.get('nro_banos') if not pd.isna(data.get('nro_banos')) else None
            piso = data.get('piso') if not pd.isna(data.get('piso')) else None
            valor_alquiler = data.get('valor_alquiler') if not pd.isna(data.get('valor_alquiler')) else None
            unit_area = data.get('unit_area') if not pd.isna(data.get('unit_area')) else None
            precio = data.get('precio') if not pd.isna(data.get('precio')) else None
            precio_venta = data.get('precio_venta') if not pd.isna(data.get('precio_venta')) else None
            fecha_ingreso = data.get('fecha_ingreso') if not pd.isna(data.get('fecha_ingreso')) else None
            fecha_actualizacion = data.get('fecha_actualizacion') if not pd.isna(data.get('fecha_actualizacion')) else None
            edificio = data.get('edificio').lower() if not pd.isna(data.get('edificio')) else None
            anio_construccion = data.get('anio_construccion') if not pd.isna(data.get('anio_construccion')) else None
            distrito = data.get('distrito').lower() if not pd.isna(data.get('distrito')) else None
            valor_porcentaje_inicial = data.get('valor_porcentaje_inicial') if not pd.isna(data.get('valor_porcentaje_inicial')) else None
            valor_porcentaje_financiado = data.get('valor_porcentaje_financiado') if not pd.isna(data.get('valor_porcentaje_financiado')) else None
            etapa = "inmediata"
            areas_comunes = True if data.get('areas_comunes') == "SI" else False
            piscina = True if data.get('piscina') == "SI" else False
            gym = True if data.get('gym') == "SI" else False
            coworking = True if data.get('coworking') == "SI" else False
            cine = True if data.get('cine') == "SI" else False
            parrilla = True if data.get('parrilla') == "SI" else False
            sum = True if data.get('sum') == "SI" else False
            bicicleta = True if data.get('bicicleta') == "SI" else False
            bar = True if data.get('bar') == "SI" else False
            web = True
            descuento_porcentaje_preventa=0
            coordenada_A = data.get('coordenada_A') if not pd.isna(data.get('coordenada_A')) else None
            coordenada_B = data.get('coordenada_B') if not pd.isna(data.get('coordenada_B')) else None
            


            tir_ = 0
            roi_ = 0
            valor_cuota_ = 0
            renta_ = 0
            patrimonio_inicial_ = 0
            patrimonio_anio_5_ = 0
            patrimonio_anio_10_ = 0
            patrimonio_anio_20_ = 0
            patrimonio_anio_30_ = 0

            analyzer=Analyzer.objects.get(id=1) 
            
            fecha_entrega_updated = date.today().replace(day=1) 
            new_precio = precio * 3.8 if tipo_moneda == "usd" else precio
            new_precio_dolar = precio if tipo_moneda == "usd" else 0
            
            new_precio_venta = precio_venta * 3.8 if tipo_moneda == "usd" else precio_venta
            new_precio_venta_dolar = precio_venta if tipo_moneda == "usd" else 0
            monto_inicial= new_precio*valor_porcentaje_inicial
            
            
            if new_precio and valor_alquiler and unit_area and valor_porcentaje_inicial and fecha_entrega_updated:

                data = analyze_api(
                    analyzer.tasa_credito, new_precio, valor_alquiler, unit_area, valor_porcentaje_inicial, 
                    fecha_entrega_updated, analyzer.costo_porcentaje_instalacion, descuento_porcentaje_preventa, 
                    analyzer.costo_porcentaje_operativo, analyzer.costo_porcentaje_administrativo, analyzer.corretaje, 
                    analyzer.plazo_meses, analyzer.dias_vacancia, analyzer.costo_porcentaje_capex_reparaciones, 
                    analyzer.costo_porcentaje_administrativos_venta,
                    etapa, tipo_moneda)
                                
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
                "slug": slug,
                "areas_comunes": areas_comunes,
                "etapa": etapa,
                "valor_porcentaje_inicial": valor_porcentaje_inicial,
                "valor_porcentaje_financiado":valor_porcentaje_financiado,
                "distrito": distrito,
                "anio_construccion": anio_construccion,
                "edificio":edificio,
                'ocultar':ocultar,
                'nombre': nombre,
                "fecha_ingreso":fecha_ingreso,
                "fecha_actualizacion": fecha_actualizacion,
                "estatus": estatus,
                'nro_depa': nro_depa,
                'unit_area': unit_area,
                'nro_dormitorios': nro_dormitorios,
                'nro_banos': nro_banos,
                'valor_alquiler': valor_alquiler,
                'piso': piso,
                'vista': vista,
                'precio': new_precio,
                "precio_dolar": new_precio_dolar,
                "precio_venta":new_precio_venta,
                "precio_venta_dolar": new_precio_venta_dolar,
                'descuento_porcentaje_preventa': descuento_porcentaje_preventa,
                'tipo_moneda': tipo_moneda,
                "tipo_inventario": tipo_inventario,
                'patrimonio_inicial': patrimonio_inicial_,
                "patrimonio_anio_5": patrimonio_anio_5_,
                "patrimonio_anio_10": patrimonio_anio_10_,
                'patrimonio_anio_20': patrimonio_anio_20_,
                'patrimonio_anio_30': patrimonio_anio_30_,
                "tir": tir_,
                "roi": roi_,
                "valor_cuota": valor_cuota_,
                "renta": renta_,
                "areas_comunes" :areas_comunes,
                "piscina":piscina,
                "gym" :gym,
                "coworking" :coworking,
                "cine" :cine,
                "parrilla" :parrilla,
                "sum" :sum,
                "bicicleta" :bicicleta,
                "bar":bar,
                "web" :web,
                "coordenada_A" :coordenada_A,
                "coordenada_B" :coordenada_B,
                "monto_inicial":monto_inicial
            }

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            if fields_not_none:
                departamento, created = Departamento_Alquiler.objects.update_or_create(
                    nombre=fields_not_none['nombre'],
                    defaults=fields_not_none
                )
                if created:
                    return Response({'message': 'Departamento Cargado'}, status=200)
                else:
                    return Response({'message': 'Departamento Actualizado'}, status=200)

        except KeyError:
            return Response({'message': 'Archivo no válido'}, status=400)
        except pd.errors.EmptyDataError:
            return Response({'message': 'El archivo está vacío'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=500)
