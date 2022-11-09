from django.urls import path
from copadomundo.views import home

urlpatterns = [
    path('', home),
]