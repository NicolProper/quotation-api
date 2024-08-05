# Generated by Django 4.0.4 on 2024-08-04 16:35

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
            name='Proyecto_Workshop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('frase', models.CharField(default='', max_length=1000)),
                ('parrafo', models.CharField(default='', max_length=3000)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyects.proyecto')),
            ],
        ),
    ]
