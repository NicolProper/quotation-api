# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .services.s3_service import upload_image, delete_image
from rest_framework.decorators import api_view

# services/s3_service.py

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def upload_image(file, project_name, image_name, file_name):
    key = f"{project_name}/{file_name}/{image_name}"
    try:
        path = default_storage.save(key, ContentFile(file.read()))
        return default_storage.url(path)
    except Exception as e:
        return str(e)




@api_view(['POST'])
def upload_image_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        project_name = request.POST.get('project_name')
        file_name = request.POST.get('file_name')
        image_name = file.name
        url = upload_image(file, project_name, image_name,file_name)
        return JsonResponse({'url': url})



def delete_image(project_name, image_name, file_name):
    key = f"{project_name}/{file_name}/{image_name}"
    print(key)
    try:
        default_storage.delete(key)
        return True
    except Exception as e:
        return str(e)
    
    
@api_view(['POST'])
def delete_image_view(request):
    if request.method == 'POST':
        
        project_name = request.POST.get('project_name')
        file_name = request.POST.get('file_name')
        print(project_name)
        image_name = request.POST.get('image_name')
        result = delete_image(project_name, image_name, file_name)
        print(result)
        return JsonResponse({'result': result})


