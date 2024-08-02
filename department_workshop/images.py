from django.core.files.storage import get_storage_class
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .custom_storage import AnotherBucketS3Boto3Storage  # Importa tu clase personalizada

def upload_image(file, project_name, image_name, file_name):
    storage = AnotherBucketS3Boto3Storage()
    key = f"{project_name}/{file_name}/{image_name}"
    try:
        path = storage.save(key, file)
        return storage.url(path)
    except Exception as e:
        return str(e)

@api_view(['POST'])
def upload_image_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        project_name = request.POST.get('project_name')
        file_name = request.POST.get('file_name')
        image_name = file.name
        url = upload_image(file, project_name, image_name, file_name)
        return JsonResponse({'url': url})


def delete_image(project_name, image_name, file_name):
    storage = AnotherBucketS3Boto3Storage()
    key = f"{project_name}/{file_name}/{image_name}"
    print(key)
    try:
        storage.delete(key)
        return True
    except Exception as e:
        return str(e)

@api_view(['POST'])
def delete_image_view(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        file_name = request.POST.get('file_name')
        image_name = request.POST.get('image_name')
        result = delete_image(project_name, image_name, file_name)
        return JsonResponse({'result': result})