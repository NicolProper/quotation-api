import uuid
from django.db import models
from django.dispatch import receiver
from proyects.models import Proyecto

# Enum etapa: Planos, preventa, construccion, entrega inme

class Proyecto_Workshop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frase = models.CharField(max_length=1000, default='')
    parrafo = models.CharField(max_length=3000, default='')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    # Also could be a slug to static url
    def __str__(self):
        return self.proyecto
    
    
