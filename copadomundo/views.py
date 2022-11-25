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
    #meu_palpite = meu_palpite.filter(Rodada= verificacao.Rodada)
    meu_palpite = meu_palpite.filter(user=request.user)
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

#@login_required
#def save(request):
    #form = PalpitesForm()
    #if request.method == 'POST':
    #    form = PalpitesForm(request.POST)
    #    if form.is_valid():
    #        form.instance.user = request.user
    #        form.save()
    #        return redirect('homecopa')
    #context = {'form': form}
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
    #return render(request, 'copadomundo/save.html', context)

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
    data['classificacao'] = Pontuacao.objects.all()
    data['rodada']= request.GET['rodada']
    data['jogo'] = request.GET['jogo']
    resul = Resultado.objects.all()
    resul = resul.filter(Rodada=str(request.GET['rodada']))
    resul = resul.filter(Rodada=str(request.GET['jogo']))
    data['resultadoobj'] = resul
    resul = resul.first()

    palpi = Palpites.objects.all()
    palpi = palpi.filter(Rodada=str(request.GET['rodada']))
    palpi = palpi.filter(Jogo=str(request.GET['jogo']))
    palpites = []
    for i in palpi:
        PONTOS = 0
        RE = 0
        RB = 0
        RP = 0
        ER = 0
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
        palpites.append({"user": i.user, "user_id": i.user_id, "PONTOS": PONTOS, "RE": RE, "RB": RB, "RP": RP, "ER": ER})
        pontuacao = Pontuacao(user_id=i.user_id, Rodada=request.GET['rodada'], RE=RE, RB=RB, RP=RP, ER=ER, PONTOS=PONTOS)
    data['palpite'] = palpites
    count = 0
    for i in range(len(palpi)):
        if resul.time1 - resul.time2 > 0:
            data['derrota'] += 1
        else:
            count += 1
    data['vitoria'] = count
    return render(request, 'copadomundo/calculadora.html', data)

    #usuarios = Pontuacao.objects.all()
    #usuarios_novos = Palpites.objects.all()
    #rodadaant = str(int(request.GET['rodada']) - 1)
    #rodadaatual = str(request.GET['rodada'])
    #usuarios_ant = usuarios.filter(Rodada=rodadaant)
    #usuarios_atual = usuarios_novos.filter(Rodada=rodadaatual)
    #usuarios_atual = usuarios_atual.aggregate(Max('user_id'))
    #usuarios_atual = usuarios_atual["user_id__max"]
    #usuarios_atual = usuarios_atual + 1
    #usuariomax = usuarios_ant.aggregate(Max('user_id'))
    #usuariomax = usuariomax["user_id__max"]
    #usuariomax = usuariomax + 1
    #if usuarios_atual > usuariomax:
        #usuariomax = usuarios_atual
    #data['usuariomax'] = usuariomax
    #data['salvo'] = 0
    #data['salvo1'] = 0
    #data['salvo2'] = 0
    #data['salvo3'] = 0
    #data['salvo4'] = 0
    #data['salvo5'] = 0
    #for j in range(usuariomax):
        #palpite = palpi.filter(user=j)
        #if palpite:
            #data['salvo1'] += 1
            #data['palpiteobj'] = palpite
            #palpite = palpite.first()
            #ttime1 = palpite.AthleticoPR
            #ttime2 = palpite.Palmeiras
            #user = palpite.user
            #palpite = {"AthleticoPR": ttime1, "Palmeiras": ttime2, "Corinthians": ttime3, "Internacional": ttime4,
               #        "AtleticoMG": ttime5, "Fluminense": ttime6, "Santos": ttime7, "SaoPaulo": ttime8,
              #         "Flamengo": ttime9, "Botafogo": ttime10, "Avai": ttime11, "Bragantino": ttime12,
             #          "AtleticoGO": ttime13, "Goias": ttime14, "Ceara": ttime15, "Coritiba": ttime16,
            #           "AmericaMG": ttime17, "Cuiaba": ttime18, "Juventude": ttime19, "Fortaleza": ttime20, "user": user}
            #data['palpite'] = palpite
            #ordem = OrdenacaoBrasileirao.objects.all()
            #ordem = ordem.filter(Rodada=str(request.GET['rodada']))
            #data['ordemobj'] = ordem
            #if ordem:
            #    times = ordem.first()
            #    time1 = times.AthleticoPR
            #    time2 = times.Palmeiras

            #    ordem = [time1, time2, time3, time4, time5, time6, time7, time8, time9, time10, time11, time12, time13,
            #             time14, time15, time16, time17, time18, time19, time20]
            #    data['ordem'] = ordem
            #else:
            #    return redirect('/caminhocalculadora/')
            #tttime1 = resul.AthleticoPR
            #tttime2 = resul.Palmeiras

            #resultado = {"AthleticoPR": tttime1, "Palmeiras": tttime2, "Corinthians": tttime3, "Internacional": tttime4,
              #           "AtleticoMG": tttime5, "Fluminense": tttime6, "Santos": tttime7, "SaoPaulo": tttime8,
             #            "Flamengo": tttime9, "Botafogo": tttime10, "Avai": tttime11, "Bragantino": tttime12,
            #             "AtleticoGO": tttime13, "Goias": tttime14, "Ceara": tttime15, "Coritiba": tttime16,
            #             "AmericaMG": tttime17, "Cuiaba": tttime18, "Juventude": tttime19, "Fortaleza": tttime20}
            #data['resultado'] = resultado
            #i = 0
            #igual = 0
            #exato = 0
            #bonus = 0
            #diferente = 0
            #total = 0
            #while i < 19:
                #if i % 2 == 0:
                    #if resultado[ordem[i]] != None:
                        #if resultado[ordem[i + 1]] != None:
                            #if palpite[ordem[i]] != None:
                                #if palpite[ordem[i + 1]] != None:
                                    #if resultado[ordem[i]] - resultado[ordem[i + 1]] > 0:
                                        #if palpite[ordem[i]] - palpite[ordem[i + 1]] > 0:
                                            #if resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[ordem[i + 1]]:
                                                #if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                                                #    exato += 1
                                                #    data['exato'] = exato
                                                #    total += 18
                                                #    data['total'] = total
                                                #else:
                                                #    bonus += 1
                                               #     data['bonus'] = bonus
                                              #      total += 12
                                             #       data['total'] = total
                                            #else:
                                           #     igual += 1
                                          #      data['igual'] = igual
                                         #       total += 9
                                        #        data['total'] = total
                                       # else:
                                      #      diferente += 1
                                     #       data['diferente'] = diferente
                                    #elif resultado[ordem[i]] - resultado[ordem[i + 1]] < 0:
                                        #if palpite[ordem[i]] - palpite[ordem[i + 1]] < 0:
                                            #if resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[ordem[i + 1]]:
                                                #if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                                                #    exato += 1
                                               #     data['exato'] = exato
                                              #      total += 18
                                             #       data['total'] = total
                                            #    else:
                                           #         bonus += 1
                                          #          data['bonus'] = bonus
                                         #           total += 12
                                        #            data['total'] = total
                                       #     else:
                                      #          igual += 1
                                     #           data['igual'] = igual
                                    #            total += 9
                                   #             data['total'] = total
                                  #      else:
                                 #           diferente += 1
                                #            data['diferente'] = diferente
                               #     elif resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[
                              #          ordem[i + 1]]:
                             #           if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                            #                exato += 1
                           #                 data['exato'] = exato
                          #                  total += 18
                         #                   data['total'] = total
                        #                else:
                       #                     igual += 1
                      #                      data['igual'] = igual
                     #                       total += 9
                    #                        data['total'] = total
                   #                 else:
                  #                      diferente += 1
                 #                       data['diferente'] = diferente
                #i += 1

            #userid = palpite["user"]
            #rodada = request.GET['rodada']
            #pontuacao = PontuacaoBrasileirao(user_id=j, Rodada=rodada, RE=exato, RB=bonus, RP=igual, ER=diferente, PONTOS=total)
            #Verificacao
            #verificacao = PontuacaoBrasileirao.objects.all()
            #verificacao = verificacao.filter(Rodada=request.GET['rodada'])
            #verificacao = verificacao.filter(user_id=j)
            #verificacao = verificacao.first()
            #if verificacao:
                #pontos = verificacao.PONTOS
                #erro = verificacao.ER
                #if pontos == total:
               #     if erro == diferente:
              #          data['salvo2'] += 1
             #   else:
            #        verificacao.delete()
           #         pontuacao.save()
          #  else:
         #       pontuacao.save()
        #else:
            #data['salvo'] += 1
            #user = usuarios.filter(user=j)
            #if user:
                #data['salvo3'] += 1
                #verificacao = PontuacaoBrasileirao.objects.all()
                #verificacao = verificacao.filter(Rodada=request.GET['rodada'])
                #verificacao = verificacao.filter(user_id=j)
               # verificacao = verificacao.first()
              #  if verificacao:
             #       pontos = verificacao.PONTOS
            #        erro = verificacao.ER
           #         if pontos == 0:
          #              if erro == 0:
         #                   data['salvo4'] += 1
        #        else:
       #             pontuacao = PontuacaoBrasileirao(user_id=j, Rodada=int(request.GET['rodada']), RE=0, RB=0, RP=0, ER=0, PONTOS=0)
      #              pontuacao.save()
     #               data['salvo5'] += 1

    #return render(request, 'app/tabelapontuacao.html', data)

#@login_required
#def classificacao(request):
#    pirirpororo
