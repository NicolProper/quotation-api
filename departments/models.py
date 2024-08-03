from django.db import models
from proyects.models import Proyecto

class Departamento(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_actualizacion = models.DateField(null=True, blank=True)
    nro_depa = models.CharField(max_length=200)
    unit_area = models.FloatField( default=1)   
    nro_dormitorios = models.IntegerField(default=1)
    nro_banos = models.IntegerField(default=1)
    piso = models.IntegerField(default=1)


    class Vista(models.TextChoices):
        INTERIOR = 'interior'
        EXTERIOR = 'exterior'
    vista = models.CharField(
        max_length=20,
        choices=Vista.choices,
        blank=True
    )
    
    class Moneda(models.TextChoices):
        SOLES = 'pen'
        DOLAR = 'usd'
    tipo_moneda = models.CharField(
        max_length=20,
        choices=Moneda.choices,
        default=Moneda.SOLES,
    )
    
    class TIPO_INVENTARIO(models.TextChoices):
        PROYECTO = 'proyecto'
        CINQUILINO = 'c/inquilino'
        
    tipo_inventario = models.CharField(
        max_length=100,
        choices=TIPO_INVENTARIO.choices,
        default=TIPO_INVENTARIO.PROYECTO,
    )
    nombre = models.CharField(max_length=100, blank=True)
    tipo_departamento= models.CharField(max_length=200, default="")
    
    precio = models.FloatField(default=0)
    precio_dolar = models.FloatField(null=True)
    precio_venta = models.FloatField(default=0)
    precio_venta_dolar = models.FloatField(default=0)
    monto_inicial = models.FloatField(default=0)
    estatus = models.CharField(max_length=100, default="no disponible")
    ocultar = models.BooleanField(default=False)

    precio_workshop = models.FloatField(null=True)
    valor_descuento_preventa = models.FloatField(null=True)
    reservado = models.BooleanField(default=False)
    valor_alquiler = models.FloatField(default=0)
    roi = models.FloatField(default=0)
    tir = models.FloatField(default=0)   
    valor_cuota = models.FloatField(default=0)
    renta = models.FloatField(default=0) 


    patrimonio_inicial =  models.FloatField(default=0)
    patrimonio_anio_5 =  models.FloatField(default=0)
    patrimonio_anio_10 =  models.FloatField(default=0)
    patrimonio_anio_20 =  models.FloatField(default=0)
    patrimonio_anio_30 =  models.FloatField(default=0)

    # def save(self, *args, **kwargs):
    #     self.monto_inicial = self.proyecto.valor_porcentaje_inicial * self.precio
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre