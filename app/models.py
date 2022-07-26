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

class Brasileirao(models.Model):
    Rodada = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    AthleticoPR = models.IntegerField()
    Palmeiras = models.IntegerField()
    Corinthians = models.IntegerField()
    Internacional = models.IntegerField()
    AtleticoMG = models.IntegerField()
    Fluminense = models.IntegerField()
    Santos = models.IntegerField()
    SaoPaulo = models.IntegerField()
    Flamengo = models.IntegerField()
    Botafogo = models.IntegerField()
    Avai = models.IntegerField()
    Bragantino = models.IntegerField()
    AtleticoGO = models.IntegerField()
    Goias = models.IntegerField()
    Ceara = models.IntegerField()
    Coritiba = models.IntegerField()
    AmericaMG = models.IntegerField()
    Cuiaba = models.IntegerField()
    Juventude = models.IntegerField()
    Fortaleza = models.IntegerField()

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
    AthleticoPR = models.IntegerField()
    Palmeiras = models.IntegerField()
    Corinthians = models.IntegerField()
    Internacional = models.IntegerField()
    AtleticoMG = models.IntegerField()
    Fluminense = models.IntegerField()
    Santos = models.IntegerField()
    SaoPaulo = models.IntegerField()
    Flamengo = models.IntegerField()
    Botafogo = models.IntegerField()
    Avai = models.IntegerField()
    Bragantino = models.IntegerField()
    AtleticoGO = models.IntegerField()
    Goias = models.IntegerField()
    Ceara = models.IntegerField()
    Coritiba = models.IntegerField()
    AmericaMG = models.IntegerField()
    Cuiaba = models.IntegerField()
    Juventude = models.IntegerField()
    Fortaleza = models.IntegerField()


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Rodada = models.CharField(max_length=2, choices=RODADAS)
    Jogo1 = models.IntegerField()
    Jogo2 = models.IntegerField()
    Jogo3 = models.IntegerField()
    Jogo4 = models.IntegerField()
    Jogo5 = models.IntegerField()
    Jogo6 = models.IntegerField()
    Jogo7 = models.IntegerField()
    Jogo8 = models.IntegerField()
    Jogo9 = models.IntegerField()
    Jogo10 = models.IntegerField()
    RE = models.IntegerField()
    RB = models.IntegerField()
    RP = models.IntegerField()
    PONTOS = models.IntegerField()
