from django.db import models
from django.dispatch import receiver

# Enum etapa: Planos, preventa, construccion, entrega inme

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200,unique=True)
    distrito = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, default='')
    fecha_entrega = models.DateField(blank=True)
    fecha_ingreso = models.DateField(default="1900-02-01")
    nombre_real = models.CharField(max_length=200,  default='')
    # precio_desde =  models.FloatField(blank=True, default=0)

    class Etapa(models.TextChoices):
        PLANOS = 'planos'
        PREVENTA = 'preventa'
        CONSTRUCCION = 'construccion'
        ENTREGA_INMEDIATA = 'entrega inmediata'

    etapa = models.CharField(
        max_length=20,
        choices=Etapa.choices,
        default=Etapa.PLANOS,
    )

    class Banco(models.TextChoices):
        BBVA = 'bbva'
        BANBIF = 'banbif'
        SCOTIABANK = 'scotiabank'
        IBK = 'ibk'
        BCP = 'bcp'
        TODOS = 'todos'
    banco = models.CharField(
        max_length=20,
        choices=Banco.choices,
        default=Banco.TODOS,
    )

    class Moneda(models.TextChoices):
        SOLES = 'pen'
        DOLAR = 'usd'
    tipo_moneda = models.CharField(
        max_length=20,
        choices=Moneda.choices,
        default=Moneda.SOLES,
    )

    nro_pisos = models.IntegerField(default=0)
    nro_dptos = models.IntegerField(default=0)   
    valor_de_separacion = models.FloatField(default=0)
    # valor_inicial = models.FloatField(default=0)
    # valor_financiado = models.FloatField(default=0)
    valor_porcentaje_inicial = models.FloatField(default=0)
    valor_porcentaje_financiado = models.FloatField(default=0)
    # area_desde =  models.FloatField(default=1)
    # area_hasta =  models.FloatField( default=1)
    # dorms_desde =  models.FloatField( default=1)
    # dorms_hasta =  models.FloatField( default=1)  
    # banos_desde =  models.FloatField( default=1)
    # banos_hasta =  models.FloatField( default=1)
    # renta = models.FloatField(null=False, default=0)
    # roi = models.FloatField(null=False,  default=0)
    # tir = models.FloatField(null=False,  default=0)
    # valor_alquiler = models.FloatField(null=False,  default=0)
    # valor_cuota =models.FloatField(null=False,  default=0)

    areas_comunes = models.BooleanField(default=False)
    piscina= models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    coworking = models.BooleanField(default=False)
    cine = models.BooleanField(default=False)
    parrilla = models.BooleanField(default=False)
    sum = models.BooleanField(default=False)
    bicicleta = models.BooleanField(default=False)
    workshop = models.BooleanField(default=False) 
    web = models.BooleanField(default=False) 
    bar = models.BooleanField(default=False) 
    # parametros analizer
    dias_vacancia=models.FloatField(null=False,  default=0)
    costo_porcentaje_operativo=models.FloatField(null=False,  default=0)
    costo_porcentaje_administrativo=models.FloatField(null=False,  default=0)
    costo_porcentaje_instalacion=models.FloatField(null=False,  default=0)
    corretaje= models.BooleanField(default=False) 
    tasa_credito= models.FloatField(null=False,  default=0.06)
    costo_porcentaje_capex_reparaciones=models.FloatField(null=False,  default=0) #gastos de capital
    plazo_meses = models.IntegerField(default=300)
    descuento_porcentaje_preventa=models.FloatField(null=False,  default=0)  
    costo_porcentaje_administrativos_venta=models.FloatField(null=False,  default=0) #costo de cierre
    coordenada_A=models.FloatField(null=True)
    coordenada_B=models.FloatField(null=True)
    
    
    #coordinadas
    


        
    

    # Also could be a slug to static url
    def __str__(self):
        return self.nombre
    
    
