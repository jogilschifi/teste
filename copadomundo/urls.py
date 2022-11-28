from django.urls import path
from copadomundo.views import home, palpite, update, caminhocalculadora, calculadora, calculadoraclassificacao, classificacao

urlpatterns = [
    path('', home, name='homecopa'),
    #path('jogos/', PalpiteList.as_view(), name='palpitescopa'),
    path('palpite/<Rodada>/<Jogo>/', palpite, name='palpite'),
    #path('save/', save),
    path('update/<int:pk>/', update, name='update'),
#    path('classificacao/', classificacao),
    path('caminhocalculadora/', caminhocalculadora),
    path('calculadora/', calculadora),
    path('calculadoraclassificacao/', calculadoraclassificacao),
    path('classificacao/', classificacao),
#    path('calculadora/', calculadora),
    #path('update/<int:pk>/', PalpiteUpdate.as_view(), name='palpiteupdate'),
]