# Generated by Django 4.0.4 on 2024-08-07 18:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento_Workshop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_workshop', models.DateField()),
                ('nro_depa', models.CharField(max_length=200)),
                ('precio', models.FloatField(default=0)),
                ('precio_workshop', models.FloatField(default=0)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyects.proyecto')),
            ],
        ),
    ]
