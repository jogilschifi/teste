from django.contrib import admin
from .models import Clubes, PalpitesFormula1, PontuacaoF1, PontuacaoTotalF1, ResultadosBrasileirao, OrdenacaoBrasileirao, Brasileirao, PontuacaoBrasileirao, PontuacaoTotalBrasileirao, CopadoBrasil, ResultadosCopadoBrasil
# Register your models here.

admin.site.register(Clubes)

admin.site.register(ResultadosBrasileirao, required=False)

admin.site.register(OrdenacaoBrasileirao)

admin.site.register(Brasileirao)

admin.site.register(PontuacaoBrasileirao)

admin.site.register(PontuacaoTotalBrasileirao)

admin.site.register(CopadoBrasil)

admin.site.register(ResultadosCopadoBrasil)

admin.site.register(PalpitesFormula1)

admin.site.register(PontuacaoF1)

admin.site.register(PontuacaoTotalF1)