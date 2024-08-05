# models.py
from datetime import date, datetime
from django.db import models

class Variable(models.Model):
    TIPO_CHOICES = (
        ('str', 'String'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('date', 'Date'),
    )

    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return self.name

    def get_value(self):
        if self.tipo == 'int':
            return int(self.value)
        elif self.tipo == 'float':
            return float(self.value)
        elif self.tipo == 'date':
            return datetime.strptime(self.value, '%Y-%m-%d').date()
        return self.value

    def set_value(self, val):
        if isinstance(val, int):
            self.tipo = 'int'
        elif isinstance(val, float):
            self.tipo = 'float'
        elif isinstance(val, date):
            self.tipo = 'date'
            val = val.strftime('%Y-%m-%d')
        else:
            self.tipo = 'str'
        self.value = str(val)
