import uuid
from django.db import models

# Create your models here.
from django.db import models
from proyects.models import Proyecto

class Departamento_Workshop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_workshop = models.DateField(null=False)
    nro_depa = models.CharField(max_length=200)
    precio = models.FloatField(default=0)
    precio_workshop = models.FloatField(default=0)

    def __str__(self):
        return self.nro_depa