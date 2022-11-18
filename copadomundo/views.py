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
    data['palpites'] = Palpites.objects.all()
    data['palpites'] = data['palpites'].filter(user=request.user)
    return render(request, 'copadomundo/home.html', data)

@login_required
def palpite(request, Rodada, Jogo):
    jogo = Jogos.objects.all()
    jogo = jogo.filter(Rodada=Rodada)
    data = {}
    data['jogo'] = jogo.filter(Jogo=Jogo)
    data['Rodada'] = Rodada
    data['Jogo'] = Jogo
    return render(request, 'copadomundo/save.html', data)

@login_required
def save(request):
    if not request.GET['home']:
        return redirect(reverse("palpite", kwargs={'Rodada':request.GET['Rodada'], 'Jogo':request.GET['Jogo']}))
    if not request.GET['away']:
        return redirect(reverse("palpite", kwargs={'Rodada':request.GET['Rodada'], 'Jogo':request.GET['Jogo']}))
    jogo = Jogos.abjects.all()
    jogo = jogo.filter(Jogo=int(request.GET['Jogo']))
    jogo = jogo.first()
    time1 = jogo.Time1
    time2 = jogo.Time2
    palpite = Palpites(Rodada=request.GET['Rodada'], user=request.user)
    data = {}
    data['home'] = request.GET['home']
    data['away'] = request.GET['away']
    data['Rodada'] = request.GET['Rodada']
    data['Jogo'] = request.GET['Jogo']
    return render(request, 'copadomundo/home.html', data)

class PalpiteList(LoginRequiredMixin, ListView):
    model = Palpites
    context_object_name = 'palpites'
    template_name = 'palpites_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['palpites'] = Palpites.objects.all()
        context['palpites'] = context['palpites'].filter(user=self.request.user)
        return context

    def filter(self, user):
        pass

    @classmethod
    def user_id(cls):
        pass

class PalpiteCreate(LoginRequiredMixin, CreateView):
    model = Palpites
    template_name = 'copadomundo/home.html'
    fields = '__all__'
    context_object_name = 'palpites'
    success_url = reverse_lazy('palpites')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteCreate, self).form_valid(form)


class PalpiteUpdate(LoginRequiredMixin, UpdateView):
    model = Palpites
    fields = '__all__'
    success_url = reverse_lazy('palpites')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteUpdate, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verficacao se já passou do horario para atualizar palpite (acessando pela URL)
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 11, 8, 21, 30)
        return context

class PalpiteDetail(LoginRequiredMixin, DetailView):
    model = Palpites
    context_object_name = 'palpites'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verficacao se já passou do horario para visualizar o palpite
        context['horario'] = datetime.datetime.now()
        context['horalimite'] = datetime.datetime(2022, 11, 8, 21, 30)
        return context