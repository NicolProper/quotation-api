# Generated by Django 4.0.4 on 2024-08-08 16:31

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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('tipodoc', models.CharField(max_length=100)),
                ('nrodoc', models.CharField(max_length=10)),
                ('email', models.IntegerField()),
                ('edadrango', models.CharField(max_length=100)),
                ('nrocelular', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'cliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bancaria',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('apellido_materno', models.CharField(default='', max_length=200)),
                ('apellido_paterno', models.CharField(default='', max_length=200)),
                ('fecha_nacimiento', models.DateField(default='2000-02-01')),
                ('dni', models.CharField(max_length=20)),
                ('edad', models.IntegerField(default=0)),
                ('residencia', models.CharField(choices=[('Perú', 'Peru'), ('Extranjero', 'Extranjero')], default='Perú', max_length=20)),
                ('primera_vivienda', models.CharField(choices=[('SÍ', 'Si'), ('NO', 'No')], default='SÍ', max_length=10)),
                ('ingreso_primera_categoria', models.FloatField(default=0)),
                ('ingreso_segunda_categoria', models.FloatField(default=0)),
                ('ingreso_tercera_categoria', models.FloatField(default=0)),
                ('ingreso_cuarta_categoria', models.FloatField(default=0)),
                ('ingreso_quinta_categoria', models.FloatField(default=0)),
                ('cuota_vehicular', models.FloatField(default=0)),
                ('cuota_personal', models.FloatField(default=0)),
                ('cuota_tarjeta_credito', models.FloatField(default=0)),
                ('cuota_inicial', models.FloatField(default=0)),
                ('cuota_hipotecaria', models.FloatField(default=0)),
                ('continuidad_laboral', models.IntegerField(default=0)),
            ],
        ),
    ]
