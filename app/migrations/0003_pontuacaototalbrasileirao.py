# Generated by Django 4.0.5 on 2022-09-01 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_remove_pontuacaobrasileirao_jogo1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PontuacaoTotalBrasileirao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rodada', models.IntegerField()),
                ('RE', models.IntegerField()),
                ('RB', models.IntegerField()),
                ('RP', models.IntegerField()),
                ('PONTOS', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
