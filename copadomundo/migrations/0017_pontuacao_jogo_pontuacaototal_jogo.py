# Generated by Django 4.0.5 on 2022-11-25 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copadomundo', '0016_resultado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pontuacao',
            name='Jogo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pontuacaototal',
            name='Jogo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
