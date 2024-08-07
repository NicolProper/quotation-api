import json
from django.http import JsonResponse

from proyects.models import Proyecto
from .models import Variable
from rest_framework.decorators import api_view



@api_view(['POST'])
def create_variable(request):
    if request.method == 'POST':
        try:
            data_ = request.body
            data = json.loads(data_)
            
            name = data.get('name').lower()
            value = data.get('value')

            if not name or value is None:
                return JsonResponse({'error': 'Name and value are required'}, status=400)
            
            
            Proyecto.objects.filter(workshop=True).update(workshop=False)
            
            # Usar update_or_create para actualizar o crear el registro
            variable, created = Variable.objects.update_or_create(
                name=name,
                defaults={}
            )
            variable.set_value(value)
            variable.save()
            
            message = "Variable created" if created else "Variable updated"
            return JsonResponse({'message': message}, status=201 if created else 200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            # Captura cualquier otra excepción y registra el error
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

