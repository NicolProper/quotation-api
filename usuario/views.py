import json
# import os
# from urllib.request import Request
# from django.shortcuts import render
# from httplib2 import Credentials
# from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import permissions
from rest_framework import viewsets
from usuario.models import User
from usuario.serializers import UsuarioSerializer
# from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view


# Create your views here.
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')  # Ordenar por el campo 'id' u otro campo adecuado
    serializer_class = UsuarioSerializer 
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = USE  # Usar el filtro personalizado
    ordering_fields = '__all__'
    
# usuario/utils.py


from .models import User  # Asegúrate de importar el modelo correcto

def crear_usuario(nombre, apellido,dni, cuota_hipotecaria,  edad, residencia, ingreso_primera_categoria, ingreso_segunda_categoria, ingreso_tercera_categoria, ingreso_cuarta_categoria, ingreso_quinta_categoria, primera_vivienda, cuota_vehicular, cuota_personal, cuota_tarjeta_credito, cuota_inicial):
    # Verificar si ya existe un usuario con el mismo DNI
    if User.objects.filter(dni=dni).exists():
        raise ValueError("Ya existe un usuario con este DNI.")

    # Crear un nuevo usuario
    nuevo_usuario = User(nombre=nombre,apellido=apellido, dni=dni, cuota_hipotecaria=cuota_hipotecaria,  edad=edad, residencia=residencia, ingreso_primera_categoria=ingreso_primera_categoria, ingreso_segunda_categoria=ingreso_segunda_categoria, ingreso_tercera_categoria=ingreso_tercera_categoria, ingreso_cuarta_categoria=ingreso_cuarta_categoria, ingreso_quinta_categoria=ingreso_quinta_categoria, primera_vivienda=primera_vivienda, cuota_vehicular=cuota_vehicular, cuota_personal=cuota_personal, cuota_tarjeta_credito=cuota_tarjeta_credito, cuota_inicial=cuota_inicial)
    nuevo_usuario.save()

    return nuevo_usuario

@api_view(['POST'])
def actualizar_usuario(dni, datos_actualizacion):
    if dni is None:
        raise ValueError("El DNI es obligatorio para identificar al usuario.")
    
    # Verificar si ya existe un usuario con el mismo DNI
    usuario_existente = User.objects.filter(dni=dni).first()
    
    if usuario_existente is None:
        raise ValueError("No existe un usuario con este DNI.")
    
    # Actualizar los campos del usuario existente según los datos proporcionados
    for campo, valor in datos_actualizacion.items():
        if hasattr(usuario_existente, campo):
            setattr(usuario_existente, campo, valor)
    
    usuario_existente.save()
    
    return usuario_existente




# usuario/views.py
@api_view(['POST'])
def crear_usuario_view(request):
    if request.method == 'POST':
        data_ = request.body
        data = json.loads(data_)
        nombre= data.get('nombre')
        apellido= data.get('apellido')
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

        try:
            usuario_creado = crear_usuario(nombre,apellido, dni, cuota_hipotecaria, edad, residencia, ingreso_primera_categoria,ingreso_segunda_categoria, ingreso_tercera_categoria, ingreso_cuarta_categoria , ingreso_quinta_categoria, primera_vivienda, cuota_vehicular, cuota_personal, cuota_tarjeta_credito, cuota_inicial)
            return JsonResponse({'mensaje': 'Usuario creado exitosamente', 'id': usuario_creado.id}, status=201)
        except ValueError as e:
            return JsonResponse({'mensaje': str(e)}, status=201)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)



@api_view(['PUT'])  # Utilizamos PUT para actualizaciones
def actualizar_usuario_view(request, pk):
    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)

    # Si el usuario existe, intentamos actualizarlo
    data = request.data  # Utilizamos request.data para obtener los datos del cuerpo de la solicitud

    # Serializamos el usuario existente con los datos actualizados
    serializer = UsuarioSerializer(usuario, data=data)
    
    if serializer.is_valid():
        serializer.save()  # Guardamos los datos actualizados en la base de datos
        return JsonResponse(serializer.data, status=200)
    
    return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
def buscar_usuario_por_dni(request, dni):
    try:
        usuario = User.objects.get(dni=dni)  # Buscar usuario por DNI
    except User.DoesNotExist:
        return JsonResponse({'mensaje': 'Usuario no encontrado'}, status=404)

    # Serializar el usuario encontrado
    serializer = UsuarioSerializer(usuario)
    
    # Devolver la respuesta con los datos serializados del usuario
    return JsonResponse({"data":serializer.data, "mensaje": "Usuario encontrado"}, status=200)




SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# def get_gmail_service():
#     creds = None
#     token_path = os.path.join('token.json')

#     if os.path.exists(token_path):
#         creds = Credentials.from_authorized_user_file(token_path, SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 os.path.join('credentials.json'), SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open(token_path, 'w') as token:
#             token.write(creds.to_json())

#     try:
#         service = build('gmail', 'v1', credentials=creds)
#         return service
#     except HttpError as error:
#         print(f'An error occurred: {error}')
#         return None

# def send_email(service, sender, to, subject, message_text):
#     message = MIMEText(message_text)
#     message['to'] = to
#     message['from'] = sender
#     message['subject'] = subject
#     raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
#     body = {'raw': raw_message}
#     try:
#         message = service.users().messages().send(userId='me', body=body).execute()
#         print(f'Message Id: {message["id"]}')
#         return message
#     except HttpError as error:
#         print(f'An error occurred: {error}')
#         return None