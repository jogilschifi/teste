from urllib import request
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Max

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

import datetime

from app.models import Clubes, Brasileirao, ResultadosBrasileirao, OrdenacaoBrasileirao, PontuacaoBrasileirao, PontuacaoTotalBrasileirao


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('palpites')


class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('palpites')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('palpites')
        return super(RegisterPage, self).get(*args, **kwargs)

def perfilusuarios(request, pk, user):

    horario = datetime.datetime.now()
    horalimite = datetime.datetime(2022, 10, 8, 19, 00)
    if horalimite > horario:
        rod = 30
    else:
        rod = 31
    data = {}
    data['rod'] = rod
    data['palpites'] = Brasileirao.objects.all()
    data['palpites'] = data['palpites'].filter(user_id=pk)
    data['palpites'] = data['palpites'].filter(Rodada=rod)
    data['palpites'] = data['palpites'].first()
    data['rodada'] = ResultadosBrasileirao.objects.all()
    data['pk'] = pk
    data['user'] = user
    if data['palpites']:
        return render(request, 'app/perfilusuarios.html', data)
    else:
        data['palpites'] = 0
    return render(request, 'app/perfilusuarios.html', data)


class PalpiteList(LoginRequiredMixin, ListView):
    model = Brasileirao
    context_object_name = 'palpites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['palpites'] = context['palpites'].filter(user=self.request.user)
        context['palpites'] = context['palpites'].filter(Rodada=31)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 10, 8, 19, 00)
        return context

    def filter(self, user):
        pass

    @classmethod
    def user_id(cls):
        pass


class PalpiteDetail(LoginRequiredMixin, DetailView):
    model = Brasileirao
    context_object_name = 'palpites'


class PalpiteCreate(LoginRequiredMixin, CreateView):
    model = Brasileirao
    fields = '__all__'
    context_object_name = 'palpites'
    success_url = reverse_lazy('palpites')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dados'] = Brasileirao.objects.all()
        context['dados'] = context['dados'].filter(user=self.request.user)
        context['dados'] = context['dados'].filter(Rodada=31)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 10, 8, 19, 00)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteCreate, self).form_valid(form)


class PalpiteUpdate(LoginRequiredMixin, UpdateView):
    model = Brasileirao
    fields = '__all__'
    success_url = reverse_lazy('palpites')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteUpdate, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 10, 8, 19, 00)
        return context

class PalpiteDelete(DeleteView):
    model = Brasileirao
    success_url = reverse_lazy('palpites')


def pontuacao(request):
    return render(request, 'app/pontuacao.html')

def rodada(request):
    data = {}
    data['rodada'] = ResultadosBrasileirao.objects.all()
    return render(request, 'app/rodada.html', data)

def classificacao(request):
    classificacao = PontuacaoTotalBrasileirao.objects.all()
    if classificacao:
        rodada = classificacao.aggregate(Max('Rodada'))
        rodada = rodada["Rodada__max"]
        rodadas = ResultadosBrasileirao.objects.all()
        classificacao = classificacao.filter(Rodada=rodada)
        def classif_sort(clas):
            return clas.PONTOS, clas.RE, clas.RB, clas.id
        classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)
        data = {}
        data['rodadas'] = rodadas
        data['rodada'] = rodada
        usuarios = len(classificacao)

        cla = []
        for i in range(usuarios):
            classifnova = classificacao_sort[i]
            cla.append({"PONTOS":classifnova.PONTOS, "RE":classifnova.RE, "RB":classifnova.RB, "RP":classifnova.RP, "user":classifnova.user, "id":classifnova.user_id, "posicao":i+1})
        data['cla'] = cla
        return render(request, 'app/classificacao.html', data)
    data = {}
    data['cla'] = Brasileirao.objects.all()


    return render(request, 'app/classificacao.html', data)

def classificacaoporrodada(request):

    classificacao = PontuacaoTotalBrasileirao.objects.all()
    rodada = request.GET['rodada']
    if rodada == '0':
        return redirect('/classificacao/')
    rodadas = ResultadosBrasileirao.objects.all()
    classificacao = classificacao.filter(Rodada=rodada)

    def classif_sort(clas):
        return clas.PONTOS, clas.RE, clas.RB, clas.id

    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)
    data = {}
    data['rodadas'] = rodadas
    data['rodada'] = rodada
    usuarios = len(classificacao)

    cla = []
    for i in range(usuarios):
        classifnova = classificacao_sort[i]
        cla.append({"PONTOS": classifnova.PONTOS, "RE": classifnova.RE, "RB": classifnova.RB, "RP": classifnova.RP, "user": classifnova.user, "id":classifnova.user_id, "posicao": i + 1})
    data['cla'] = cla

    return render(request, 'app/classificacaoporrodada.html', data)

