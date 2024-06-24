from django_filters import rest_framework as filters
from .models import Proyecto
from django_filters import NumberFilter

class PriceRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = [float(val) for val in value.split(',')]
            # print(f'min_price: {min_price}, max_price: {max_price}')
            return qs.filter(precio_desde__range=(min_price, max_price))
        return qs
    
    
class RoiRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_roi, max_roi = [float(val) for val in value.split(',')]
            
            return qs.filter(roi__range=(min_roi/100, max_roi/100))
        return qs
    
    
    
class AlquilerRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = [float(val) for val in value.split(',')]
            # print(f'min_price: {min_price}, max_price: {max_price}')
            return qs.filter(alquiler__range=(min_price, max_price))
        return qs


class CuotaRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = [float(val) for val in value.split(',')]
            # print(f'min_price: {min_price}, max_price: {max_price}')
            return qs.filter(cuota__range=(min_price, max_price))
        return qs 
    
    
class ValorAlquilerRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = [float(val) for val in value.split(',')]
            # print(f'min_price: {min_price}, max_price: {max_price}')
            return qs.filter(valor_inicial__range=(min_price, max_price))
        return qs 

ETAPAS = (
    ('planos', 'planos'),
    ('preventa', 'preventa'),
    ('construccion', 'construccion'),
    ('inmediata', 'inmediata'),
)


class ProyectosFilter(filters.FilterSet):
    precio_desde = PriceRangeFilter(field_name='precio_desde')
    roi= RoiRangeFilter(field_name="roi")
    alquiler= AlquilerRangeFilter(field_name="alquiler")
    cuota= CuotaRangeFilter(field_name="cuota")
    valor_inicial= ValorAlquilerRangeFilter( field_name="valor_inicial")
    area_desde = NumberFilter(field_name='area_desde',  lookup_expr='gte')
    area_hasta = NumberFilter(field_name='area_hasta', lookup_expr='lte')
    dorms_desde = NumberFilter(field_name='dorms_desde', lookup_expr='gte')
    dorms_hasta = NumberFilter(field_name='dorms_hasta', lookup_expr='lte')
    banos_desde = NumberFilter(field_name='banos_desde', lookup_expr='gte')
    banos_hasta = NumberFilter(field_name='banos_hasta', lookup_expr='lte')
 
    
    # etapa mutiple choice
    etapa = filters.MultipleChoiceFilter(choices=ETAPAS)

    class Meta:
        model = Proyecto
        fields = ['distrito', 'banco','etapa', 'precio_desde', 'id',  "valor_inicial"]
