import uuid
from django.db import models

class Departamento_Alquiler(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200,unique=True, default='')
    nro_depa =  models.CharField(max_length=50,blank=True)
    codigo =  models.CharField(max_length=50,blank=True)
    slug = models.CharField(max_length=200, default='')

    fecha_actualizacion = models.DateField(null=True, blank=True)
    fecha_ingreso = models.DateField(default="1900-02-01")

    edificio =  models.CharField(max_length=50,blank=True)
    anio_construccion = models.IntegerField(blank=True,  default=2024)
    distrito = models.CharField(max_length=100,blank=True,  default="lima")
    class Moneda(models.TextChoices):
        SOLES = 'pen'
        DOLAR = 'usd'
    tipo_moneda = models.CharField(
        max_length=20,
        choices=Moneda.choices,
        default=Moneda.SOLES,
    )
    estatus = models.CharField(max_length=100, default="no disponible")
    ocultar = models.BooleanField(default=False)

    class TIPO_INVENTARIO(models.TextChoices):
        PROYECTO = 'proyecto'
        CINQUILINO = 'c/inquilino'
        
    tipo_inventario = models.CharField(
        max_length=100,
        choices=TIPO_INVENTARIO.choices,
        default=TIPO_INVENTARIO.CINQUILINO,
    )
    precio = models.FloatField(default=0,blank=True)
    precio_dolar = models.FloatField(null=True)
    precio_venta = models.FloatField(default=0,blank=True)
    precio_venta_dolar = models.FloatField(null=True)
    nro_dormitorios = models.IntegerField(default=1,blank=True )
    nro_banos = models.IntegerField(default=1, blank=True)
    valor_alquiler = models.FloatField(default=0, blank=True)
    unit_area = models.FloatField(  default=1)
    class Vista(models.TextChoices):
        INTERIOR = 'interior'
        EXTERIOR = 'exterior'
    vista = models.CharField(
        max_length=20,
        choices=Vista.choices,
        default=Vista.INTERIOR,
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
    piso = models.IntegerField(default=0, blank=True)
    valor_porcentaje_inicial = models.FloatField( blank=True, default=0)
    valor_porcentaje_financiado = models.FloatField( blank=True, default=0)
    tipo_departamento= models.CharField(max_length=200,blank=True,default="")
    valor_cuota = models.FloatField(default=0, blank=True)
    roi = models.FloatField(default=0, blank=True)
    tir = models.FloatField(default=0, blank=True)  
    renta = models.FloatField(default=0, blank=True) 
    class Etapa(models.TextChoices):
        PLANOS = 'planos'
        PREVENTA = 'preventa'
        CONSTRUCCION = 'construccion'
        ENTREGA_INMEDIATA = 'inmediata'

    etapa = models.CharField(
        max_length=20,
        choices=Etapa.choices,
        default=Etapa.ENTREGA_INMEDIATA,
    )
    areas_comunes = models.BooleanField(default=False)
    piscina= models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    coworking = models.BooleanField(default=False)
    cine = models.BooleanField(default=False)
    parrilla = models.BooleanField(default=False)
    sum = models.BooleanField(default=False)
    bicicleta = models.BooleanField(default=False)
    web = models.BooleanField(default=False) 
    bar = models.BooleanField(default=False) 
    monto_inicial = models.FloatField(default=0)
    
    
        # parametros analizer
    # dias_vacancia=models.FloatField(null=False,  default=0)
    # costo_porcentaje_operativo=models.FloatField(null=False,  default=0)
    # costo_porcentaje_administrativo=models.FloatField(null=False,  default=0)
    # costo_porcentaje_instalacion=models.FloatField(null=False,  default=0)
    # corretaje= models.BooleanField(default=False) 
    # tasa_credito= models.FloatField(null=False,  default=0.06)
    # costo_porcentaje_capex_reparaciones=models.FloatField(null=False,  default=0) #gastos de capital
    # plazo_meses = models.IntegerField(default=300)
    descuento_porcentaje_preventa=models.FloatField(null=False,  default=0)  
    # costo_porcentaje_administrativos_venta=models.FloatField(null=False,  default=0) #costo de cierre
    coordenada_A=models.FloatField(null=True)
    coordenada_B=models.FloatField(null=True)
    
    

    patrimonio_inicial =  models.FloatField(default=0)
    patrimonio_anio_5 =  models.FloatField(default=0)
    patrimonio_anio_10 =  models.FloatField(default=0)
    patrimonio_anio_20 =  models.FloatField(default=0)
    patrimonio_anio_30 =  models.FloatField(default=0)
    def __str__(self):
        return f'Departamento en {self.nombre}'





