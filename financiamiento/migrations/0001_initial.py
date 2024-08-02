# Generated by Django 4.0.4 on 2024-08-01 02:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('dni', models.CharField(max_length=20)),
                ('ingresos', models.FloatField(default=0)),
                ('deudas', models.FloatField(default=0)),
                ('tasa_interes', models.FloatField(default=0)),
                ('plazo_meses', models.IntegerField(default=0)),
                ('valor_porcentaje_inicial', models.FloatField(default=0)),
                ('valor_porcentaje_capacidad_deuda', models.FloatField(default=0)),
                ('banco', models.CharField(max_length=200)),
                ('financiamiento_max', models.FloatField(default=0)),
                ('asesor', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
