from urllib import request
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Max

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserRegisterForm, UserUpdateForm

import datetime

from operator import itemgetter

from .models import PalpitesPGL, PalpitesFormula1, PontuacaoF1, PontuacaoTotalF1, Brasileirao, ResultadosBrasileirao, OrdenacaoBrasileirao, PontuacaoBrasileirao, PontuacaoTotalBrasileirao, CopadoBrasil, ResultadosCopadoBrasil
from django.contrib.auth.models import Group, User, GroupManager

# Create your views here.

def bemvindo(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    return render(request, 'app/bemvindo.html')

@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')

@login_required
def liga(request, group):
    users = User.objects.all()
    ultimo_id = users.last()
    ultimo_id = ultimo_id.id + 1
    count = 0
    lista_liga = []
    for i in range(ultimo_id):
        user_grupos = users.filter(id=i)
        usuario = user_grupos.first()
        if usuario:
            user_grupos = usuario.groups.all()
            user_grupos = user_grupos.filter(name=group)
            if user_grupos:
                lista_liga.append({"id": i, "user": usuario.username, "posição": i + 1 - count})
            else:
                count += 1
        else:
            count += 1
    data = {}
    data['membros'] = lista_liga
    data['group'] = group
    return render(request, 'app/grupos.html',data)

@login_required
def grupos(request):
    grupos = Group.objects.all()
    users = User.objects.all()
    data = {}
    data['users'] = users
    def group_sort(clas):
        return clas.id
    group = sorted(grupos, key=group_sort)
    data['group'] = group
    #grupos = []
    #for i in users:
    #    groups = users.groups.all()
    #    if groups:
    #        grupos.append({"id": i, "groups": groups})
    #data['grupos'] = grupos
    return render(request, 'app/grupos.html', data)

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, **kwargs)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)


    context = {
        'u_form': u_form,
    }

    return render(request, 'app/profile.html', context)

@login_required
def perfilusuarios(request, pk, user):
    data = {}
    # Verificacao se outros usuários vao poder ver palpite da ultima ou da atual rodada
    horario = datetime.datetime.now()
    horalimite = datetime.datetime(2022, 11, 13, 16, 00)
    data['horario'] = horario
    data['horalimite'] = horalimite
    if horalimite > horario:
        rod = 37
    else:
        rod = 38
    data['rod'] = rod
    data['palpites'] = Brasileirao.objects.all()
    data['palpites'] = data['palpites'].filter(user_id=pk)
    data['palpites'] = data['palpites'].filter(Rodada=rod)
    data['palpites'] = data['palpites'].first()
    rodadas = Brasileirao.objects.all()
    rodadas = rodadas.filter(user_id=pk)
    if rodadas:
        def rodadas_sort(clas):
            return clas.Rodada
        rodadas = sorted(rodadas, key=rodadas_sort)
        data['rodadas'] = rodadas
    data['pk'] = pk
    data['user'] = user
    data['classificacao'] = PontuacaoTotalBrasileirao.objects.all()
    data['classificacao'] = data['classificacao'].filter(user_id=pk)
    rodada = data['classificacao'].aggregate(Max('Rodada'))
    rodada = rodada["Rodada__max"]
    data['classificacao'] = data['classificacao'].filter(Rodada=rodada)
    data['classificacao'] = data['classificacao'].first()
    return render(request, 'app/perfilusuarios.html', data)


class PalpiteList(LoginRequiredMixin, ListView):
    model = Brasileirao
    context_object_name = 'palpites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verficacao se usuario irá palpitar ou atualizar palpite
        context['palpites'] = context['palpites'].filter(user=self.request.user)
        context['palpites'] = context['palpites'].filter(Rodada=38)
        # Verficacao se usuario pode palpitar/atualizar palpite ou visualizar palpite
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 11, 13, 16, 00)
        context['temporestante'] = context['horalimite'] - context['horario']
        context['classificacao'] = PontuacaoTotalBrasileirao.objects.all()
        context['classificacao'] = context['classificacao'].filter(user=self.request.user)
        rodada = context['classificacao'].aggregate(Max('Rodada'))
        rodada = rodada["Rodada__max"]
        context['classificacao'] = context['classificacao'].filter(Rodada=rodada)
        context['classificacao'] = context['classificacao'].first()
        return context

    def filter(self, user):
        pass

    @classmethod
    def user_id(cls):
        pass


class PalpiteCreate(LoginRequiredMixin, CreateView):
    model = Brasileirao
    fields = '__all__'
    context_object_name = 'palpites'
    success_url = reverse_lazy('palpites')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificacao se usuario já palpitou (acessando pela URL)
        context['dados'] = Brasileirao.objects.all()
        context['dados'] = context['dados'].filter(user=self.request.user)
        context['dados'] = context['dados'].filter(Rodada=38)
        # Verficacao se já passou do horario para palpitar (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 11, 13, 16, 00)
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
        # Verficacao se já passou do horario para atualizar palpite (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 11, 13, 16, 00)
        return context

