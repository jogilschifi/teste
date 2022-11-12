from django.urls import path
from copadomundo.views import home, PalpiteList

urlpatterns = [
    path('', home),
    path('jogos/', PalpiteList.as_view(), name='palpitescopa'),
]