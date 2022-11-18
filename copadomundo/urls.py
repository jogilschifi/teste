from django.urls import path
from copadomundo.views import home, PalpiteList, palpite, save

urlpatterns = [
    path('', home),
    path('jogos/', PalpiteList.as_view(), name='palpitescopa'),
    path('palpite/<Rodada>/<Jogo>/', palpite, name='palpite'),
    path('save/', save),
]