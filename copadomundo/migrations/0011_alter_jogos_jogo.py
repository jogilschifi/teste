# Generated by Django 4.0.5 on 2022-11-17 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copadomundo', '0010_jogos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogos',
            name='Jogo',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16)], max_length=2),
        ),
    ]
