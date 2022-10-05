from django.contrib import admin
from .models import Clubes, ResultadosBrasileirao, OrdenacaoBrasileirao, Brasileirao, PontuacaoBrasileirao, PontuacaoTotalBrasileirao
# Register your models here.

admin.site.register(Clubes)

admin.site.register(ResultadosBrasileirao, required=False)

admin.site.register(OrdenacaoBrasileirao)

admin.site.register(Brasileirao)

admin.site.register(PontuacaoBrasileirao)

admin.site.register(PontuacaoTotalBrasileirao)