from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Clubes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    athleticoPR = models.IntegerField()
    libertad = models.IntegerField()
    fortaleza = models.IntegerField()
    estudiantes = models.IntegerField()
    cerroPorteno = models.IntegerField()
    palmeiras = models.IntegerField()
    emelec = models.IntegerField()
    atleticoMG = models.IntegerField()
    tolima = models.IntegerField()
    flamengo = models.IntegerField()
    corinthians = models.IntegerField()
    bocaJuniors = models.IntegerField()
    talleres = models.IntegerField()
    colon = models.IntegerField()
    velezSarsfield = models.IntegerField()
    riverPlate = models.IntegerField()

class CopadoBrasil(models.Model):
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
    )
    opcao = (
        ('corinthians', 'corinthians'),
        ('flamengo', 'flamengo'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    CorinthiansTempoNormal = models.PositiveSmallIntegerField(choices=gols)
    FlamengoTempoNormal = models.PositiveSmallIntegerField(choices=gols)
    CorinthiansProrrogacao = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    FlamengoProrrogacao = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Penalti = models.CharField(max_length=15, choices=opcao, null=True, blank=True)

class ResultadosCopadoBrasil(models.Model):
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
    )
    opcao = (
        ('corinthians', 'corinthians'),
        ('flamengo', 'flamengo'),
    )
    CorinthiansTempoNormal = models.PositiveSmallIntegerField(choices=gols)
    FlamengoTempoNormal = models.PositiveSmallIntegerField(choices=gols)
    CorinthiansProrrogacao = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    FlamengoProrrogacao = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Penalti = models.CharField(max_length=15, choices=opcao, null=True, blank=True)

class Brasileirao(models.Model):
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
    )
    Rodada = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    AthleticoPR = models.PositiveSmallIntegerField(choices=gols)
    Palmeiras = models.PositiveSmallIntegerField(choices=gols)
    Corinthians = models.PositiveSmallIntegerField(choices=gols)
    Internacional = models.PositiveSmallIntegerField(choices=gols)
    AtleticoMG = models.PositiveSmallIntegerField(choices=gols)
    Fluminense = models.PositiveSmallIntegerField(choices=gols)
    Santos = models.PositiveSmallIntegerField(choices=gols)
    SaoPaulo = models.PositiveSmallIntegerField(choices=gols)
    Flamengo = models.PositiveSmallIntegerField(choices=gols)
    Botafogo = models.PositiveSmallIntegerField(choices=gols)
    Avai = models.PositiveSmallIntegerField(choices=gols)
    Bragantino = models.PositiveSmallIntegerField(choices=gols)
    AtleticoGO = models.PositiveSmallIntegerField(choices=gols)
    Goias = models.PositiveSmallIntegerField(choices=gols)
    Ceara = models.PositiveSmallIntegerField(choices=gols)
    Coritiba = models.PositiveSmallIntegerField(choices=gols)
    AmericaMG = models.PositiveSmallIntegerField(choices=gols)
    Cuiaba = models.PositiveSmallIntegerField(choices=gols)
    Juventude = models.PositiveSmallIntegerField(choices=gols)
    Fortaleza = models.PositiveSmallIntegerField(choices=gols)

class ResultadosBrasileirao(models.Model):
    RODADAS = (
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
    )
    Rodada = models.CharField(max_length=2, choices=RODADAS)
    AthleticoPR = models.IntegerField(null=True, blank=True)
    Palmeiras = models.IntegerField(null=True, blank=True)
    Corinthians = models.IntegerField(null=True, blank=True)
    Internacional = models.IntegerField(null=True, blank=True)
    AtleticoMG = models.IntegerField(null=True, blank=True)
    Fluminense = models.IntegerField(null=True, blank=True)
    Santos = models.IntegerField(null=True, blank=True)
    SaoPaulo = models.IntegerField(null=True, blank=True)
    Flamengo = models.IntegerField(null=True, blank=True)
    Botafogo = models.IntegerField(null=True, blank=True)
    Avai = models.IntegerField(null=True, blank=True)
    Bragantino = models.IntegerField(null=True, blank=True)
    AtleticoGO = models.IntegerField(null=True, blank=True)
    Goias = models.IntegerField(null=True, blank=True)
    Ceara = models.IntegerField(null=True, blank=True)
    Coritiba = models.IntegerField(null=True, blank=True)
    AmericaMG = models.IntegerField(null=True, blank=True)
    Cuiaba = models.IntegerField(null=True, blank=True)
    Juventude = models.IntegerField(null=True, blank=True)
    Fortaleza = models.IntegerField(null=True, blank=True)

    def to_python(self, value):
        """
        Validate that int() can be called on the input. Return the result
        of int() or None for empty values.
        """
        value = super().to_python(value)
        if value in self.empty_values:
            return None