class PalpiteDetail(LoginRequiredMixin, DetailView):
    model = Brasileirao
    context_object_name = 'palpites'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verficacao se já passou do horario para visualizar o palpite
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 11, 13, 16, 00)
        return context


class PalpiteDelete(LoginRequiredMixin, DeleteView):
    model = Brasileirao
    success_url = reverse_lazy('palpites')

@login_required
def pontuacao(request):
    return render(request, 'app/pontuacao.html')
@login_required
def desempate(request):
    return render(request, 'app/desempate.html')
@login_required
def rodada(request,pk):
    data = {}
    rodadas = Brasileirao.objects.all()
    rodadas = rodadas.filter(user_id=pk)
    if rodadas:
        def rodadas_sort(clas):
            return clas.Rodada

        rodadas = sorted(rodadas, key=rodadas_sort)
        data['rodadas'] = rodadas
    return render(request, 'app/rodada.html', data)
@login_required
def classificacao(request):
    data = {}
    classificacao = PontuacaoTotalBrasileirao.objects.all()
    if classificacao:
        rodada = classificacao.aggregate(Max('Rodada'))
        rodada = rodada["Rodada__max"]
        rodadas = ResultadosBrasileirao.objects.all()
        classificacao = classificacao.filter(Rodada=rodada)
        def classif_sort(clas):
            return clas.PONTOS, clas.RE, clas.RB, -clas.ER, -clas.id
        classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)

        data['rodadas'] = rodadas
        data['rodada'] = rodada
        usuarios = len(classificacao)

        cla = []
        for i in range(usuarios):
            classifnova = classificacao_sort[i]
            cla.append({"PONTOS":classifnova.PONTOS, "RE":classifnova.RE, "RB":classifnova.RB, "RP":classifnova.RP, "user":classifnova.user, "id":classifnova.user_id, "posicao":i+1})
        data['cla'] = cla
        return render(request, 'app/classificacao.html', data)

    data['cla'] = Brasileirao.objects.all()
    return render(request, 'app/classificacao.html', data)
