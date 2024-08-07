# Generated by Django 4.0.4 on 2024-08-07 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('str', 'String'), ('int', 'Integer'), ('float', 'Float'), ('date', 'Date')], max_length=10)),
            ],
        ),
    ]
