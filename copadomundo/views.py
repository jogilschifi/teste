from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Max

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Palpites, Horarios, Resultados, Ordenacao, Pontuacao, PontuacaoTotal, Jogos
from django.contrib.auth.models import Group, User, GroupManager
from .forms import PalpitesForm

import datetime
# Create your views here.

@login_required
def home(request):
    jogos = Jogos.objects.all()
    p = Paginator(jogos, 1)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)

    data = {}
    data['pages'] = p
    data['page'] = page
    data['page_num'] = page_num
    meu_palpite = Palpites.objects.all()
    #meu_palpite = meu_palpite.filter(Rodada= verificacao.Rodada)
    #meu_palpite = meu_palpite.filter(user=request.user)
    data['meu_palpite'] = meu_palpite.filter(Jogo=page_num)
    return render(request, 'copadomundo/home.html', data)

@login_required
def palpite(request, Rodada, Jogo):
    jogo = Jogos.objects.all()
    jogo = jogo.filter(Rodada=Rodada)
    data = {}
    data['jogo'] = jogo.filter(Jogo=Jogo)
    data['Rodada'] = Rodada
    data['Jogo'] = Jogo
    form = PalpitesForm()
    if request.method == 'POST':
        form = PalpitesForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('homecopa')
    data['form'] = form
    return render(request, 'copadomundo/save.html', data)

@login_required
def save(request):
    form = PalpitesForm()
    if request.method == 'POST':
        form = PalpitesForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('homecopa')
    context = {'form': form}
    #if not request.GET['home']:
    #    return redirect(reverse("palpite", kwargs={'Rodada':request.GET['Rodada'], 'Jogo':request.GET['Jogo']}))
    #if not request.GET['away']:
    #    return redirect(reverse("palpite", kwargs={'Rodada':request.GET['Rodada'], 'Jogo':request.GET['Jogo']}))
    #verificacao = Palpites.objects.all()
    #verificacao = verificacao.filter(Rodada=int(request.GET['Rodada']))
    #verificacao = verificacao.filter(user=request.user)
    #verificacao = verificacao.filter(Jogo=int(request.GET['Jogo']))
    #data = {}
    #if verificacao:
    #    data['mensagem'] = 'Voce já palpitou'
    #else:
    #    data['mensagem'] = 'Palpite Salvo'
    #    palpite = Palpites(Rodada=int(request.GET['Rodada']), user=request.user, Jogo=int(request.GET['Jogo']), time1= int(request.GET['home']), time2= int(request.GET['away']))
    #    palpite.save()

    #data['home'] = request.GET['home']
    #data['away'] = request.GET['away']
    #data['Rodada'] = request.GET['Rodada']
    #data['Jogo'] = request.GET['Jogo']
    return render(request, 'copadomundo/save.html', context)

@login_required
def update(request, pk):
    palpite = Palpites.objects.get(id=pk)
    jogo = Jogos.objects.all()
    jogo = jogo.filter(Rodada=palpite.Rodada)
    data = {}
    data['jogo'] = jogo.filter(Jogo=palpite.Jogo)
    data['Rodada'] = palpite.Rodada
    data['Jogo'] = palpite.Jogo
    palpite = Palpites.objects.get(id=pk)
    form = PalpitesForm(instance=palpite)
    if request.method == 'POST':
        form = PalpitesForm(request.POST, instance=palpite)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('homecopa')
    data['form'] = form
    return render(request, 'copadomundo/save.html', data)