class OrdenacaoBrasileirao(models.Model):
    RODADAS = (
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
    )
    TIMES = (
        ('AthleticoPR', 'AthleticoPR'),
        ('Palmeiras', 'Palmeiras'),
        ('Corinthians', 'Corinthians'),
        ('Internacional', 'Internacional'),
        ('AtleticoMG', 'AtleticoMG'),
        ('Fluminense', 'Fluminense'),
        ('Santos', 'Santos'),
        ('SaoPaulo', 'SaoPaulo'),
        ('Flamengo', 'Flamengo'),
        ('Botafogo', 'Botafogo'),
        ('Avai', 'Avai'),
        ('Bragantino', 'Bragantino'),
        ('AtleticoGO', 'AtleticoGO'),
        ('Goias', 'Goias'),
        ('Ceara', 'Ceara'),
        ('Coritiba', 'Coritiba'),
        ('AmericaMG', 'AmericaMG'),
        ('Cuiaba', 'Cuiaba'),
        ('Juventude', 'Juventude'),
        ('Fortaleza', 'Fortaleza'),
    )
    Rodada = models.CharField(max_length=2, choices=RODADAS)
    AthleticoPR = models.CharField(max_length=14, choices=TIMES)
    Palmeiras = models.CharField(max_length=14, choices=TIMES)
    Corinthians = models.CharField(max_length=14, choices=TIMES)
    Internacional = models.CharField(max_length=14, choices=TIMES)
    AtleticoMG = models.CharField(max_length=14, choices=TIMES)
    Fluminense = models.CharField(max_length=14, choices=TIMES)
    Santos = models.CharField(max_length=14, choices=TIMES)
    SaoPaulo = models.CharField(max_length=14, choices=TIMES)
    Flamengo = models.CharField(max_length=14, choices=TIMES)
    Botafogo = models.CharField(max_length=14, choices=TIMES)
    Avai = models.CharField(max_length=14, choices=TIMES)
    Bragantino = models.CharField(max_length=14, choices=TIMES)
    AtleticoGO = models.CharField(max_length=14, choices=TIMES)
    Goias = models.CharField(max_length=14, choices=TIMES)
    Ceara = models.CharField(max_length=14, choices=TIMES)
    Coritiba = models.CharField(max_length=14, choices=TIMES)
    AmericaMG = models.CharField(max_length=14, choices=TIMES)
    Cuiaba = models.CharField(max_length=14, choices=TIMES)
    Juventude = models.CharField(max_length=14, choices=TIMES)
    Fortaleza = models.CharField(max_length=14, choices=TIMES)

class PontuacaoBrasileirao(models.Model):
    RODADAS = (
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31),
        (32, 32),
        (33, 33),
        (34, 34),
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Rodada = models.IntegerField(choices=RODADAS)
    RE = models.IntegerField(null=True)
    RB = models.IntegerField(null=True)
    RP = models.IntegerField(null=True)
    ER = models.IntegerField(null=True)
    PONTOS = models.IntegerField()


class PontuacaoTotalBrasileirao(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Rodada = models.IntegerField()
    RE = models.IntegerField(null=True)
    RB = models.IntegerField(null=True)
    RP = models.IntegerField(null=True)
    ER = models.IntegerField(null=True)
    PONTOS = models.IntegerField()
