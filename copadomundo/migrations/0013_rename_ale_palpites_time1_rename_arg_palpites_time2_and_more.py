# Generated by Django 4.0.5 on 2022-11-18 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copadomundo', '0012_alter_jogos_jogo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='palpites',
            old_name='ALE',
            new_name='time1',
        ),
        migrations.RenameField(
            model_name='palpites',
            old_name='ARG',
            new_name='time2',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='ARA',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='AUS',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='BEL',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='BRA',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='CAM',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='CAN',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='CAT',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='COR',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='CRC',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='CRO',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='DIN',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='EQU',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='ESP',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='EUA',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='FRA',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='GAL',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='GAN',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='HOL',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='ING',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='IRA',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='JAP',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='MAR',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='MEX',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='POL',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='POR',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='SEN',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='SER',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='SUI',
        ),
        migrations.RemoveField(
            model_name='palpites',
            name='TUN',
        ),
    ]
