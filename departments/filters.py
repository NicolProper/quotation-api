from django_filters import rest_framework as filters
from .models import Departamento
from django_filters import NumberFilter


class PriceRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = [float(val) for val in value.split(',')]
            print(f'min_price: {min_price}, max_price: {max_price}')
            return qs.filter(precio__range=(min_price, max_price))
        return qs
    
class ValorAlquilerFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = [float(val) for val in value.split(',')]
            print(f'min_price: {min_price}, max_price: {max_price}')
            return qs.filter(valor_alquiler__range=(min_price, max_price))
        return qs
    
class DepartamentoFilter(filters.FilterSet):
    valor_alquiler = ValorAlquilerFilter(field_name='valor_alquiler')
    class Meta:
        model = Departamento
        fields = ['proyecto', 'nro_banos', 'nro_dormitorios', 'precio', 'valor_alquiler']   
    
    
class TirRangeFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            print('value', value), 
            
            min_tir, max_tir = [float(val) for val in value.split(',')]
            print(f'min_tir: {min_tir}, max_tir: {max_tir}')
            return qs.filter(tir__range=(min_tir, max_tir))
        return qs


class RoiRangeFilter(filters.Filter):
    print('emtre')
    def filter(self, qs, value):
        if value:
            min_roi, max_roi = [float(val) for val in value.split(',')]
            print(f'min_roi: {min_roi}, max_roi: {max_roi}')
            return qs.filter(roi__range=(min_roi, max_roi))
        return qs


class DepartamentoFilter2(filters.FilterSet):
    
    
    tir = TirRangeFilter(field_name='tir')
    roi = RoiRangeFilter(field_name='roi')
    precio = PriceRangeFilter(field_name='precio')


    class Meta:
        model = Departamento
        fields = ['precio']


