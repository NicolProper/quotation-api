import uuid
from django.db import models
from django.dispatch import receiver

# Enum etapa: Planos, preventa, construccion, entrega inme

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    apellido =models.CharField(max_length=200)
    dni = models.CharField(max_length=20, null=False)
    edad = models.IntegerField(null=False,  default=0)


    class Residencia(models.TextChoices):
        PERU = 'Perú'
        EXTRANJERO = 'Extranjero'

    residencia = models.CharField(
        max_length=20,
        choices=Residencia.choices,
        default=Residencia.PERU,
    )

    class PrimeraVivienda(models.TextChoices):
        SI = 'SÍ'
        NO = 'NO'
        
    primera_vivienda = models.CharField(
        max_length=10,
        choices=PrimeraVivienda.choices,
        default=PrimeraVivienda.SI,
    )


    ingreso_primera_categoria=models.FloatField(null=False,  default=0)
    ingreso_segunda_categoria=models.FloatField(null=False,  default=0)
    ingreso_tercera_categoria=models.FloatField(null=False,  default=0)
    ingreso_cuarta_categoria=models.FloatField(null=False,  default=0)
    ingreso_quinta_categoria= models.FloatField(null=False,  default=0)

    cuota_vehicular= models.FloatField(null=False,  default=0)
    cuota_personal=models.FloatField(null=False,  default=0) #gastos de capital
    cuota_tarjeta_credito = models.FloatField(null=False, default=0)
    cuota_inicial=models.FloatField(null=False,  default=0)  
    cuota_hipotecaria=models.FloatField(null=False,  default=0) #costo de cierre

    
    #coordinadas
    


        
    

    # Also could be a slug to static url
    def __str__(self):
        return self.dni
    
    
