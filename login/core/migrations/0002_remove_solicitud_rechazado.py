# Generated by Django 5.0.6 on 2024-06-21 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='rechazado',
        ),
    ]