def classificacaodoispontozero(request):
    pont = PontuacaoBrasileirao.objects.all()
    usuariomax = pont.aggregate(Max('user_id'))
    usuariomax = usuariomax["user_id__max"]
    usuariomax = usuariomax + 1
    for i in range(usuariomax):
        pontuser = pont.filter(user=i)
        if pontuser:
            total = pontuser.aggregate(Sum('PONTOS'))
            total = total["PONTOS__sum"]
            rodada = pontuser.aggregate(Max('Rodada'))
            rodada = rodada["Rodada__max"]
            exato = pontuser.aggregate(Sum('RE'))
            exato = exato["RE__sum"]
            bonus = pontuser.aggregate(Sum('RB'))
            bonus = bonus["RB__sum"]
            igual = pontuser.aggregate(Sum('RP'))
            igual = igual["RP__sum"]
            diferente = pontuser.aggregate(Sum('ER'))
            diferente = diferente["ER__sum"]
            pontuacaototal = PontuacaoTotalBrasileirao(user_id=i, Rodada=rodada, RE=exato, RB=bonus, RP=igual, ER=diferente, PONTOS=total)
            ponttotalantigo = PontuacaoTotalBrasileirao.objects.all()
            ponttotalantigo = ponttotalantigo.filter(user=i)
            if ponttotalantigo:
                rodadaantiga = ponttotalantigo.aggregate(Max('Rodada'))
                rodadaantiga = rodadaantiga["Rodada__max"]
                ponttotalantigo = ponttotalantigo.filter(Rodada=rodadaantiga)
                ponttotalantigo = ponttotalantigo.first()
                totalantigo = ponttotalantigo.PONTOS
                erroantigo = ponttotalantigo.ER
                if diferente != erroantigo:
                    if total != totalantigo:
                        if rodada != rodadaantiga:
                            pontuacaototal.save()
                        else:
                            ponttotalantigo.delete()
                            pontuacaototal.save()
            else:
                if pontuacaototal:
                    pontuacaototal.save()

    data = {}
    data['classificacao'] = PontuacaoTotalBrasileirao.objects.all()
    data['rodada'] = ResultadosBrasileirao.objects.all()

    return render(request, 'app/classificacaodoispontozero.html', data)


