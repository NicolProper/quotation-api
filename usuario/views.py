import json
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import permissions
from rest_framework import viewsets
from usuario.models import User
from usuario.serializers import UsuarioSerializer
from django.shortcuts import render
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
        usuario = User.objects.get(dni=int(dni))  # Buscar usuario por DNI
    except User.DoesNotExist:
        return JsonResponse({'mensaje': 'Usuario no encontrado'}, status=404)

    # Serializar el usuario encontrado
    serializer = UsuarioSerializer(usuario)
    
    # Devolver la respuesta con los datos serializados del usuario
    return JsonResponse({"data":serializer.data, "mensaje": "Usuario encontrado"}, status=200)