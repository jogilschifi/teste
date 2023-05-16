from django.urls import path
from copadobrasil.views import home

urlpatterns = [
    path('', home),
    #path('jogos/', PalpiteList.as_view(), name='palpitescopa'),
    #path('palpite/<Rodada>/<Jogo>/', palpite, name='palpite'),
    #path('save/', save),
    #path('update/<int:page>/<int:pk>/', update, name='update'),
    #path('classificacao/', classificacao),
    #path('caminhocalculadora/', caminhocalculadora),
    #path('calculadora/', calculadora),
    #path('calculadoraclassificacao/', calculadoraclassificacao),
    #path('classificacao/', classificacao),
    #path('<int:pk>/<user>/', perfilcopa),
    #path('calculadora/', calculadora),
    #path('update/<int:pk>/', PalpiteUpdate.as_view(), name='palpiteupdate'),
]