@login_required
def classificacaogrupo(request, group):
    #Rodada de início ligas
    if group == 'Bem Amigos':
        rodadamin = 34
    elif group == 'Uefa League':
        rodadamin = 36
    else:
        classificacao = PontuacaoTotalBrasileirao.objects.all()
        rodada = classificacao.aggregate(Max('Rodada'))
        rodada = rodada["Rodada__max"]
        rodadas = ResultadosBrasileirao.objects.all()
        classificacao = classificacao.filter(Rodada=rodada)
        def classif_sort(clas):
            return clas.PONTOS, clas.RE, clas.RB, -clas.id
        classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)
        data = {}
        data['group'] = group
        data['rodadas'] = rodadas
        usuarios = len(classificacao)

        users = User.objects.all()
        ultimo_id = users.last()
        ultimo_id = ultimo_id.id + 1

        count = 0
        lista_liga = []
        for i in range(ultimo_id):
            user_grupos = users.filter(id=i)
            usuario = user_grupos.first()
            if usuario:
                user_grupos = usuario.groups.all()
                user_grupos = user_grupos.filter(name=group)
                if user_grupos:
                    verificacao = classificacao.filter(user_id=i)
                    if verificacao:
                        lista_liga.append(i)
                    else:
                        count += 1
        data['membros'] = len(lista_liga) + count
        data['rodadamin'] = 28
        cla = []
        j = 0
        for i in range(usuarios):
            classifnova = classificacao_sort[i]
            if classifnova.user_id in lista_liga:
                cla.append(
                    {"PONTOS": classifnova.PONTOS, "RE": classifnova.RE, "RB": classifnova.RB, "RP": classifnova.RP,
                     "user": classifnova.user, "id": classifnova.user_id, "posicao": i + 1 - j})
            else:
                j += 1
        data['cla'] = cla
        return render(request, 'app/classificacao.html', data)

    classificacaomin = PontuacaoTotalBrasileirao.objects.all()
    classificacaomin = classificacaomin.filter(Rodada=str(int(rodadamin)-1))
    classificacaomax = PontuacaoTotalBrasileirao.objects.all()
    rodada = classificacaomax.aggregate(Max('Rodada'))
    rodada = rodada["Rodada__max"]
    classificacaomax = classificacaomax.filter(Rodada=rodada)
    usuariosmax = len(classificacaomax)
    usuariosmin = len(classificacaomin)
    usuariosminver = usuariosmin - 1

    classificacaomaxima = []
    for i in range(usuariosmax):
        classificacaomaxima.append(classificacaomax[i])
    classificacaominima = []
    for i in range(usuariosmin):
        classificacaominima.append(classificacaomin[i])

    count = 0
    classificacao = []
    for i in range(usuariosmax):
        usermax = classificacaomaxima[i].user_id
        for j in range(usuariosmin):
            usermin = classificacaominima[j].user_id
            if usermax == usermin:
                classificacao.append({"PONTOS": classificacaomaxima[i].PONTOS - classificacaominima[j].PONTOS,
                                                                "RE": classificacaomaxima[i].RE - classificacaominima[j].RE,
                                                            "RB": classificacaomaxima[i].RB - classificacaominima[j].RB,
                                                                "RP": classificacaomaxima[i].RP - classificacaominima[j].RP,
                                                                "user": classificacaomaxima[i].user, "user_id":classificacaomaxima[i].user_id})
                count += 1
                break
            else:
                if j == usuariosminver:
                    if i == count:
                        classificacao.append({"PONTOS": classificacaomaxima[i].PONTOS, "RE": classificacaomaxima[i].RE,
                                                      "RB": classificacaomaxima[i].RB,"RP": classificacaomaxima[i].RP,
                                                      "user": classificacaomaxima[i].user, "user_id": classificacaomaxima[i].user_id})
                        count += 1

    data = {}
    data['rodadamin'] = rodadamin
    data['group'] = group
    def classif_sort(clas):
        return clas["PONTOS"], clas["RE"], clas["RB"], -clas["user_id"]
    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)

    #Rodadas apartir do início das ligas
    rodadasobj = ResultadosBrasileirao.objects.all()
    rodadas = []
    for i in range(len(rodadasobj)):
        x = rodadasobj[i].Rodada
        if int(rodadasobj[i].Rodada) >= rodadamin:
            rodadas.append({"Rodada": x})

    data['rodadas'] = rodadas
    data['rodada'] = rodada
    usuarios = len(classificacao)

    users = User.objects.all()
    ultimo_id = users.last()
    ultimo_id = ultimo_id.id + 1

    count = 0
    lista_liga = []
    for i in range(ultimo_id):
        user_grupos = users.filter(id=i)
        usuario = user_grupos.first()
        if usuario:
            user_grupos = usuario.groups.all()
            user_grupos = user_grupos.filter(name=group)
            if user_grupos:
                verificacao = classificacaomax.filter(user_id=i)
                if verificacao:
                    lista_liga.append(i)
                else:
                    count += 1
    data['lista_liga'] = lista_liga
    data['membros'] = len(lista_liga) + count
    cla = []
    j = 0
    for i in range(usuarios):
        classifnova = classificacao_sort[i]
        if classifnova["user_id"] in lista_liga:
            cla.append({"PONTOS":classifnova["PONTOS"], "RE":classifnova["RE"], "RB":classifnova["RB"], "RP":classifnova["RP"], "user":classifnova["user"], "id":classifnova["user_id"], "posicao":i+1-j})
        else:
            j += 1
    data['cla'] = cla
    return render(request, 'app/classificacao.html', data)

