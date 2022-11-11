from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.

class Palpites(models.Model):
    gols = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
    )
    Rodada = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    CAT = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    EQU = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    HOL = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    SEN = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    EUA = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    ING = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    IRA = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    GAL = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    ARG = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    ARA = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    MEX = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    POL = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    AUS = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    DIN = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    FRA = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    TUN = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    ALE = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    CRC = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    ESP = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    JAP = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    BEL = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    CAN = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    CRO = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    MAR = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    BRA = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    CAM = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    SUI = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    SER = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    COR = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    GAN = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    POR = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    GAN = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)

class Horarios(models.Model):
    GRUPOS = (
        ('Grupo A', 'Grupo A'),
        ('Grupo B', 'Grupo B'),
        ('Grupo C', 'Grupo C'),
        ('Grupo D', 'Grupo D'),
        ('Grupo E', 'Grupo E'),
        ('Grupo F', 'Grupo F'),
        ('Grupo G', 'Grupo G'),
        ('Grupo H', 'Grupo H'),
    )
    Rodada = models.IntegerField()
    Jogo1 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ1 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo2 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ2 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo3 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ3 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo4 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ4 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo5 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ5 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo6 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ6 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo7 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ7 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo8 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ8 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo9 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ9 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo10 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ10 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo11 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ11 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo12 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ12 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo13 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ13 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo14 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ14 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo15 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ15 = models.CharField(max_length=8, choices=GRUPOS)
    Jogo16 = models.DateTimeField('data/hora', null=True, blank=True)
    GrupoJ16 = models.CharField(max_length=8, choices=GRUPOS)

class Resultados(models.Model):
    RODADAS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    )
    Rodada = models.CharField(max_length=2, choices=RODADAS)
    CAT = models.PositiveSmallIntegerField(null=True, blank=True)
    EQU = models.PositiveSmallIntegerField(null=True, blank=True)
    HOL = models.PositiveSmallIntegerField(null=True, blank=True)
    SEN = models.PositiveSmallIntegerField(null=True, blank=True)
    EUA = models.PositiveSmallIntegerField(null=True, blank=True)
    ING = models.PositiveSmallIntegerField(null=True, blank=True)
    IRA = models.PositiveSmallIntegerField(null=True, blank=True)
    GAL = models.PositiveSmallIntegerField(null=True, blank=True)
    ARG = models.PositiveSmallIntegerField(null=True, blank=True)
    ARA = models.PositiveSmallIntegerField(null=True, blank=True)
    MEX = models.PositiveSmallIntegerField(null=True, blank=True)
    POL = models.PositiveSmallIntegerField(null=True, blank=True)
    AUS = models.PositiveSmallIntegerField(null=True, blank=True)
    DIN = models.PositiveSmallIntegerField(null=True, blank=True)
    FRA = models.PositiveSmallIntegerField(null=True, blank=True)
    TUN = models.PositiveSmallIntegerField(null=True, blank=True)
    ALE = models.PositiveSmallIntegerField(null=True, blank=True)
    CRC = models.PositiveSmallIntegerField(null=True, blank=True)
    ESP = models.PositiveSmallIntegerField(null=True, blank=True)
    JAP = models.PositiveSmallIntegerField(null=True, blank=True)
    BEL = models.PositiveSmallIntegerField(null=True, blank=True)
    CAN = models.PositiveSmallIntegerField(null=True, blank=True)
    CRO = models.PositiveSmallIntegerField(null=True, blank=True)
    MAR = models.PositiveSmallIntegerField(null=True, blank=True)
    BRA = models.PositiveSmallIntegerField(null=True, blank=True)
    CAM = models.PositiveSmallIntegerField(null=True, blank=True)
    SUI = models.PositiveSmallIntegerField(null=True, blank=True)
    SER = models.PositiveSmallIntegerField(null=True, blank=True)
    COR = models.PositiveSmallIntegerField(null=True, blank=True)
    GAN = models.PositiveSmallIntegerField(null=True, blank=True)
    POR = models.PositiveSmallIntegerField(null=True, blank=True)
    URU = models.PositiveSmallIntegerField(null=True, blank=True)

