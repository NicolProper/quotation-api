# Generated by Django 4.0.4 on 2024-07-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financiamiento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='asesor',
            field=models.CharField(default='', max_length=200),
        ),
    ]