@login_required
def classificacaoporrodadagrupo(request, group):
    #Rodada de início ligas
    if group == 'Bem Amigos':
        rodadamin = 34
    elif group == 'Uefa League':
        rodadamin = 36
    else:
        rodadamin = 'geral'

    tipo = request.GET['tipo']
    rodada = request.GET['rodada']

    global classificacao
    if tipo == '0':
        return redirect(reverse("classificacaogrupo", kwargs={'group':group}))
    else:
        if rodada == '0':
            return redirect(reverse("classificacaogrupo", kwargs={'group':group}))

        elif tipo == '1':
            if not rodadamin == 'geral':
                classificacaomin = PontuacaoTotalBrasileirao.objects.all()
                classificacaomin = classificacaomin.filter(Rodada=str(int(rodadamin) - 1))
                classificacaomax = PontuacaoTotalBrasileirao.objects.all()
                classificacaomax = classificacaomax.filter(Rodada=rodada)
                usuariosmax = len(classificacaomax)
                usuariosmin = len(classificacaomin)
                usuariosminver = usuariosmin - 1

                classificacaomaxima = []
                for i in range(usuariosmax):
                    classificacaomaxima.append(classificacaomax[i])
                classificacaominima = []
                for i in range(usuariosmin):
                    classificacaominima.append(classificacaomin[i])

                count = 0
                classificacao = []
                for i in range(usuariosmax):
                    usermax = classificacaomaxima[i].user_id
                    for j in range(usuariosmin):
                        usermin = classificacaominima[j].user_id
                        if usermax == usermin:
                            classificacao.append({"PONTOS": classificacaomaxima[i].PONTOS - classificacaominima[j].PONTOS,
                                                  "RE": classificacaomaxima[i].RE - classificacaominima[j].RE,
                                                  "RB": classificacaomaxima[i].RB - classificacaominima[j].RB,
                                                  "RP": classificacaomaxima[i].RP - classificacaominima[j].RP,
                                                  "user": classificacaomaxima[i].user,
                                                  "user_id": classificacaomaxima[i].user_id})
                            count += 1
                            break
                        else:
                            if j == usuariosminver:
                                if i == count:
                                    classificacao.append(
                                        {"PONTOS": classificacaomaxima[i].PONTOS, "RE": classificacaomaxima[i].RE,
                                         "RB": classificacaomaxima[i].RB, "RP": classificacaomaxima[i].RP,
                                         "user": classificacaomaxima[i].user, "user_id": classificacaomaxima[i].user_id})
                                    count += 1

                def classif_sort(clas):
                    return clas["PONTOS"], clas["RE"], clas["RB"], -clas["user_id"]
                classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)

                rodadasobj = ResultadosBrasileirao.objects.all()
                rodadas = []
                for i in range(len(rodadasobj)):
                    x = rodadasobj[i].Rodada
                    if int(rodadasobj[i].Rodada) >= rodadamin:
                        rodadas.append({"Rodada": x})
                data = {}
                data['group'] = group
                data['rodadas'] = rodadas
                data['rodada'] = rodada
                usuarios = len(classificacao)

                users = User.objects.all()
                ultimo_id = users.last()
                ultimo_id = ultimo_id.id + 1

                count = 0
                lista_liga = []
                for i in range(ultimo_id):
                    user_grupos = users.filter(id=i)
                    usuario = user_grupos.first()
                    if usuario:
                        user_grupos = usuario.groups.all()
                        user_grupos = user_grupos.filter(name=group)
                        if user_grupos:
                            verificacao = classificacaomax.filter(user_id=i)
                            if verificacao:
                                lista_liga.append(i)
                            else:
                                count += 1
                data['membros'] = len(lista_liga) + count
                data['rodadamin'] = rodadamin
                cla = []
                j = 0
                for i in range(usuarios):
                    classifnova = classificacao_sort[i]
                    if classifnova["user_id"] in lista_liga:
                        cla.append({"PONTOS": classifnova["PONTOS"], "RE": classifnova["RE"], "RB": classifnova["RB"],
                                    "RP": classifnova["RP"], "user": classifnova["user"], "id": classifnova["user_id"],
                                    "posicao": i + 1 - j})
                    else:
                        j += 1
                data['cla'] = cla
                data['tipo'] = int(tipo)
                return render(request, 'app/classificacaoporrodada.html', data)
            else:
                classificacao = PontuacaoTotalBrasileirao.objects.all()
                classificacao = classificacao.filter(Rodada=rodada)
        elif tipo == '2':
            classificacao = PontuacaoBrasileirao.objects.all()
            classificacao = classificacao.filter(Rodada=rodada)

    def classif_sort(clas):
        return clas.PONTOS, clas.RE, clas.RB, -clas.id

    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)
    data = {}
    #Rodadas apartir do início das ligas
    rodadasobj = ResultadosBrasileirao.objects.all()
    if rodadamin == 'geral':
        rodadas = rodadasobj
        data['rodadamin'] = 28
    else:
        data['rodadamin'] = rodadamin
        rodadas = []
        for i in range(len(rodadasobj)):
            x = rodadasobj[i].Rodada
            if int(rodadasobj[i].Rodada) >= rodadamin:
                rodadas.append({"Rodada": x})
    data['rodadas'] = rodadas
    data['group'] = group
    data['rodada'] = int(rodada)
    data['tipo'] = int(tipo)
    usuarios = len(classificacao)

    users = User.objects.all()
    ultimo_id = users.last()
    ultimo_id = ultimo_id.id + 1

    count = 0
    lista_liga = []
    for i in range(ultimo_id):
        user_grupos = users.filter(id=i)
        usuario = user_grupos.first()
        if usuario:
            user_grupos = usuario.groups.all()
            user_grupos = user_grupos.filter(name=group)
            if user_grupos:
                verificacao = classificacao.filter(user_id=i)
                if verificacao:
                    lista_liga.append(i)
                else:
                    count += 1
    data['membros'] = len(lista_liga) + count

    #Maneira burra de converter lista_string em lista
    #lista = []
    #for i in range(len(lista_liga)):
    #    if lista_liga[i] != '[':
    #        if lista_liga[i] != ']':
    #            if lista_liga[i] != ',':
    #                if lista_liga[i] != ' ':
    #                    if lista_liga[i+1] == ',':
    #                       if lista_liga[i-1] == ' ':
    #                            lista.append(int(lista_liga[i]))
    #                        else:
    #                            if lista_liga[i - 1] == '[':
    #                                lista.append(int(lista_liga[i]))
    #                    else:
    #                        if lista_liga[i+1] != ']':
    #                            if lista_liga[i+2] == ',':
    #                                lista.append(10 * int(lista_liga[i]) + int(lista_liga[i + 1]))
    #                            else:
    #                                if lista_liga[i+2] == ']':
    #                                    if lista_liga[i-1] == ' ':
    #                                        lista.append(10 * int(lista_liga[i]) + int(lista_liga[i + 1]))
    #                                else:
    #                                    lista.append(100 * int(lista_liga[i]) + 10 * int(lista_liga[i + 1]) + int(lista_liga[i + 2]))
    #                        elif lista_liga[i-1] == ' ':
    #                                lista.append(int(lista_liga[i]))

    cla = []
    j = 0
    for i in range(usuarios):
        classifnova = classificacao_sort[i]
        if classifnova.user_id in lista_liga:
            cla.append({"PONTOS": classifnova.PONTOS, "RE": classifnova.RE, "RB": classifnova.RB, "RP": classifnova.RP,
                        "user": classifnova.user, "id": classifnova.user_id, "posicao": i + 1 - j})
        else:
            j += 1
    data['cla'] = cla

    return render(request, 'app/classificacaoporrodada.html', data)

