# Generated by Django 4.0.4 on 2024-08-01 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyects', '0001_initial'),
        ('project_workshop', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProyectoWorkshop',
            new_name='Proyecto_Workshop',
        ),
    ]