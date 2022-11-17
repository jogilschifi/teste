from django.urls import path
from copadomundo.views import home, PalpiteList, salvar

urlpatterns = [
    path('', home),
    path('jogos/', PalpiteList.as_view(), name='palpitescopa'),
    path('save/<time1>/<time2>/', salvar),
]