@login_required
def classificacaoporrodada(request):
    tipo = request.GET['tipo']
    rodada = request.GET['rodada']
    global classificacao
    if tipo == '0':
        return redirect('/classificacao/')
    else:
        if rodada == '0':
            return redirect('/classificacao/')
        elif tipo == '1':
            classificacao = PontuacaoTotalBrasileirao.objects.all()
            classificacao = classificacao.filter(Rodada=rodada)
        elif tipo == '2':
            classificacao = PontuacaoBrasileirao.objects.all()
            classificacao = classificacao.filter(Rodada=rodada)

    #rodadamin = request.GET['rodadamin']
    #rodadamax = request.GET['rodadamax']
    #if rodadamin != '0':
    #    if rodadamax == '0':
    #        classificacao = PontuacaoBrasileirao.objects.all()
    #        classificacao = classificacao.filter(Rodada=rodadamin)
    #    else:
    #        if rodadamin == '28':
    #            classificacao = PontuacaoTotalBrasileirao.objects.all()
    #            classificacao = classificacao.filter(Rodada=rodadamax)
    #        else:
    #
    #            classificacaomin = PontuacaoTotalBrasileirao.objects.all()
    #            classificacaomin = classificacaomin.filter(Rodada=str(int(rodadamin)-1))
    #            classificacaomax = PontuacaoTotalBrasileirao.objects.all()
    #            classificacaomax = classificacaomax.filter(Rodada=rodadamax)
    #            usuariosmax = len(classificacaomax)
    #            usuariosmin = len(classificacaomin)
    #            usuariosminver = usuariosmin - 1
    #
    #            classificacaomaxima = []
    #            for i in range(usuariosmax):
    #                classificacaomaxima.append(classificacaomax[i])
    #            classificacaominima = []
    #            for i in range(usuariosmin):
    #                classificacaominima.append(classificacaomin[i])
    #
    #            count = 0
    #            classificacao = []
    #            for i in range(usuariosmax):
    #                usermax = classificacaomaxima[i].user_id
    #                for j in range(usuariosmin):
    #                    usermin = classificacaominima[j].user_id
    #                    if usermax == usermin:
    #                        classificacao.append({"PONTOS": classificacaomaxima[i].PONTOS - classificacaominima[j].PONTOS,
    #                                                                        "RE": classificacaomaxima[i].RE - classificacaominima[j].RE,
    #                                                                    "RB": classificacaomaxima[i].RB - classificacaominima[j].RB,
    #                                                                        "RP": classificacaomaxima[i].RP - classificacaominima[j].RP,
    #                                                                        "user": classificacaomaxima[i].user, "user_id":classificacaomaxima[i].user_id})
    #                        count += 1
    #                        break
    #                    else:
    #                        if j == usuariosminver:
    #                            if i == count:
    #                                classificacao.append({"PONTOS": classificacaomaxima[i].PONTOS, "RE": classificacaomaxima[i].RE,
    #                                                              "RB": classificacaomaxima[i].RB,"RP": classificacaomaxima[i].RP,
    #                                                              "user": classificacaomaxima[i].user, "user_id": classificacaomaxima[i].user_id})
    #                                count += 1
    #            def classif_sort(clas):
    #                return clas["PONTOS"], clas["RE"], clas["RB"], clas["user_id"]
    #            classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)
    #            #itemgetter('PONTOS', 'RE', 'RB', 'RP', 'user_id')
    #            cla = []
    #            for i in range(usuariosmax):
    #                classifnova = classificacao_sort[i]
    #                cla.append(
    #                    {"PONTOS": classifnova["PONTOS"], "RE": classifnova["RE"], "RB": classifnova["RB"], "RP": classifnova["RP"],
    #                     "user": classifnova["user"], "id": classifnova["user_id"], "posicao": i + 1})
    #            rodadas = ResultadosBrasileirao.objects.all()
    #            data = {}
    #            data['rodadas'] = rodadas
    #            data['rodadamin'] = int(rodadamin)
    #            data['rodadamax'] = int(rodadamax)
    #            data['cla'] = cla
    #            return render(request, 'app/classificacaoporrodada.html', data)
    #else:
    #    if rodadamax != '0':
    #        classificacao = PontuacaoTotalBrasileirao.objects.all()
    #        classificacao = classificacao.filter(Rodada=rodadamax)
    #    else:
    #        return redirect('/classificacao/')
    #data = {}
    #data['cla'] = classificacao
    #return render(request, 'app/classificacaoporrodada.html', data)

    def classif_sort(clas):
        return clas.PONTOS, clas.RE, clas.RB, -clas.id

    #classificacao = classificacao.first()
    #data = {}
    #data['classificacao'] = classificacao
    #return render(request, 'app/classificacaoporrodada.html', data)
    rodadas = ResultadosBrasileirao.objects.all()
    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)
    data = {}
    data['rodadas'] = rodadas
    data['rodada'] = int(rodada)
    data['tipo'] = int(tipo)
    usuarios = len(classificacao)

    cla = []
    for i in range(usuarios):
        classifnova = classificacao_sort[i]
        cla.append({"PONTOS": classifnova.PONTOS, "RE": classifnova.RE, "RB": classifnova.RB, "RP": classifnova.RP, "user": classifnova.user, "id":classifnova.user_id, "posicao": i + 1})
    data['cla'] = cla

    return render(request, 'app/classificacaoporrodada.html', data)

