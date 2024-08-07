import json
from django.shortcuts import get_object_or_404
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from department_workshop.models import Departamento_Workshop
from project_workshop.models import Proyecto_Workshop
from proyects.models import Proyecto
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['POST'])
def active_project(request, nombre):
    if not nombre:
        return Response({'message': 'El campo "nombre" es obligatorio'}, status=400)

    try:
        proyecto = get_object_or_404(Proyecto, nombre=nombre)
        departments = Departamento_Workshop.objects.filter(proyecto=proyecto)
        print(len(proyecto.nombre_real))
        if  not proyecto.nombre_real or len(proyecto.nombre_real) <=1:
            return Response({'message': 'El proyecto NO cuenta con Nombre Real'}, status=200)

        if not departments.exists():
            return Response({'message': 'No existen departamentos para workshop'}, status=200)

        proyecto.workshop = True
        proyecto.save()
        return Response({'message': 'Success'}, status=200)

    except Exception as e:
        # Log unexpected errors for debugging purposes
        print(f"Unexpected error: {e}")
        return Response({'message': 'Something went wrong'}, status=500)



@api_view(['POST'])
def desactive_project(request, nombre):
    if not nombre:
        return Response({'message': 'El campo "nombre" es obligatorio'}, status=400)

    try:
        proyecto = Proyecto.objects.filter(nombre=nombre).first()
        proyecto.workshop = False
        proyecto.save()
        return Response({'message': 'Success'}, status=200)

    except Proyecto.DoesNotExist:
        return Response({'message': 'Something went wrong'}, status=400)
    
    
@api_view(['GET'])
def get_all_projects(request):
    # Parámetro para filtrar por fecha
    data_ = request.body
    data = json.loads(data_)
    print("Received data:", data)
    
    # Get fecha_workshop and validate
    fecha_workshop = data.get('fecha_workshop')
    
    try:
        # Filtrar por fecha_workshop y obtener solo los nombres de los proyectos
        departamentos_data = Proyecto_Workshop.objects.filter(fecha_workshop=fecha_workshop).values_list('nombre', flat=True)
        print("Departamentos found:", departamentos_data)
        
        if not departamentos_data:
            print("No proyectos found for the given fecha_workshop")
            return Response({'data': []})
        
        # Devolver los departamentos como JSON
        return Response({'data': (departamentos_data)})
    except Exception as e:
        print("Error:", e)
        return Response({'error': str(e)}, status=500)



@api_view(['POST'])
def upload_data_proyecto(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            proyecto = data.get('proyecto').lower() if not pd.isna(data.get('proyecto')) else None

            fields = {
                'proyecto': proyecto,
            }

            fields_not_none = {key: value for key, value in fields.items() if value is not None}

            if fields_not_none:
                proyecto_obj = Proyecto.objects.filter(nombre=proyecto).first()
                
                if proyecto_obj:

                    proyecto_workshop, created = Proyecto_Workshop.objects.update_or_create(
                        proyecto=proyecto_obj
                    )
                    if created:
                        print('Registro creado en project_workshop')
                    else:
                        print('Registro actualizado en project_workshop')

            return Response({'message': 'Datos procesados correctamente'}, status=200)

        except Exception as e:
            print(f'Error: {e}')
            return Response({'message': 'Error en la carga de datos'}, status=400)
        
        

@api_view(['GET'])
def get_all_projects_name_id(request):
    # Utiliza values_list para obtener solo los IDs de los proyectos desde Proyecto_Workshop
    project_ids = Proyecto_Workshop.objects.values_list('proyecto_id', flat=True)
    data = []

    for project_id in project_ids:
        # Obtener el objeto Proyecto correspondiente al ID del proyecto
        try:
            proyecto = Proyecto.objects.get(id=project_id)
            data.append({'id': proyecto.id, 'nombre': proyecto.nombre, "slug": proyecto.slug})
        except Proyecto.DoesNotExist:
            continue  # Si no se encuentra el proyecto, continúa con el siguiente

    # Devolver los datos como JSON
    return Response({'data': data})



@api_view(['GET'])
def get_info_project(request, id):
    project = Proyecto_Workshop.objects.filter(proyecto_id=id).first()
    if project:
        data = {
            "parrafo": project.parrafo,
            "frase": project.frase
        }
        return Response({'data': data})
    else:
        return Response({'error': 'Project not found'}, status=404)
    
    
@api_view(['POST'])
def update_info_project(request, id):
    try:
        # data = json.loads(request.body)

        # frase = data.get('frase', '').lower()
        # parrafo = data.get('parrafo', '').lower()
        data_ = request.body
        data = json.loads(data_)
        frase = data.get('frase').lower() if not pd.isna(data.get('frase')) else None
        parrafo = data.get('parrafo').lower() if not pd.isna(data.get('parrafo')) else None

        project = Proyecto_Workshop.objects.filter(proyecto_id=id).first()
        if project:
            project.frase = frase
            project.parrafo = parrafo
            project.save()
            return Response({'message': 'Datos actualizados correctamente'}, status=200)
        else:
            return Response({'message': 'Proyecto no encontrado'}, status=404)

    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error en la carga de datos'}, status=400)
    
    
    # get_all_projects_workshop
    
@api_view(['POST'])
def get_all_projects_workshop(request):
    try:
        data_ = request.body
        data = json.loads(data_)
        
        # Get fecha_workshop and validate
        fecha_workshop = data.get('fecha_workshop')
                
        # Query the database
        departamentos = Departamento_Workshop.objects.filter(fecha_workshop=fecha_workshop).distinct('proyecto')
        print("Departamentos found:", departamentos)
        
        data = []
        # Check if any departamentos exist and respond accordingly
        if departamentos.exists():
            for departamento in departamentos:
                data.append({
                    'nombre': departamento.proyecto.nombre,
                    'id': departamento.proyecto.id,
                    'slug': departamento.proyecto.slug
                })
            return Response({'message': 'Datos actualizados correctamente', 'data': data}, status=200)
        else:
            print("No proyectos found for the given fecha_workshop")
            return Response({'message': 'Proyecto no encontrado', 'data': []}, status=201)

    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error en la carga de datos', 'data': []}, status=400)