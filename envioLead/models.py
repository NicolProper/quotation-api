import uuid
from django.db import models

from departments.models import Departamento
from departments_rent.models import Departamento_Alquiler
from proyects.models import Proyecto

# Enum etapa: Planos, preventa, construccion, entrega inme

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(blank=True, null=True)  # Allow null if blank is allowed
    nombre = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    dni = models.CharField(max_length=10)  # Adjust length based on the format of your DNI
    celular = models.CharField(max_length=20)  # Adjust length based on the format of your DNI
    correo = models.CharField(max_length=20)  # Adjust length based on the format of your DNI
    inmobiliaria = models.CharField(max_length=20)  # Adjust length based on the format of your DNI
    emisor = models.CharField(max_length=20)  # Adjust length based on the format of your DNI
    emisor = models.CharField(max_length=20)  # Adjust length based on the format of your DNI

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)    
    proyecto_nombre = models.CharField(max_length=100, null=True)  # You might want to keep this in sync with Proyecto

    def __str__(self):
        return self.dni
    
    
