from django.shortcuts import render
from django.template import Template
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

@login_required
def home(request):
    data = {}
    data['horalimite'] = datetime.datetime(2022, 11, 20, 13, 00)

    return render(request, 'copadobrasil/home.html', data)