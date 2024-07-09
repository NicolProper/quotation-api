import uuid
from django.db import models

from departments.models import Departamento
from proyects.models import Proyecto

# Enum etapa: Planos, preventa, construccion, entrega inme

class Proyectos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(blank=True)
    asesor =models.CharField(max_length=100)
    correo_asesor = models.CharField(max_length=100, null=False)
    cliente = models.CharField(max_length=100, null=False)
    dni=models.CharField(max_length=100)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    proyecto_nombre = models.CharField(max_length=20, null=False)
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
    departamento_nro=models.CharField(max_length=20, null=False)

    # Also could be a slug to static url
    def __str__(self):
        return self.dni
    
    
