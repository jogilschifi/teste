from django.contrib import admin
from .models import Palpites, Horarios, Resultados, Ordenacao, Pontuacao, PontuacaoTotal

# Register your models here.
admin.site.register(Palpites)

admin.site.register(Horarios)

admin.site.register(Resultados)

admin.site.register(Ordenacao)

admin.site.register(Pontuacao)

admin.site.register(PontuacaoTotal)