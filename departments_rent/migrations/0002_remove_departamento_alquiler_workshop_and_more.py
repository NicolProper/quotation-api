# Generated by Django 4.0.4 on 2024-08-08 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments_rent', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departamento_alquiler',
            name='workshop',
        ),
        migrations.AddField(
            model_name='departamento_alquiler',
            name='monto_inicial',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='departamento_alquiler',
            name='precio_venta',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='departamento_alquiler',
            name='precio_venta_dolar',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='departamento_alquiler',
            name='etapa',
            field=models.CharField(choices=[('planos', 'Planos'), ('preventa', 'Preventa'), ('construccion', 'Construccion'), ('inmediata', 'Entrega Inmediata')], default='inmediata', max_length=20),
        ),
        migrations.AlterField(
            model_name='departamento_alquiler',
            name='nombre',
            field=models.CharField(default='', max_length=200, unique=True),
        ),
    ]