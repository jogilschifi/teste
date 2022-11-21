from django.contrib import admin
from .models import Palpites, Horarios, Resultado, Ordenacao, Pontuacao, PontuacaoTotal, Ligas, Jogos

# Register your models here.
admin.site.register(Palpites)

admin.site.register(Horarios)

admin.site.register(Resultado)

admin.site.register(Ordenacao)

admin.site.register(Pontuacao)

admin.site.register(PontuacaoTotal)

admin.site.register(Ligas)

admin.site.register(Jogos)