class Ordenacao(models.Model):
    RODADAS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
    )
    TIMES = (
        ('CAT', 'CAT'),
        ('EQU', 'EQU'),
        ('HOL', 'HOL'),
        ('SEN', 'SEN'),
        ('EUA', 'EUA'),
        ('ING', 'ING'),
        ('IRA', 'IRA'),
        ('GAL', 'GAL'),
        ('ARG', 'ARG'),
        ('ARA', 'ARA'),
        ('MEX', 'MEX'),
        ('POL', 'POL'),
        ('AUS', 'AUS'),
        ('FRA', 'FRA'),
        ('TUN', 'TUN'),
        ('DIN', 'DIN'),
        ('ALE', 'ALE'),
        ('CRC', 'CRC'),
        ('ESP', 'ESP'),
        ('JAP', 'JAP'),
        ('BEL', 'BEL'),
        ('CAN', 'CAN'),
        ('CRO', 'CRO'),
        ('MAR', 'MAR'),
        ('BRA', 'BRA'),
        ('CAM', 'CAM'),
        ('SUI', 'SUI'),
        ('SER', 'SER'),
        ('COR', 'COR'),
        ('GAN', 'GAN'),
        ('POR', 'POR'),
        ('URU', 'URU'),
    )
    Rodada = models.CharField(max_length=2, choices=RODADAS)
    CAT = models.CharField(max_length=14, choices=TIMES)
    EQU = models.CharField(max_length=14, choices=TIMES)
    HOL = models.CharField(max_length=14, choices=TIMES)
    SEN = models.CharField(max_length=14, choices=TIMES)
    EUA = models.CharField(max_length=14, choices=TIMES)
    ING = models.CharField(max_length=14, choices=TIMES)
    IRA = models.CharField(max_length=14, choices=TIMES)
    GAL = models.CharField(max_length=14, choices=TIMES)
    ARG = models.CharField(max_length=14, choices=TIMES)
    ARA = models.CharField(max_length=14, choices=TIMES)
    MEX = models.CharField(max_length=14, choices=TIMES)
    POL = models.CharField(max_length=14, choices=TIMES)
    AUS = models.CharField(max_length=14, choices=TIMES)
    DIN = models.CharField(max_length=14, choices=TIMES)
    FRA = models.CharField(max_length=14, choices=TIMES)
    TUN = models.CharField(max_length=14, choices=TIMES)
    ALE = models.CharField(max_length=14, choices=TIMES)
    CRC = models.CharField(max_length=14, choices=TIMES)
    ESP = models.CharField(max_length=14, choices=TIMES)
    JAP = models.CharField(max_length=14, choices=TIMES)
    BEL = models.CharField(max_length=14, choices=TIMES)
    CAN = models.CharField(max_length=14, choices=TIMES)
    CRO = models.CharField(max_length=14, choices=TIMES)
    MAR = models.CharField(max_length=14, choices=TIMES)
    BRA = models.CharField(max_length=14, choices=TIMES)
    CAM = models.CharField(max_length=14, choices=TIMES)
    SUI = models.CharField(max_length=14, choices=TIMES)
    SER = models.CharField(max_length=14, choices=TIMES)
    COR = models.CharField(max_length=14, choices=TIMES)
    GAN = models.CharField(max_length=14, choices=TIMES)
    POR = models.CharField(max_length=14, choices=TIMES)
    URU = models.CharField(max_length=14, choices=TIMES)


class Pontuacao(models.Model):
    RODADAS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Rodada = models.IntegerField(choices=RODADAS)
    RE = models.IntegerField(null=True)
    RB = models.IntegerField(null=True)
    RP = models.IntegerField(null=True)
    GV = models.IntegerField(null=True)
    GP = models.IntegerField(null=True)
    ER = models.IntegerField(null=True)
    PONTOS = models.IntegerField()

class PontuacaoTotal(models.Model):
    RODADAS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Rodada = models.IntegerField(choices=RODADAS)
    RE = models.IntegerField(null=True)
    RB = models.IntegerField(null=True)
    RP = models.IntegerField(null=True)
    GV = models.IntegerField(null=True)
    GP = models.IntegerField(null=True)
    ER = models.IntegerField(null=True)
    PONTOS = models.IntegerField()

class Ligas(models.Model):
    title = models.CharField(max_length=30)
    users = models.ManyToManyField(User, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)