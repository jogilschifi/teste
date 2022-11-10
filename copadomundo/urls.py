from django.urls import path
from copadomundo.views import home, PalpiteList

urlpatterns = [
    path('', home),
    path('pedro/', PalpiteList.as_view(), name='palpites'),
]