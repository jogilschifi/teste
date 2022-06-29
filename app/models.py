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
