# Generated by Django 4.1 on 2024-04-30 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_usuario_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioBloqueado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
