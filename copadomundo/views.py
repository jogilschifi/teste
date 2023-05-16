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
        data['horalimite'] = datetime.datetime(2023, 11, 21, 16, 00)
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
    elif page_num == '16':
        data['horalimite'] = datetime.datetime(2022, 11, 24, 16, 00)
    else:
        data['horalimite'] = datetime.datetime(2022, 11, 28, 13, 00)
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
    data['usuario'] = request.user
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
def update(request, pk, page):
    palpite = Palpites.objects.get(id=pk)
    usuario_palpite = palpite.user_id
    if not usuario_palpite == request.user.id:
        return redirect('homecopa')
    jogo = Jogos.objects.all()
    jogo = jogo.filter(Rodada=palpite.Rodada)
    data = {}
    data['page_num']= page
    data['jogo'] = jogo.filter(Jogo=palpite.Jogo)
    data['Rodada'] = palpite.Rodada
    data['Jogo'] = str(palpite.Jogo)
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
    resultado = Resultado.objects.all()
    resultado = resultado.filter(Rodada=str(request.GET['rodada']))
    pontuacao = Pontuacao.objects.all()
    pontuacao = pontuacao.filter(Rodada=str(request.GET['rodada']))

    palpi = Palpites.objects.all()
    palpi = palpi.filter(Rodada=str(request.GET['rodada']))

    lista_resultado = []
    for i in resultado:
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
            resul = resultado.filter(Jogo=i.Jogo)
            resul = resul.first()
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
    data['pontuacao'] = Pontuacao.objects.all()
    return render(request, 'copadomundo/calculadora.html', data)

@login_required
def calculadoraclassificacao(request):
    pontuacao = Pontuacao.objects.all()
    lista_usuarios = []
    for i in pontuacao:
        if i.user_id not in lista_usuarios:
            lista_usuarios.append(i.user_id)
    ver_pontuacao_total = PontuacaoTotal.objects.all()
    #por_rodada
    #get(id=pk)
    classificacao = []
    for i in lista_usuarios:
        pontuacao_total_usuario = ver_pontuacao_total.filter(user=i)
        pontuacao_total_usuario = pontuacao_total_usuario.first()
        pontuacao_usuario = pontuacao.filter(user=i)
        PONTOS = pontuacao_usuario.aggregate(Sum('PONTOS'))
        PONTOS = PONTOS["PONTOS__sum"]
        Jogo = pontuacao_usuario.aggregate(Max('Jogo'))
        Jogo = Jogo["Jogo__max"]
        Rodada = pontuacao_usuario.aggregate(Max('Rodada'))
        Rodada = Rodada["Rodada__max"]
        RE = pontuacao_usuario.aggregate(Sum('RE'))
        RE = RE["RE__sum"]
        RB = pontuacao_usuario.aggregate(Sum('RB'))
        RB = RB["RB__sum"]
        RP = pontuacao_usuario.aggregate(Sum('RP'))
        RP = RP["RP__sum"]
        ER = pontuacao_usuario.aggregate(Sum('ER'))
        ER = ER["ER__sum"]
        GV = pontuacao_usuario.aggregate(Sum('GV'))
        GV = GV["GV__sum"]
        GP = pontuacao_usuario.aggregate(Sum('GP'))
        GP = GP["GP__sum"]
        pontuacao_usuario = pontuacao_usuario.first()
        classificacao.append(
            {"user":pontuacao_usuario.user, "user_id": i, "Jogo": Jogo, "Rodada":Rodada, "PONTOS": PONTOS, "RE": RE, "RB": RB,
             "RP": RP, "ER": ER, "GV": GV, "GP": GP})
        pontuacao_total = PontuacaoTotal(user_id=i, Rodada=Rodada, Jogo=Jogo, RE=RE, RB=RB, RP=RP, GV=GV, GP=GP, ER=ER, PONTOS=PONTOS)
        if not pontuacao_total_usuario:
            pontuacao_total.save()
        elif pontuacao_total_usuario.PONTOS != PONTOS or pontuacao_total_usuario.ER != ER:
            pontu = ver_pontuacao_total.filter(id=pontuacao_total_usuario.id)
            pontu.update(user_id=i, Rodada=Rodada, Jogo=Jogo, RE=RE, RB=RB, RP=RP, GV=GV, GP=GP, ER=ER, PONTOS=PONTOS)
    data = {}
    data['pontuacao'] = PontuacaoTotal.objects.all()
    data['lista_usuarios'] = lista_usuarios
    data['classificacao'] = classificacao
    return render(request, 'copadomundo/calculadora.html', data)

@login_required
def classificacao(request):
    classificacao = PontuacaoTotal.objects.all()
    def classif_sort(clas):
        GVGP = clas.GV + clas.GP
        return clas.PONTOS, clas.RE, clas.RB, clas.id, GVGP, clas.GV, -clas.id
    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)

    cla = []
    count = 1
    for i in classificacao_sort:
        cla.append({"PONTOS": i.PONTOS, "RE": i.RE, "RB": i.RB, "RP": i.RP,
                    "user": i.user, "id": i.user_id, "posicao": count})
        count += 1
    data = {}
    data['cla'] = cla
    return render(request, 'copadomundo/classificacao.html', data)

def perfilcopa(request, user, pk):
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
        data['horalimite'] = datetime.datetime(2023, 11, 21, 13, 00)
    elif page_num == '4':
        data['horalimite'] = datetime.datetime(2023, 11, 21, 16, 00)
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
    meu_palpite = meu_palpite.filter(user=pk)
    data['meu_palpite'] = meu_palpite.filter(Jogo=page_num)
    pontuacao = Pontuacao.objects.all()
    pontuacao = pontuacao.filter(user=pk)
    pontuacao = pontuacao.filter(Jogo=page_num)
    data['pontuacao'] = pontuacao.first()
    resultado = Resultado.objects.all()
    resultado = resultado.filter(Jogo=page_num)
    data['resultado'] = resultado.first()
    data['usuario'] = user
    return render(request, 'copadomundo/home.html', data)