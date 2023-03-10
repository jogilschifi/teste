# Generated by Django 4.0.5 on 2022-11-21 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copadomundo', '0015_alter_palpites_time1_alter_palpites_time2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rodada', models.IntegerField()),
                ('Jogo', models.IntegerField(blank=True, null=True)),
                ('time1', models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)])),
                ('time2', models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)])),
            ],
        ),
    ]
