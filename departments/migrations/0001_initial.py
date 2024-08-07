# Generated by Django 4.0.4 on 2024-08-07 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientePostgres',
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
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_actualizacion', models.DateField(blank=True, null=True)),
                ('nro_depa', models.CharField(max_length=200)),
                ('unit_area', models.FloatField(default=1)),
                ('nro_dormitorios', models.IntegerField(default=1)),
                ('nro_banos', models.IntegerField(default=1)),
                ('piso', models.IntegerField(default=1)),
                ('vista', models.CharField(blank=True, choices=[('interior', 'Interior'), ('exterior', 'Exterior')], max_length=20)),
                ('tipo_moneda', models.CharField(choices=[('pen', 'Soles'), ('usd', 'Dolar')], default='pen', max_length=20)),
                ('tipo_inventario', models.CharField(choices=[('proyecto', 'Proyecto'), ('c/inquilino', 'Cinquilino')], default='proyecto', max_length=100)),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('tipo_departamento', models.CharField(default='', max_length=200)),
                ('precio', models.FloatField(default=0)),
                ('precio_dolar', models.FloatField(null=True)),
                ('precio_venta', models.FloatField(default=0)),
                ('precio_venta_dolar', models.FloatField(default=0)),
                ('monto_inicial', models.FloatField(default=0)),
                ('estatus', models.CharField(default='no disponible', max_length=100)),
                ('ocultar', models.BooleanField(default=False)),
                ('precio_workshop', models.FloatField(null=True)),
                ('valor_descuento_preventa', models.FloatField(null=True)),
                ('reservado', models.BooleanField(default=False)),
                ('valor_alquiler', models.FloatField(default=0)),
                ('roi', models.FloatField(default=0)),
                ('tir', models.FloatField(default=0)),
                ('valor_cuota', models.FloatField(default=0)),
                ('renta', models.FloatField(default=0)),
                ('patrimonio_inicial', models.FloatField(default=0)),
                ('patrimonio_anio_5', models.FloatField(default=0)),
                ('patrimonio_anio_10', models.FloatField(default=0)),
                ('patrimonio_anio_20', models.FloatField(default=0)),
                ('patrimonio_anio_30', models.FloatField(default=0)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyects.proyecto')),
            ],
        ),
    ]