@login_required
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
                    if total == totalantigo:
                        if rodada != rodadaantiga:
                            pontuacaototal.save()
            else:
                if pontuacaototal:
                    pontuacaototal.save()

    data = {}
    data['classificacao'] = PontuacaoTotalBrasileirao.objects.all()
    data['rodada'] = ResultadosBrasileirao.objects.all()

    return render(request, 'app/classificacaodoispontozero.html', data)

@login_required
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
            return redirect(reverse("perfilusuarios", kwargs={'pk':int(current_user), 'user':str(user)}))
        return redirect(reverse("rodada", kwargs={'pk':int(current_user)}))
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
            return redirect(reverse("perfilusuarios", kwargs={'pk':int(current_user), 'user':str(user)}))
        return redirect(reverse("rodada", kwargs={'pk':int(current_user)}))
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
                    if palpite[ordem[i]] != None:
                        if palpite[ordem[i + 1]] != None:
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
@login_required
def caminhocalculadora(request):
    data = {}

    data['rodada'] = ResultadosBrasileirao.objects.all()
    data['usuario'] = Brasileirao.objects.all()
    return render(request, 'app/caminhocalculadora.html', data)

@login_required
def calculadoradoispontozero(request):
    data = {}
    data['classificacao'] = PontuacaoBrasileirao.objects.all()
    data['rodada']= request.GET['rodada']
    resul = ResultadosBrasileirao.objects.all()
    resul = resul.filter(Rodada=str(request.GET['rodada']))
    data['resultadoobj'] = resul
    resul = resul.first()

    palpi = Brasileirao.objects.all()
    palpi = palpi.filter(Rodada=str(request.GET['rodada']))

    usuarios = PontuacaoBrasileirao.objects.all()
    usuarios_novos = Brasileirao.objects.all()
    rodadaant = str(int(request.GET['rodada']) - 1)
    rodadaatual = str(request.GET['rodada'])
    usuarios_ant = usuarios.filter(Rodada=rodadaant)
    usuarios_atual = usuarios_novos.filter(Rodada=rodadaatual)
    usuarios_atual = usuarios_atual.aggregate(Max('user_id'))
    usuarios_atual = usuarios_atual["user_id__max"]
    usuarios_atual = usuarios_atual + 1
    usuariomax = usuarios_ant.aggregate(Max('user_id'))
    usuariomax = usuariomax["user_id__max"]
    usuariomax = usuariomax + 1
    if usuarios_atual > usuariomax:
        usuariomax = usuarios_atual

    data['usuariomax'] = usuariomax
    data['salvo'] = 0
    data['salvo1'] = 0
    data['salvo2'] = 0
    data['salvo3'] = 0
    data['salvo4'] = 0
    data['salvo5'] = 0
    for j in range(usuariomax):
        palpite = palpi.filter(user=j)
        if palpite:
            data['salvo1'] += 1
            data['palpiteobj'] = palpite
            palpite = palpite.first()
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
            user = palpite.user
            palpite = {"AthleticoPR": ttime1, "Palmeiras": ttime2, "Corinthians": ttime3, "Internacional": ttime4,
                       "AtleticoMG": ttime5, "Fluminense": ttime6, "Santos": ttime7, "SaoPaulo": ttime8,
                       "Flamengo": ttime9, "Botafogo": ttime10, "Avai": ttime11, "Bragantino": ttime12,
                       "AtleticoGO": ttime13, "Goias": ttime14, "Ceara": ttime15, "Coritiba": ttime16,
                       "AmericaMG": ttime17, "Cuiaba": ttime18, "Juventude": ttime19, "Fortaleza": ttime20, "user": user}
            data['palpite'] = palpite
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
                ordem = [time1, time2, time3, time4, time5, time6, time7, time8, time9, time10, time11, time12, time13,
                         time14, time15, time16, time17, time18, time19, time20]
                data['ordem'] = ordem
            else:
                return redirect('/caminhocalculadora/')
            tttime1 = resul.AthleticoPR
            tttime2 = resul.Palmeiras
            tttime3 = resul.Corinthians
            tttime4 = resul.Internacional
            tttime5 = resul.AtleticoMG
            tttime6 = resul.Fluminense
            tttime7 = resul.Santos
            tttime8 = resul.SaoPaulo
            tttime9 = resul.Flamengo
            tttime10 = resul.Botafogo
            tttime11 = resul.Avai
            tttime12 = resul.Bragantino
            tttime13 = resul.AtleticoGO
            tttime14 = resul.Goias
            tttime15 = resul.Ceara
            tttime16 = resul.Coritiba
            tttime17 = resul.AmericaMG
            tttime18 = resul.Cuiaba
            tttime19 = resul.Juventude
            tttime20 = resul.Fortaleza
            resultado = {"AthleticoPR": tttime1, "Palmeiras": tttime2, "Corinthians": tttime3, "Internacional": tttime4,
                         "AtleticoMG": tttime5, "Fluminense": tttime6, "Santos": tttime7, "SaoPaulo": tttime8,
                         "Flamengo": tttime9, "Botafogo": tttime10, "Avai": tttime11, "Bragantino": tttime12,
                         "AtleticoGO": tttime13, "Goias": tttime14, "Ceara": tttime15, "Coritiba": tttime16,
                         "AmericaMG": tttime17, "Cuiaba": tttime18, "Juventude": tttime19, "Fortaleza": tttime20}
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
                        if resultado[ordem[i + 1]] != None:
                            if palpite[ordem[i]] != None:
                                if palpite[ordem[i + 1]] != None:
                                    if resultado[ordem[i]] - resultado[ordem[i + 1]] > 0:
                                        if palpite[ordem[i]] - palpite[ordem[i + 1]] > 0:
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
                                    elif resultado[ordem[i]] - resultado[ordem[i + 1]] < 0:
                                        if palpite[ordem[i]] - palpite[ordem[i + 1]] < 0:
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
                                    elif resultado[ordem[i]] - resultado[ordem[i + 1]] == palpite[ordem[i]] - palpite[
                                        ordem[i + 1]]:
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

            userid = palpite["user"]
            rodada = request.GET['rodada']
            pontuacao = PontuacaoBrasileirao(user_id=j, Rodada=rodada, RE=exato, RB=bonus, RP=igual, ER=diferente, PONTOS=total)
            #Verificacao
            verificacao = PontuacaoBrasileirao.objects.all()
            verificacao = verificacao.filter(Rodada=request.GET['rodada'])
            verificacao = verificacao.filter(user_id=j)
            verificacao = verificacao.first()
            if verificacao:
                pontos = verificacao.PONTOS
                erro = verificacao.ER
                if pontos == total:
                    if erro == diferente:
                        data['salvo2'] += 1
                else:
                    verificacao.delete()
                    pontuacao.save()
            else:
                pontuacao.save()
        else:
            data['salvo'] += 1
            user = usuarios.filter(user=j)
            if user:
                data['salvo3'] += 1
                verificacao = PontuacaoBrasileirao.objects.all()
                verificacao = verificacao.filter(Rodada=request.GET['rodada'])
                verificacao = verificacao.filter(user_id=j)
                verificacao = verificacao.first()
                if verificacao:
                    pontos = verificacao.PONTOS
                    erro = verificacao.ER
                    if pontos == 0:
                        if erro == 0:
                            data['salvo4'] += 1
                else:
                    pontuacao = PontuacaoBrasileirao(user_id=j, Rodada=int(request.GET['rodada']), RE=0, RB=0, RP=0, ER=0, PONTOS=0)
                    pontuacao.save()
                    data['salvo5'] += 1

    #verificacao = PontuacaoBrasileirao.objects.all()
    #verificacao = verificacao.filter(Rodada=request.GET['rodada'])
    #verificacao = verificacao.filter(user=request.GET['usuario'])

    #if verificacao:
    #    verificacao = verificacao.first()
    #    verificacaopontos = verificacao.PONTOS
    #    verificacaoerros = verificacao.ER
    #    if verificacaoerros != None:
    #        if verificacaopontos == total:
    #            data['verificacao'] = 0
    #            return render(request, 'app/tabelapontuacao.html', data)
    #    verificacao.delete()
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