def resultado(request):
    data = {}
    verificacao = int(request.GET['verificacao'])
    data['verificacao'] = verificacao
    current_user = request.GET['user_id']
    data['requestuser'] = request.user
    data['user_id'] = current_user
    user = request.GET['user']
    data['user'] = user
    data['rodada'] = int(request.GET['rodada'])
    resultado = ResultadosBrasileirao.objects.all()
    resultado = resultado.filter(Rodada=request.GET['rodada'])
    resultado = resultado.first()
    data['resultadoobj'] = resultado

    palpite = Brasileirao.objects.all()
    palpite = palpite.filter(Rodada=request.GET['rodada'])
    palpite = palpite.filter(user=current_user)
    palpite = palpite.first()
    data['palpiteobj'] = palpite

    ordem = OrdenacaoBrasileirao.objects.all()
    ordem = ordem.filter(Rodada=request.GET['rodada'])
    data['ordemobj'] = ordem
    if ordem:
        times = ordem.first()
        time1 = times.AthleticoPR
        time2 = times.Palmeiras
        time3 = times.Corinthians
        time4 = times.Internacional
        time5 = times.AtleticoMG
        time6 = times.Fluminense
        time7 = times.Santos
        time8 = times.SaoPaulo
        time9 = times.Flamengo
        time10 = times.Botafogo
        time11 = times.Avai
        time12 = times.Bragantino
        time13 = times.AtleticoGO
        time14 = times.Goias
        time15 = times.Ceara
        time16 = times.Coritiba
        time17 = times.AmericaMG
        time18 = times.Cuiaba
        time19 = times.Juventude
        time20 = times.Fortaleza
        ordem = [time1, time2, time3, time4, time5, time6, time7, time8, time9, time10, time11, time12, time13, time14, time15, time16, time17, time18, time19, time20]
        data['ordem'] = ordem
    else:
        if data['verificacao'] == 1:
            return redirect(reverse("perfilusuarios",kwargs={'pk':int(current_user), 'user':str(user)}))
        return redirect('/rodada/')
    if palpite:
        ttime1 = palpite.AthleticoPR
        ttime2 = palpite.Palmeiras
        ttime3 = palpite.Corinthians
        ttime4 = palpite.Internacional
        ttime5 = palpite.AtleticoMG
        ttime6 = palpite.Fluminense
        ttime7 = palpite.Santos
        ttime8 = palpite.SaoPaulo
        ttime9 = palpite.Flamengo
        ttime10 = palpite.Botafogo
        ttime11 = palpite.Avai
        ttime12 = palpite.Bragantino
        ttime13 = palpite.AtleticoGO
        ttime14 = palpite.Goias
        ttime15 = palpite.Ceara
        ttime16 = palpite.Coritiba
        ttime17 = palpite.AmericaMG
        ttime18 = palpite.Cuiaba
        ttime19 = palpite.Juventude
        ttime20 = palpite.Fortaleza
        palpite = {"AthleticoPR": ttime1, "Palmeiras": ttime2, "Corinthians": ttime3 , "Internacional": ttime4, "AtleticoMG": ttime5, "Fluminense": ttime6, "Santos": ttime7, "SaoPaulo": ttime8, "Flamengo": ttime9, "Botafogo": ttime10, "Avai": ttime11, "Bragantino": ttime12, "AtleticoGO": ttime13, "Goias": ttime14, "Ceara": ttime15, "Coritiba": ttime16, "AmericaMG": ttime17, "Cuiaba": ttime18, "Juventude": ttime19, "Fortaleza": ttime20}
        data['palpite'] = palpite
    else:
        if data['verificacao'] == 1:
            return redirect(reverse("perfilusuarios",kwargs={'pk':int(current_user), 'user':str(user)}))
        return redirect('/rodada/')
    tttime1 = resultado.AthleticoPR
    tttime2 = resultado.Palmeiras
    tttime3 = resultado.Corinthians
    tttime4 = resultado.Internacional
    tttime5 = resultado.AtleticoMG
    tttime6 = resultado.Fluminense
    tttime7 = resultado.Santos
    tttime8 = resultado.SaoPaulo
    tttime9 = resultado.Flamengo
    tttime10 = resultado.Botafogo
    tttime11 = resultado.Avai
    tttime12 = resultado.Bragantino
    tttime13 = resultado.AtleticoGO
    tttime14 = resultado.Goias
    tttime15 = resultado.Ceara
    tttime16 = resultado.Coritiba
    tttime17 = resultado.AmericaMG
    tttime18 = resultado.Cuiaba
    tttime19 = resultado.Juventude
    tttime20 = resultado.Fortaleza
    resultado = {"AthleticoPR": tttime1, "Palmeiras": tttime2, "Corinthians": tttime3, "Internacional": tttime4, "AtleticoMG": tttime5, "Fluminense": tttime6, "Santos": tttime7, "SaoPaulo": tttime8, "Flamengo": tttime9, "Botafogo": tttime10, "Avai": tttime11, "Bragantino": tttime12, "AtleticoGO": tttime13, "Goias": tttime14, "Ceara": tttime15, "Coritiba": tttime16, "AmericaMG": tttime17, "Cuiaba": tttime18, "Juventude": tttime19, "Fortaleza": tttime20}
    data['resultado'] = resultado

    i = 0
    igual = 0
    data['igual'] = igual
    exato = 0
    data['exato'] = exato
    bonus = 0
    data['bonus'] = bonus
    diferente = 0
    data['diferente'] = diferente
    total = 0
    data['total'] = total
    while i < 19:
        if i % 2 == 0:
            if resultado[ordem[i]] != None:
                if resultado[ordem[i+1]] != None:
                    if resultado[ordem[i]] - resultado[ordem[i+1]] > 0:
                        if palpite[ordem[i]] - palpite[ordem[i+1]] > 0:
                            if resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[ordem[i + 1]]:
                                if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                                    exato += 1
                                    data['exato'] = exato
                                    total += 18
                                    data['total'] = total
                                    if i == 0:
                                        data['cor1'] = 'blue'
                                    elif i == 2:
                                        data['cor2'] = 'blue'
                                    elif i == 4:
                                        data['cor3'] = 'blue'
                                    elif i == 6:
                                        data['cor4'] = 'blue'
                                    elif i == 8:
                                        data['cor5'] = 'blue'
                                    elif i == 10:
                                        data['cor6'] = 'blue'
                                    elif i == 12:
                                        data['cor7'] = 'blue'
                                    elif i == 14:
                                        data['cor8'] = 'blue'
                                    elif i == 16:
                                        data['cor9'] = 'blue'
                                    elif i == 18:
                                        data['cor10'] = 'blue'
                                else:
                                    bonus += 1
                                    data['bonus'] = bonus
                                    total += 12
                                    data['total'] = total
                                    if i == 0:
                                        data['cor1'] = '#993399'
                                    elif i == 2:
                                        data['cor2'] = '#993399'
                                    elif i == 4:
                                        data['cor3'] = '#993399'
                                    elif i == 6:
                                        data['cor4'] = '#993399'
                                    elif i == 8:
                                        data['cor5'] = '#993399'
                                    elif i == 10:
                                        data['cor6'] = '#993399'
                                    elif i == 12:
                                        data['cor7'] = '#993399'
                                    elif i == 14:
                                        data['cor8'] = '#993399'
                                    elif i == 16:
                                        data['cor9'] = '#993399'
                                    elif i == 18:
                                        data['cor10'] = '#993399'
                            else:
                                igual += 1
                                data['igual'] = igual
                                total += 9
                                data['total'] = total
                                if i == 0:
                                    data['cor1'] = 'orange'
                                elif i == 2:
                                    data['cor2'] = 'orange'
                                elif i == 4:
                                    data['cor3'] = 'orange'
                                elif i == 6:
                                    data['cor4'] = 'orange'
                                elif i == 8:
                                    data['cor5'] = 'orange'
                                elif i == 10:
                                    data['cor6'] = 'orange'
                                elif i == 12:
                                    data['cor7'] = 'orange'
                                elif i == 14:
                                    data['cor8'] = 'orange'
                                elif i == 16:
                                    data['cor9'] = 'orange'
                                elif i == 18:
                                    data['cor10'] = 'orange'

                        else:
                            diferente += 1
                            data['diferente'] = diferente
                            if i == 0:
                                data['cor1'] = 'red'
                            elif i == 2:
                                data['cor2'] = 'red'
                            elif i == 4:
                                data['cor3'] = 'red'
                            elif i == 6:
                                data['cor4'] = 'red'
                            elif i == 8:
                                data['cor5'] = 'red'
                            elif i == 10:
                                data['cor6'] = 'red'
                            elif i == 12:
                                data['cor7'] = 'red'
                            elif i == 14:
                                data['cor8'] = 'red'
                            elif i == 16:
                                data['cor9'] = 'red'
                            elif i == 18:
                                data['cor10'] = 'red'
                    elif resultado[ordem[i]] - resultado[ordem[i+1]] < 0:
                        if palpite[ordem[i]] - palpite[ordem[i+1]] < 0:
                            if resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[ordem[i + 1]]:
                                if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                                    exato += 1
                                    data['exato'] = exato
                                    total += 18
                                    data['total'] = total
                                    if i == 0:
                                        data['cor1'] = 'blue'
                                    elif i == 2:
                                        data['cor2'] = 'blue'
                                    elif i == 4:
                                        data['cor3'] = 'blue'
                                    elif i == 6:
                                        data['cor4'] = 'blue'
                                    elif i == 8:
                                        data['cor5'] = 'blue'
                                    elif i == 10:
                                        data['cor6'] = 'blue'
                                    elif i == 12:
                                        data['cor7'] = 'blue'
                                    elif i == 14:
                                        data['cor8'] = 'blue'
                                    elif i == 16:
                                        data['cor9'] = 'blue'
                                    elif i == 18:
                                        data['cor10'] = 'blue'
                                else:
                                    bonus += 1
                                    data['bonus'] = bonus
                                    total += 12
                                    data['total'] = total
                                    if i == 0:
                                        data['cor1'] = '#993399'
                                    elif i == 2:
                                        data['cor2'] = '#993399'
                                    elif i == 4:
                                        data['cor3'] = '#993399'
                                    elif i == 6:
                                        data['cor4'] = '#993399'
                                    elif i == 8:
                                        data['cor5'] = '#993399'
                                    elif i == 10:
                                        data['cor6'] = '#993399'
                                    elif i == 12:
                                        data['cor7'] = '#993399'
                                    elif i == 14:
                                        data['cor8'] = '#993399'
                                    elif i == 16:
                                        data['cor9'] = '#993399'
                                    elif i == 18:
                                        data['cor10'] = '#993399'
                            else:
                                igual += 1
                                data['igual'] = igual
                                total += 9
                                data['total'] = total
                                if i == 0:
                                    data['cor1'] = 'orange'
                                elif i == 2:
                                    data['cor2'] = 'orange'
                                elif i == 4:
                                    data['cor3'] = 'orange'
                                elif i == 6:
                                    data['cor4'] = 'orange'
                                elif i == 8:
                                    data['cor5'] = 'orange'
                                elif i == 10:
                                    data['cor6'] = 'orange'
                                elif i == 12:
                                    data['cor7'] = 'orange'
                                elif i == 14:
                                    data['cor8'] = 'orange'
                                elif i == 16:
                                    data['cor9'] = 'orange'
                                elif i == 18:
                                    data['cor10'] = 'orange'
                        else:
                            diferente += 1
                            data['diferente'] = diferente
                            if i == 0:
                                data['cor1'] = 'red'
                            elif i == 2:
                                data['cor2'] = 'red'
                            elif i == 4:
                                data['cor3'] = 'red'
                            elif i == 6:
                                data['cor4'] = 'red'
                            elif i == 8:
                                data['cor5'] = 'red'
                            elif i == 10:
                                data['cor6'] = 'red'
                            elif i == 12:
                                data['cor7'] = 'red'
                            elif i == 14:
                                data['cor8'] = 'red'
                            elif i == 16:
                                data['cor9'] = 'red'
                            elif i == 18:
                                data['cor10'] = 'red'
                    elif resultado[ordem[i]] - resultado[ordem[i+1]] == palpite[ordem[i]] - palpite[ordem[i+1]]:
                        if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                            exato += 1
                            data['exato'] = exato
                            total += 18
                            data['total'] = total
                            if i == 0:
                                data['cor1'] = 'blue'
                            elif i == 2:
                                data['cor2'] = 'blue'
                            elif i == 4:
                                data['cor3'] = 'blue'
                            elif i == 6:
                                data['cor4'] = 'blue'
                            elif i == 8:
                                data['cor5'] = 'blue'
                            elif i == 10:
                                data['cor6'] = 'blue'
                            elif i == 12:
                                data['cor7'] = 'blue'
                            elif i == 14:
                                data['cor8'] = 'blue'
                            elif i == 16:
                                data['cor9'] = 'blue'
                            elif i == 18:
                                data['cor10'] = 'blue'
                        else:
                            igual += 1
                            data['igual'] = igual
                            total += 9
                            data['total'] = total
                            if i == 0:
                                data['cor1'] = 'orange'
                            elif i == 2:
                                data['cor2'] = 'orange'
                            elif i == 4:
                                data['cor3'] = 'orange'
                            elif i == 6:
                                data['cor4'] = 'orange'
                            elif i == 8:
                                data['cor5'] = 'orange'
                            elif i == 10:
                                data['cor6'] = 'orange'
                            elif i == 12:
                                data['cor7'] = 'orange'
                            elif i == 14:
                                data['cor8'] = 'orange'
                            elif i == 16:
                                data['cor9'] = 'orange'
                            elif i == 18:
                                data['cor10'] = 'orange'
                    else:
                        diferente += 1
                        data['diferente'] = diferente
                        if i == 0:
                            data['cor1'] = 'red'
                        elif i == 2:
                            data['cor2'] = 'red'
                        elif i == 4:
                            data['cor3'] = 'red'
                        elif i == 6:
                            data['cor4'] = 'red'
                        elif i == 8:
                            data['cor5'] = 'red'
                        elif i == 10:
                            data['cor6'] = 'red'
                        elif i == 12:
                            data['cor7'] = 'red'
                        elif i == 14:
                            data['cor8'] = 'red'
                        elif i == 16:
                            data['cor9'] = 'red'
                        elif i == 18:
                            data['cor10'] = 'red'
        i += 1

    return render(request, 'app/resultado.html', data)

