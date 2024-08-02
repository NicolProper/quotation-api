import json
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from department_workshop.models import Departamento_Workshop
from project_workshop.models import Proyecto_Workshop
from proyects.models import Proyecto
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])

def active_project(request, name_proyecto):
    try:
        proyecto = Proyecto.objects.filter(nombre=name_proyecto).first()
        if not proyecto:
            return Response({"result": False, "message": "Proyecto no encontrado"}, status=404)

        # Verificar si ya existe un ProyectoWorkshop para este proyecto
        existing_workshop = Proyecto_Workshop.objects.filter(proyecto=proyecto).first()
        if existing_workshop:
            return Response({"result": True, "id": existing_workshop.id, "message": "ProyectoWorkshop ya existe"}, status=200)
        
        nuevo_workshop = Proyecto_Workshop.objects.create(
            proyecto=proyecto
        )

        return Response({"result": True, "id": nuevo_workshop.id, "message": "ProyectoWorkshop creado exitosamente"}, status=201)

    except Exception as e:
        print(f'Error: {e}')
        return Response({"result": False, "message": str(e)}, status=500)


@api_view(['GET'])
def get_all_projects(request):
    # Utiliza values_list para obtener solo los nombres de los proyectos
    departamentos_data = Proyecto_Workshop.objects.values_list('nombre', flat=True)

    # Devolver los departamentos como JSON
    return Response({'data': list(departamentos_data)})



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
                        proyecto=proyecto_obj,
                        defaults={
                            'frase': '',
                            'parrafo': '',
                        }
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
    
@api_view(['GET'])
def get_all_projects_workshop(request):
    try:
        data_ = request.body
        data = json.loads(data_)
        fecha_workshop = data.get('fecha_workshop').lower() if data.get('fecha_workshop') and not pd.isna(data.get('fecha_workshop')) else None

        departamentos = Departamento_Workshop.objects.filter(fecha_workshop=fecha_workshop).distinct('proyecto')

        if departamentos.exists():
            proyectos = [departamento.proyecto for departamento in departamentos]
            return Response({'message': 'Datos actualizados correctamente', 'proyectos': proyectos}, status=200)
        else:
            return Response({'message': 'Proyecto no encontrado'}, status=404)

    except Exception as e:
        print(f'Error: {e}')
        return Response({'message': 'Error en la carga de datos'}, status=400)
