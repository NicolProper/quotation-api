import json

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import permissions
from rest_framework import viewsets
from usuario.models import User
from usuario.serializers import UsuarioSerializer
# from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.mail import EmailMultiAlternatives


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

# @api_view(['POST'])
# def actualizar_usuario(request, dni):
#     try:
#         usuario = User.objects.get(dni=dni)
#     except User.DoesNotExist:
#         return Response({"error": "El usuario no existe"}, status=)

#     # Aquí procesas la actualización del usuario con los datos recibidos en la solicitud
#     serializer = UserSerializer(usuario, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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
def actualizar_usuario_view(request, dni):
    try:
        usuario = User.objects.filter(dni=dni).first()
        print(usuario)
    except User.DoesNotExist:
        return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)
    data_str = request.body
    data = json.loads(data_str)
    print(data)
    # Serializamos el usuario existente con los datos actualizados
    serializer = UsuarioSerializer(usuario, data=data)
    print(serializer)
    # Actualiza los campos del usuario según los datos recibidos
    for key, value in data.items():
        setattr(usuario, key, value)

    # Guarda los cambios en la base de datos
    usuario.save()

    model = {
        "id":usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "dni": usuario.dni,
        "edad": int(usuario.edad),
        "residencia": usuario.residencia,
        "ingreso_primera_categoria": float(usuario.ingreso_primera_categoria),
        "ingreso_segunda_categoria": float(usuario.ingreso_segunda_categoria),
        "ingreso_tercera_categoria": float(usuario.ingreso_tercera_categoria),
        "ingreso_cuarta_categoria":float(usuario.ingreso_cuarta_categoria),
        "ingreso_quinta_categoria": float(usuario.ingreso_quinta_categoria),
        "primera_vivienda": usuario.primera_vivienda,
        "cuota_hipotecaria": float(usuario.cuota_hipotecaria),
        "cuota_vehicular": float(usuario.cuota_vehicular),
        "cuota_personal": float(usuario.cuota_personal),
        "cuota_tarjeta_credito": float(usuario.cuota_tarjeta_credito),
        "cuota_inicial": float(usuario.cuota_inicial)
    }
    return JsonResponse({'mensaje': 'Usuario actualizado correctamente', "data":model}, status=200)


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










# @api_view(['POST'])
# def send_email_with_attachments(request):
#     if request.method == 'POST':
#         try:
#             # Obtener datos del formulario
#             subject = request.POST.get('subject')
#             message = request.POST.get('message')
#             from_email = "nicole.mendoza@proper.com.pe"
#             to_email = "nicolmendozamattos@gmail.com"
#             attachments = request.FILES.getlist('attachments')  # Obtener una lista de archivos adjuntos
#             print(request.FILES.getlist)
#             print(attachments)

#             # Validar que todos los parámetros necesarios estén presentes
#             if subject and message and from_email and to_email and attachments:
#                 try:
#                     # Configurar el correo electrónico
#                     email = EmailMultiAlternatives(subject, message, from_email, [to_email])
#                     email.attach_alternative(message, "text/html")  # Agregar mensaje en formato HTML si es necesario
                    
#                     # Adjuntar archivos
#                     for attachment in attachments:
#                         print(attachment)
#                         email.attach(attachment.name, attachment.read(), attachment.content_type)
                    
#                     # Enviar el correo electrónico
#                     email.send()
                    
#                     return JsonResponse({'message': 'Correo con adjuntos enviado exitosamente!'})
#                 except Exception as e:
#                     return JsonResponse({'error': str(e)}, status=500)
#             else:
#                 return JsonResponse({'error': 'Faltan parámetros.'}, status=400)
#         except KeyError:
#             return JsonResponse({'error': 'No se proporcionaron los archivos adjuntos.'}, status=400)

#     return JsonResponse({'error': 'Método no permitido'}, status=405)



@api_view(['POST'])
def send_email_with_attachments(request):
    if request.method == 'POST':
        try:
            data_ = request.POST.get('data')
            data = json.loads(data_)
            # Obtener datos del formulario
            subject = data.get('subject')
            message = data.get('message')
            from_email = "nicole.mendoza@proper.com.pe"
            to_email = "nicolmendozamattos@gmail.com"
            print(subject,message)

            attachments = request.FILES.get('attachments')  # Obtener una lista de archivos adjuntos
            print(request.FILES)

            # Validar que todos los parámetros necesarios estén presentes
            if subject and message and from_email and to_email and attachments:
                try:
                    # Configurar el correo electrónico
                    print('ingrse_________1')
                    email = EmailMultiAlternatives(subject, message, from_email, [to_email])
                    email.attach_alternative(message, "text/html")  # Agregar mensaje en formato HTML si es necesario
                    print('ingrse_________2')
                    
                    # print(type(attachments))  # Asegúrate de que es una lista
                    # print(attachments)
                    # Adjuntar archivos
                    for attachment in [attachments]:
                        # print(attachment.content_type)  # Imprime los detalles de cada archivo
                        email.attach(attachment.name, attachment.read(), attachment.content_type)
                    print('ingrse_________3')

                    # Enviar el correo electrónico
                    email.send()
                    
                    return JsonResponse({'message': 'Correo con adjuntos enviado exitosamente!'})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Faltan parámetros.'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'No se proporcionaron los archivos adjuntos.'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)