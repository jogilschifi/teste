from django.db import models

# Create your models here.
class Jogos(models.Model):
    JOGOS = (
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
        (16, 16),
    )
    ESTADIOS = (
        ('ARENA DO GRÊMIO ', 'ARENA DO GRÊMIO '),
        ('MINEIRÃO', 'MINEIRÃO'),
        ('NEO QUÍMICA ARENA', 'NEO QUÍMICA ARENA'),
        ('ILHA DO RETIRO', 'ILHA DO RETIRO'),
        ('MORUMBI', 'MORUMBI'),
        ('INDEPENDÊNCIA', 'INDEPENDÊNCIA'),
        ('BEIRA-RIO', 'BEIRA-RIO'),
        ('ARENA DA BAIXADA', 'ARENA DA BAIXADA'),
        ('NILTON SANTOS', 'NILTON SANTOS'),
        ('MARACANÃ', 'MARACANÃ'),
        ('VILA BELMIRO', 'VILA BELMIRO'),
        ('ITAIPAVA ARENA FONTE NOVA', 'ITAIPAVA ARENA FONTE NOVA'),
        ('ALLIANZ PARQUE', 'ALLIANZ PARQUE'),
        ('CASTELÃO (CE)', 'CASTELÃO (CE)'),
    )
    TIMES = (
        ('CAM', 'Atlético-MG'),
        ('COR', 'Corinthians'),
        ('SPT', 'Sport'),
        ('SPO', 'São Paulo'),
        ('AME', 'América-MG'),
        ('INT', 'Internacional'),
        ('CAP', 'Athletico-PR'),
        ('BOT', 'Botafogo'),
        ('FLU', 'Fluminense'),
        ('FLA', 'Flamengo'),
        ('SAN', 'Santos'),
        ('BAH', 'Bahia'),
        ('PAL', 'Palmeiras'),
        ('FOR', 'Fortaleza'),
    )
    Rodada = models.IntegerField()
    Jogo = models.IntegerField(max_length=2, choices=JOGOS)
    Horario = models.DateTimeField('data/hora')
    Local = models.CharField(max_length=30, choices=ESTADIOS)
    Time1 = models.CharField(max_length=30, choices=TIMES)
    Time2 = models.CharField(max_length=30, choices=TIMES)