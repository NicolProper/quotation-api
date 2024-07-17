import uuid
from django.db import models
from proyects.models import Proyecto

class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(null=True, blank=True)
    nombre = models.CharField(max_length=200)
    apellido =models.CharField(max_length=200)
    dni = models.CharField(max_length=20, null=False)
    ingresos = models.FloatField(null=False,  default=0)
    deudas = models.FloatField(null=False,  default=0)
    tasa_interes = models.FloatField(null=False,  default=0)
    plazo_meses = models.IntegerField(null=False,  default=0)
    valor_porcentaje_inicial= models.FloatField(null=False,  default=0)
    valor_porcentaje_capacidad_deuda=models.FloatField(null=False,  default=0) #gastos de capital
    banco = models.CharField(max_length=200)
    financiamiento_max=models.FloatField(null=False,  default=0) #costo de cierre
    asesor=models.CharField(max_length=200, default='')

    
    def __str__(self):
        return self.nombre