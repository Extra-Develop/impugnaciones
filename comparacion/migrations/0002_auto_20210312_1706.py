# Generated by Django 2.2.16 on 2021-03-12 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comparacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fantasma',
            options={'verbose_name': 'Fantasma', 'verbose_name_plural': 'Fantasmas'},
        ),
        migrations.AlterModelOptions(
            name='votacion',
            options={'ordering': ['cod'], 'verbose_name': 'Votación', 'verbose_name_plural': 'Votaciones'},
        ),
    ]
