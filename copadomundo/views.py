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

from .models import Palpites, Horarios, Resultado, Ordenacao, Pontuacao, PontuacaoTotal, Jogos
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
    if page_num == 1:
        data['horalimite'] = datetime.datetime(2022, 11, 20, 13, 00)
    elif page_num == '1':
        data['horalimite'] = datetime.datetime(2022, 11, 20, 13, 00)
    elif page_num == '2':
        data['horalimite'] = datetime.datetime(2022, 11, 21, 10, 00)
    elif page_num == '3':
        data['horalimite'] = datetime.datetime(2022, 11, 21, 13, 00)
    elif page_num == '4':
        data['horalimite'] = datetime.datetime(2022, 11, 21, 16, 00)
    elif page_num == '5':
        data['horalimite'] = datetime.datetime(2022, 11, 22, 7, 00)
    elif page_num == '6':
        data['horalimite'] = datetime.datetime(2022, 11, 22, 10, 00)
    elif page_num == '7':
        data['horalimite'] = datetime.datetime(2022, 11, 22, 13, 00)
    elif page_num == '8':
        data['horalimite'] = datetime.datetime(2022, 11, 22, 16, 00)
    elif page_num == '9':
        data['horalimite'] = datetime.datetime(2022, 11, 23, 7, 00)
    elif page_num == '10':
        data['horalimite'] = datetime.datetime(2022, 11, 23, 10, 00)
    elif page_num == '11':
        data['horalimite'] = datetime.datetime(2022, 11, 23, 13, 00)
    elif page_num == '12':
        data['horalimite'] = datetime.datetime(2022, 11, 23, 16, 00)
    elif page_num == '13':
        data['horalimite'] = datetime.datetime(2022, 11, 24, 7, 00)
    elif page_num == '14':
        data['horalimite'] = datetime.datetime(2022, 11, 24, 10, 00)
    elif page_num == '15':
        data['horalimite'] = datetime.datetime(2022, 11, 24, 13, 00)
    else:
        data['horalimite'] = datetime.datetime(2022, 11, 24, 16, 00)
    data['hora'] = datetime.datetime.now()
    data['pages'] = p
    data['page'] = page
    data['object'] = page.object_list
    data['page_num'] = page_num
    meu_palpite = Palpites.objects.all()
    meu_palpite = meu_palpite.filter(user=request.user)
    data['meu_palpite'] = meu_palpite.filter(Jogo=page_num)
    pontuacao = Pontuacao.objects.all()
    pontuacao = pontuacao.filter(user=request.user)
    pontuacao = pontuacao.filter(Jogo=page_num)
    data['pontuacao'] = pontuacao.first()
    resultado = Resultado.objects.all()
    resultado = resultado.filter(Jogo=page_num)
    data['resultado'] = resultado.first()

    return render(request, 'copadomundo/home.html', data)

@login_required
def palpite(request, Rodada, Jogo):

    jogo = Jogos.objects.all()
    jogo = jogo.filter(Rodada=Rodada)
    data = {}
    data['jogo'] = jogo.filter(Jogo=Jogo)
    data['Rodada'] = Rodada
    data['Jogo'] = Jogo
    verificacao = Palpites.objects.all()
    verificacao = verificacao.filter(user=request.user)
    verificacao = verificacao.filter(Rodada=Rodada)
    verificacao = verificacao.filter(Jogo=Jogo)
    if verificacao:
        return redirect(reverse("homecopa", kwargs={'page':Jogo}))
    form = PalpitesForm()
    if request.method == 'POST':
        form = PalpitesForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(reverse("homecopa"))
    data['form'] = form
    return render(request, 'copadomundo/save.html', data)

@login_required
def update(request, pk):
    palpite = Palpites.objects.get(id=pk)
    usuario_palpite = palpite.user_id
    if not usuario_palpite == request.user.id:
        return redirect('homecopa')
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

@login_required
def caminhocalculadora(request):
    data = {}
    data['rodada'] = Resultado.objects.all()
    data['usuario'] = Palpites.objects.all()
    return render(request, 'copadomundo/caminhocalculadora.html', data)

@login_required
def calculadora(request):
    data = {}
    resul = Resultado.objects.all()
    resul = resul.filter(Rodada=str(request.GET['rodada']))
    pontuacao = Pontuacao.objects.all()
    pontuacao = pontuacao.filter(Rodada=str(request.GET['rodada']))

    palpi = Palpites.objects.all()
    palpi = palpi.filter(Rodada=str(request.GET['rodada']))

    lista_resultado = []
    for i in resul:
        lista_resultado.append(i.Jogo)
    data['lista_resultado'] = lista_resultado
    lista_pontuacao = []
    for i in pontuacao:
        lista_pontuacao.append(i.Jogo)
    data['lista_pontuacao'] = lista_pontuacao
    lista_palpites = []
    for i in lista_resultado:
        if i not in lista_pontuacao:
            lista_palpites.append(i)
    data['lista_palpites'] = lista_palpites

    resul = resul.first()
    palpites = []
    for i in palpi:
        if i.Jogo in lista_palpites:
            PONTOS = 0
            RE = 0
            RB = 0
            RP = 0
            ER = 0
            GV = 0
            GP = 0
            if resul.time1 - resul.time2 > 0:
                if i.time1 - i.time2 > 0:
                    if resul.time1 - resul.time2 == i.time1 - i.time2:
                        if resul.time1 == i.time1:
                            PONTOS = 18
                            RE = 1
                        else:
                            PONTOS = 12
                            RB = 1
                    else:
                        PONTOS = 9
                        RP = 1
                        if resul.time1 == i.time1:
                            GV = 1
                        elif resul.time2 == i.time2:
                            GP = 1
                else:
                    ER = 1
            elif resul.time1 - resul.time2 < 0:
                if i.time1 - i.time2 < 0:
                    if resul.time1 - resul.time2 == i.time1 - i.time2:
                        if resul.time1 == i.time1:
                            PONTOS = 18
                            RE = 1
                        else:
                            PONTOS = 12
                            RB = 1
                    else:
                        PONTOS = 9
                        RP = 1
                        if resul.time1 == i.time1:
                            GP = 1
                        elif resul.time2 == i.time2:
                            GV = 1
                else:
                    ER = 1
            elif resul.time1 - resul.time2 == i.time1 - i.time2:
                if resul.time1 == i.time1:
                    PONTOS = 18
                    RE = 1
                else:
                    PONTOS = 12
                    RB = 1
            else:
                ER = 1
            palpites.append({"user": i.user, "user_id": i.user_id, "Jogo":i.Jogo, "Rodada": i.Rodada, "PONTOS": PONTOS, "RE": RE, "RB": RB, "RP": RP, "ER": ER, "GV": GV, "GP": GP})
            pontuacao = Pontuacao(user_id=i.user_id, Rodada=request.GET['rodada'], Jogo=i.Jogo, RE=RE, RB=RB, RP=RP, GV=GV, GP=GP, ER=ER, PONTOS=PONTOS)
            pontuacao.save()
    data['palpite'] = palpites
    return render(request, 'copadomundo/calculadora.html', data)
#@login_required
#def classificacao(request):
#    pirirpororo