def caminhocalculadora(request):
    data = {}

    data['rodada'] = ResultadosBrasileirao.objects.all()
    data['usuario'] = Brasileirao.objects.all()
    return render(request, 'app/caminhocalculadora.html', data)


def calculadoradoispontozero(request):
    data = {}
    data['classificacao'] = PontuacaoBrasileirao.objects.all()
    data['rodada']= request.GET['rodada']
    resultado = ResultadosBrasileirao.objects.all()
    resultado = resultado.filter(Rodada=str(request.GET['rodada']))
    data['resultadoobj'] = resultado
    resultado = resultado.first()

    palpite = Brasileirao.objects.all()
    palpite = palpite.filter(Rodada=str(request.GET['rodada']))
    palpite = palpite.filter(user=request.GET['usuario'])
    data['palpiteobj'] = palpite
    palpite = palpite.first()

    ordem = OrdenacaoBrasileirao.objects.all()
    ordem = ordem.filter(Rodada=str(request.GET['rodada']))
    data['ordemobj'] = ordem
    if ordem:
        times = ordem.first()
        time1 = times.AthleticoPR
        time2 = times.Palmeiras
        time3 = times.Corinthians
        time4 = times.Internacional
        time5 = times.AtleticoMG
        time6 = times.Fluminense
        time7 = times.Santos
        time8 = times.SaoPaulo
        time9 = times.Flamengo
        time10 = times.Botafogo
        time11 = times.Avai
        time12 = times.Bragantino
        time13 = times.AtleticoGO
        time14 = times.Goias
        time15 = times.Ceara
        time16 = times.Coritiba
        time17 = times.AmericaMG
        time18 = times.Cuiaba
        time19 = times.Juventude
        time20 = times.Fortaleza
        ordem = [time1, time2, time3, time4, time5, time6, time7, time8, time9, time10, time11, time12, time13, time14, time15, time16, time17, time18, time19, time20]
        data['ordem'] = ordem
    else:
        return redirect('/caminhocalculadora/')
    if palpite:
        ttime1 = palpite.AthleticoPR
        ttime2 = palpite.Palmeiras
        ttime3 = palpite.Corinthians
        ttime4 = palpite.Internacional
        ttime5 = palpite.AtleticoMG
        ttime6 = palpite.Fluminense
        ttime7 = palpite.Santos
        ttime8 = palpite.SaoPaulo
        ttime9 = palpite.Flamengo
        ttime10 = palpite.Botafogo
        ttime11 = palpite.Avai
        ttime12 = palpite.Bragantino
        ttime13 = palpite.AtleticoGO
        ttime14 = palpite.Goias
        ttime15 = palpite.Ceara
        ttime16 = palpite.Coritiba
        ttime17 = palpite.AmericaMG
        ttime18 = palpite.Cuiaba
        ttime19 = palpite.Juventude
        ttime20 = palpite.Fortaleza
        palpite = {"AthleticoPR": ttime1, "Palmeiras": ttime2, "Corinthians": ttime3 , "Internacional": ttime4, "AtleticoMG": ttime5, "Fluminense": ttime6, "Santos": ttime7, "SaoPaulo": ttime8, "Flamengo": ttime9, "Botafogo": ttime10, "Avai": ttime11, "Bragantino": ttime12, "AtleticoGO": ttime13, "Goias": ttime14, "Ceara": ttime15, "Coritiba": ttime16, "AmericaMG": ttime17, "Cuiaba": ttime18, "Juventude": ttime19, "Fortaleza": ttime20}
        data['palpite'] = palpite
    else:
        return redirect('/caminhocalculadora/')
    tttime1 = resultado.AthleticoPR
    tttime2 = resultado.Palmeiras
    tttime3 = resultado.Corinthians
    tttime4 = resultado.Internacional
    tttime5 = resultado.AtleticoMG
    tttime6 = resultado.Fluminense
    tttime7 = resultado.Santos
    tttime8 = resultado.SaoPaulo
    tttime9 = resultado.Flamengo
    tttime10 = resultado.Botafogo
    tttime11 = resultado.Avai
    tttime12 = resultado.Bragantino
    tttime13 = resultado.AtleticoGO
    tttime14 = resultado.Goias
    tttime15 = resultado.Ceara
    tttime16 = resultado.Coritiba
    tttime17 = resultado.AmericaMG
    tttime18 = resultado.Cuiaba
    tttime19 = resultado.Juventude
    tttime20 = resultado.Fortaleza
    resultado = {"AthleticoPR": tttime1, "Palmeiras": tttime2, "Corinthians": tttime3, "Internacional": tttime4, "AtleticoMG": tttime5, "Fluminense": tttime6, "Santos": tttime7, "SaoPaulo": tttime8, "Flamengo": tttime9, "Botafogo": tttime10, "Avai": tttime11, "Bragantino": tttime12, "AtleticoGO": tttime13, "Goias": tttime14, "Ceara": tttime15, "Coritiba": tttime16, "AmericaMG": tttime17, "Cuiaba": tttime18, "Juventude": tttime19, "Fortaleza": tttime20}
    data['resultado'] = resultado

    i = 0
    igual = 0
    exato = 0
    bonus = 0
    diferente = 0
    total = 0
    while i < 19:
        if i % 2 == 0:
            if resultado[ordem[i]] != None:
                if resultado[ordem[i+1]] != None:
                    if resultado[ordem[i]] - resultado[ordem[i+1]] > 0:
                        if palpite[ordem[i]] - palpite[ordem[i+1]] > 0:
                            if resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[ordem[i + 1]]:
                                if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                                    exato += 1
                                    data['exato'] = exato
                                    total += 18
                                    data['total'] = total
                                else:
                                    bonus += 1
                                    data['bonus'] = bonus
                                    total += 12
                                    data['total'] = total
                            else:
                                igual += 1
                                data['igual'] = igual
                                total += 9
                                data['total'] = total
                        else:
                            diferente += 1
                            data['diferente'] = diferente
                    elif resultado[ordem[i]] - resultado[ordem[i+1]] < 0:
                        if palpite[ordem[i]] - palpite[ordem[i+1]] < 0:
                            if resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[ordem[i + 1]]:
                                if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                                    exato += 1
                                    data['exato'] = exato
                                    total += 18
                                    data['total'] = total
                                else:
                                    bonus += 1
                                    data['bonus'] = bonus
                                    total += 12
                                    data['total'] = total
                            else:
                                igual += 1
                                data['igual'] = igual
                                total += 9
                                data['total'] = total
                        else:
                            diferente += 1
                            data['diferente'] = diferente
                    elif resultado[ordem[i]] - resultado[ordem[i+1]] == palpite[ordem[i]] - palpite[ordem[i+1]]:
                        if resultado[ordem[i]] - palpite[ordem[i]] == 0:
                            exato += 1
                            data['exato'] = exato
                            total += 18
                            data['total'] = total
                        else:
                            igual += 1
                            data['igual'] = igual
                            total += 9
                            data['total'] = total
                    else:
                        diferente += 1
                        data['diferente'] = diferente
        i += 1
    verificacao = PontuacaoBrasileirao.objects.all()
    verificacao = verificacao.filter(Rodada=request.GET['rodada'])
    verificacao = verificacao.filter(user=request.GET['usuario'])

    if verificacao:
        verificacao = verificacao.first()
        verificacaopontos = verificacao.PONTOS
        verificacaoerros = verificacao.ER
        if verificacaoerros != None:
            if verificacaopontos == total:
                data['verificacao'] = 0
                return render(request, 'app/tabelapontuacao.html', data)
        verificacao.delete()
    userid = request.GET['usuario']
    rodada = request.GET['rodada']
    pontuacao = PontuacaoBrasileirao(user_id=userid, Rodada=rodada, RE=exato, RB=bonus, RP=igual, ER=diferente, PONTOS=total)
    pontuacao.save()
    return render(request, 'app/tabelapontuacao.html', data)

    #def get(self, request, rodada, *args, **kwargs):
        #result = ResultadosBrasileirao.objects.filter(Rodada=rodada)
        #return render(request, 'app/resultado.html', result)
    #return render(request, 'app/resultado.html')

#context = super(ResultadosBrasileirao).get_context_data(**kwargs)
#context['resultado'] = ResultadosBrasileirao.objects.all()
#context['resultado'] = context['resultado'].filter(Rodada=rodada)
#return render(request, 'app/resultado.html', context)

    #def form_valid(self, form, rodada):
        #data = {}
        #data['res'] = ResultadosBrasileirao.objects.all()
        #data['res'] = data['res'].filter(Rodada=rodada)
        #result = ResultadosBrasileirao.objects.filter(Rodada=rodada)
        #return render(request, 'app/resultado.html', result, data)