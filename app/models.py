from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PalpitesPGL(models.Model):
    placar = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    FaZe_V = models.IntegerField(choices=placar)
    FaZe_D = models.IntegerField(choices=placar)
    Spirit_V = models.IntegerField(choices=placar)
    Spirit_D = models.IntegerField(choices=placar)
    Vitality_V = models.IntegerField(choices=placar)
    Vitality_D = models.IntegerField(choices=placar)
    MOUZ_V = models.IntegerField(choices=placar)
    MOUZ_D = models.IntegerField(choices=placar)
    Virtuspro_V = models.IntegerField(choices=placar)
    Virtuspro_D = models.IntegerField(choices=placar)
    NatusVincere_V = models.IntegerField(choices=placar)
    NatusVincere_D = models.IntegerField(choices=placar)
    G2_V = models.IntegerField(choices=placar)
    G2_D = models.IntegerField(choices=placar)
    Complexity_V = models.IntegerField(choices=placar)
    Complexity_D = models.IntegerField(choices=placar)
    Heroic_V = models.IntegerField(choices=placar)
    Heroic_D = models.IntegerField(choices=placar)
    Cloud9_V = models.IntegerField(choices=placar)
    Cloud9_D = models.IntegerField(choices=placar)
    EternalFire_V = models.IntegerField(choices=placar)
    EternalFire_D = models.IntegerField(choices=placar)
    paiN_V = models.IntegerField(choices=placar)
    paiN_D = models.IntegerField(choices=placar)
    ECSTATIC_V = models.IntegerField(choices=placar)
    ECSTATIC_D = models.IntegerField(choices=placar)
    TheMongolz_V = models.IntegerField(choices=placar)
    TheMongolz_D = models.IntegerField(choices=placar)
    Imperial_V = models.IntegerField(choices=placar)
    Imperial_D = models.IntegerField(choices=placar)
    FURIA_V = models.IntegerField(choices=placar)
    FURIA_D = models.IntegerField(choices=placar)


class PalpitesFormula1(models.Model):
    pilotos = (
        ('Max Verstappen', 'Max Verstappen'),
        ('Logan Sargeant', 'Logan Sargeant'),
        ('Daniel Ricciardo', 'Daniel Ricciardo'),
        ('Lando Norris', 'Lando Norris'),
        ('Pierre Gasly', 'Pierre Gasly'),
        ('Sergio Perez', 'Sergio Perez'),
        ('Fernando Alonso', 'Fernando Alonso'),
        ('Charles Leclerc', 'Charles Leclerc'),
        ('Lance Stroll', 'Lance Stroll'),
        ('Kevin Magnussen', 'Kevin Magnussen'),
        ('Yuki Tsunoda', 'Yuki Tsunoda'),
        ('Alexander Albon', 'Alexander Albon'),
        ('Guan Yu Zhou', 'Guan Yu Zhou'),
        ('Nico Hulkenberg', 'Nico Hulkenberg'),
        ('Esteban Ocon', 'Esteban Ocon'),
        ('Lewis Hamilton', 'Lewis Hamilton'),
        ('Carlos Sainz Jr.', 'Carlos Sainz Jr.'),
        ('George Russell', 'George Russell'),
        ('Valtteri Bottas', 'Valtteri Bottas'),
        ('Oscar Piastri', 'Oscar Piastri'),
    )
    equipes = (
        ('Red Bull Racing', 'Red Bull Racing'),
        ('Williams', 'Williams'),
        ('AlphaTauri', 'AlphaTauri'),
        ('McLaren', 'McLaren'),
        ('Alpine', 'Alpine'),
        ('Aston Martin Racing', 'Aston Martin Racing'),
        ('Hass F1 Team', 'Hass F1 Team'),
        ('Sauber', 'Sauber'),
        ('Ferrari', 'Ferrari'),
        ('Mercedes', 'Mercedes'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    PrimeiroColocado = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    SegundoColocado = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    TerceiroColocado = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    Voltamaisrapida = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    Quemnaofinalizaaprova = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    Quembate = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    Quemganhamaisposicoes = models.CharField(max_length=20, choices=pilotos, null=True, blank=True)
    Equipe = models.CharField(max_length=20, choices=equipes, null=True, blank=True)

class PontuacaoF1(models.Model):
    Etapa = (
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
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Etapa = models.IntegerField(choices=Etapa)
    PrimeiroColocado = models.IntegerField(null=True)
    SegundoColocado = models.IntegerField(null=True)
    TerceiroColocado = models.IntegerField(null=True)
    Podio = models.IntegerField(null=True)
    Voltamaisrapida = models.IntegerField(null=True)
    Quemnaofinalizaaprova = models.IntegerField(null=True)
    Quembate = models.IntegerField(null=True)
    Equipe = models.IntegerField(null=True)
    Pts = models.IntegerField()

class PontuacaoTotalF1(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Etapa = models.IntegerField()
    PrimeiroColocado = models.IntegerField(null=True)
    SegundoColocado = models.IntegerField(null=True)
    TerceiroColocado = models.IntegerField(null=True)
    Podio = models.IntegerField(null=True)
    Voltamaisrapida = models.IntegerField(null=True)
    Quemnaofinalizaaprova = models.IntegerField(null=True)
    Quembate = models.IntegerField(null=True)
    Equipe = models.IntegerField(null=True)
    Pts = models.IntegerField()

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
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
    )
    Rodada = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    AthleticoPR = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Palmeiras = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Corinthians = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Internacional = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    AtleticoMG = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Fluminense = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Santos = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    SaoPaulo = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Flamengo = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Botafogo = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Avai = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Bragantino = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    AtleticoGO = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Goias = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Ceara = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Coritiba = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    AmericaMG = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Cuiaba = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Juventude = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)
    Fortaleza = models.PositiveSmallIntegerField(choices=gols, null=True, blank=True)

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
