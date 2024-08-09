import uuid
from django.db import models

from departments.models import Departamento
from departments_rent.models import Departamento_Alquiler
from proyects.models import Proyecto

# Enum etapa: Planos, preventa, construccion, entrega inme

class Proyectos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(blank=True, null=True)  # Allow null if blank is allowed
    asesor = models.CharField(max_length=100)
    correo_asesor = models.EmailField(max_length=100)  # Use EmailField for better validation
    cliente = models.CharField(max_length=100)
    dni = models.CharField(max_length=10)  # Adjust length based on the format of your DNI
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
    proyecto_nombre = models.CharField(max_length=100, null=True)  # You might want to keep this in sync with Proyecto
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True)
    departamento_nro = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.dni
    
    