#def formula1(request):

    #return render(request, 'app/formula1.html')

class PalpiteF1List(LoginRequiredMixin, ListView):
    model = PalpitesFormula1
    context_object_name = 'palpitesf1'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verficacao se usuario irá palpitar ou atualizar palpite
        context['palpitesf1'] = context['palpitesf1'].filter(user=self.request.user)
        # context['palpitesf1'] = context['palpitesf1'].filter(Prova=3)
        # Verficacao se usuario pode palpitar/atualizar palpite ou visualizar palpite
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2024, 3, 24, 1, 00)
        context['temporestante'] = context['horalimite'] - context['horario']
        # context['classificacao'] = PontuacaoTotalBrasileirao.objects.all()
        # context['classificacao'] = context['classificacao'].filter(user=self.request.user)
        # rodada = context['classificacao'].aggregate(Max('Rodada'))
        # rodada = rodada["Rodada__max"]
        # context['classificacao'] = context['classificacao'].filter(Rodada=rodada)
        # context['classificacao'] = context['classificacao'].first()
        return context

    def filter(self, user):
        pass

    @classmethod
    def user_id(cls):
        pass


class PalpiteF1Create(LoginRequiredMixin, CreateView):
    model = PalpitesFormula1
    fields = '__all__'
    context_object_name = 'palpitesf1'
    success_url = reverse_lazy('palpitesf1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificacao se usuario já palpitou (acessando pela URL)
        context['dados'] = PalpitesFormula1.objects.all()
        context['dados'] = context['dados'].filter(user=self.request.user)
        # context['dados'] = context['dados'].filter(Prova=3)
        # Verficacao se já passou do horario para palpitar (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2024, 3, 24, 1, 00)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteF1Create, self).form_valid(form)

class PalpiteF1Update(LoginRequiredMixin, UpdateView):
    model = PalpitesFormula1
    fields = '__all__'
    success_url = reverse_lazy('palpitesf1')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteF1Update, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verficacao se já passou do horario para atualizar palpite (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2024, 3, 24, 1, 00)
        return context

def f1resultado(request):
    classificacao = PontuacaoTotalF1.objects.all()
    etapas = PontuacaoF1.objects.values('Etapa').distinct()
    etapa = classificacao.aggregate(Max('Etapa'))
    etapa = etapa["Etapa__max"]
    #rodadas = ResultadosBrasileirao.objects.all()
    classificacao = classificacao.filter(Etapa=etapa)
    def classif_sort(clas):
        return clas.Pts, -clas.id
    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)

    data = {}
    data['etapas'] = etapas
    data['etapa'] = etapa
    usuarios = len(classificacao)

    cla = []
    for i in range(usuarios):
        classifnova = classificacao_sort[i]
        cla.append({"Pts":classifnova.Pts, "user":classifnova.user, "posicao":i+1})
    data['cla'] = cla
    return render(request, 'app/f1resultado.html', data)

