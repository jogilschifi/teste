# Generated by Django 4.0.5 on 2022-10-19 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_corinthianspenalti_copadobrasil_penalti_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copadobrasil',
            name='Rodada',
        ),
    ]
