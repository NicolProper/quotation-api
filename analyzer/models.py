# models.py
from datetime import date, datetime
from django.db import models

class Analyzer(models.Model):
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

    def __str__(self):
        return self.name


