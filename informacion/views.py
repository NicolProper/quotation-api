import json
from django.db import models

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import permissions
from rest_framework import viewsets
from informacion.serializers import BancariaSerializer
# from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.mail import EmailMultiAlternatives
from .models import Bancaria  # Asegúrate de importar el modelo correcto


# Create your views here.
class BancariaViewSet(viewsets.ModelViewSet):
    queryset = Bancaria.objects.all().order_by('id')  # Ordenar por el campo 'id' u otro campo adecuado
    serializer_class = BancariaSerializer 
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = USE  # Usar el filtro personalizado
    ordering_fields = '__all__'
    
# usuario/utils.py



def crear_usuario(nombre, apellido,dni, cuota_hipotecaria,  edad, residencia, ingreso_primera_categoria, ingreso_segunda_categoria, ingreso_tercera_categoria, ingreso_cuarta_categoria, ingreso_quinta_categoria, primera_vivienda, cuota_vehicular, cuota_personal, cuota_tarjeta_credito, cuota_inicial, continuidad_laboral):
    # Verificar si ya existe un usuario con el mismo DNI
    if Bancaria.objects.filter(dni=dni).exists():
        raise ValueError("Ya existe un usuario con este DNI.")

    # Crear un nuevo usuario
    nuevo_usuario = Bancaria(nombre=nombre,apellido=apellido, dni=dni, cuota_hipotecaria=cuota_hipotecaria,  edad=edad, residencia=residencia, ingreso_primera_categoria=ingreso_primera_categoria, ingreso_segunda_categoria=ingreso_segunda_categoria, ingreso_tercera_categoria=ingreso_tercera_categoria, ingreso_cuarta_categoria=ingreso_cuarta_categoria, ingreso_quinta_categoria=ingreso_quinta_categoria, primera_vivienda=primera_vivienda, cuota_vehicular=cuota_vehicular, cuota_personal=cuota_personal, cuota_tarjeta_credito=cuota_tarjeta_credito, cuota_inicial=cuota_inicial, continuidad_laboral=continuidad_laboral)
    nuevo_usuario.save()

    return nuevo_usuario


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
        continuidad_laboral=data.get('continuidad_laboral')

        try:
            usuario_creado = crear_usuario(nombre,apellido, dni, cuota_hipotecaria, edad, residencia, ingreso_primera_categoria,ingreso_segunda_categoria, ingreso_tercera_categoria, ingreso_cuarta_categoria , ingreso_quinta_categoria, primera_vivienda, cuota_vehicular, cuota_personal, cuota_tarjeta_credito, cuota_inicial, continuidad_laboral)
            return JsonResponse({'mensaje': 'Usuario creado exitosamente', 'id': usuario_creado.id}, status=201)
        except ValueError as e:
            return JsonResponse({'mensaje': str(e)}, status=201)

    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)



@api_view(['PUT'])  # Utilizamos PUT para actualizaciones
def actualizar_usuario_view(request, dni):
    try:
        usuario = Bancaria.objects.filter(dni=dni).first()
        print(usuario)
    except Bancaria.DoesNotExist:
        return JsonResponse({'mensaje': 'El usuario no existe'}, status=404)
    data_str = request.body
    data = json.loads(data_str)
    print(data)
    # Serializamos el usuario existente con los datos actualizados
    serializer = BancariaSerializer(usuario, data=data)
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
        "cuota_inicial": float(usuario.cuota_inicial),
        "continuidad_laboral": int(usuario.continuidad_laboral)

    }
    return JsonResponse({'mensaje': 'Usuario actualizado correctamente', "data":model}, status=200)


@api_view(['GET'])
def buscar_usuario_por_dni(request, dni):
    try:
        usuario = Bancaria.objects.get(dni=dni)  # Buscar usuario por DNI
    except Bancaria.DoesNotExist:
        return JsonResponse({'mensaje': 'Usuario no encontrado'}, status=404)

    # Serializar el usuario encontrado
    serializer = BancariaSerializer(usuario)
    
    # Devolver la respuesta con los datos serializados del usuario
    return JsonResponse({"data":serializer.data, "mensaje": "Usuario encontrado"}, status=200)

class Cliente(models.Model):
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

    
def match_user_by_DNI(request, dni):
    try:
        print(dni)
        # Realiza la consulta a la base de datos secundaria
        usuario = Cliente.objects.using('postgres').filter(nrodoc=dni).first()
        
        # Verifica si se encontraron usuarios
        if not usuario:
            return JsonResponse({'message': 'No se encontró ningún usuario con ese DNI.'}, status=404)
        
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
        return JsonResponse({'message': 'Se encontró el usuario con ese DNI.', "data": usuarios_data}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Serializar el usuario encontrado
    # serializer = UsuarioSerializer(usuario)
    
    # Devolver la respuesta con los datos serializados del usuario

# SCOPES = ['https://www.googleapis.com/auth/gmail.send']





@api_view(['POST'])
def send_email_with_attachments(request):
    if request.method == 'POST':
        try:
            data_ = request.POST.get('data')
            data = json.loads(data_)
            # Obtener datos del formulario
            subject = data.get('subject')
            message = data.get('message')
            remitente= data.get('remitente')
            destinatario= data.get('destinatario')

            from_email = remitente
            to_emails = [remitente,destinatario]
            print(subject,message)

            attachments = request.FILES.getlist('attachments')  # Obtener una lista de archivos adjuntos
            print(attachments)

            # Validar que todos los parámetros necesarios estén presentes
            if subject and message and from_email and to_emails and attachments:
                try:
                    # Configurar el correo electrónico
                    print('ingrse_________1')
                    email = EmailMultiAlternatives(subject, message, from_email, to_emails)
                    email.attach_alternative(message, "text/html")  # Agregar mensaje en formato HTML si es necesario
                    print('ingrse_________2')
                    
                    # print(type(attachments))  # Asegúrate de que es una lista
                    # print(attachments)
                    # Adjuntar archivos
                    for attachment in attachments:
                        print(attachment)  # Imprime los detalles de cada archivo
                        email.attach(attachment.name, attachment.read(), attachment.content_type)
                    # print('ingrse_________3')

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