def f1resultadoporrodada(request):
    classificacao = PontuacaoF1.objects.all()
    etapas = PontuacaoF1.objects.values('Etapa').distinct()
    etapa = request.GET['etapa']
    #rodadas = ResultadosBrasileirao.objects.all()
    classificacao = classificacao.filter(Etapa=etapa)
    def classif_sort(clas):
        return clas.Pts, -clas.id
    classificacao_sort = sorted(classificacao, key=classif_sort, reverse=True)

    data = {}
    data['etapas'] = etapas
    data['etapa'] = etapa
    usuarios = len(classificacao)

    cla = []
    for i in range(usuarios):
        classifnova = classificacao_sort[i]
        cla.append({"Pts":classifnova.Pts, "user":classifnova.user, "posicao":i+1})
    data['cla'] = cla
    return render(request, 'app/f1resultadoporrodada.html', data)

class PalpitePGLList(LoginRequiredMixin, ListView):
    model = PalpitesPGL
    fields = '__all__'
    context_object_name = 'palpitespgl'
    success_url = reverse_lazy('palpitespgl')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificacao se usuario já palpitou (acessando pela URL)
        context['dados'] = PalpitesPGL.objects.all()
        context['dados'] = context['dados'].filter(user=self.request.user)
        # context['dados'] = context['dados'].filter(Prova=3)
        # Verficacao se já passou do horario para palpitar (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2024, 3, 21, 9, 00)
        return context

class PalpitePGLCreate(LoginRequiredMixin, CreateView):
    model = PalpitesPGL
    fields = '__all__'
    context_object_name = 'palpitespgl'
    success_url = reverse_lazy('palpitespgl')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificacao se usuario já palpitou (acessando pela URL)
        context['dados'] = PalpitesPGL.objects.all()
        context['dados'] = context['dados'].filter(user=self.request.user)
        # context['dados'] = context['dados'].filter(Prova=3)
        # Verficacao se já passou do horario para palpitar (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2024, 3, 21, 9, 00)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpitePGLCreate, self).form_valid(form)