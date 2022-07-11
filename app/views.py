from urllib import request
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from app.models import Clubes, Brasileirao


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


class PalpiteList(LoginRequiredMixin, ListView):
    model = Brasileirao
    context_object_name = 'palpites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['palpites'] = context['palpites'].filter(user=self.request.user)
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
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteCreate, self).form_valid(form)

def condicao(request):
    current_user = request.user
    data = {}
    data['dados'] = Brasileirao.objects.all().filter(user=current_user)
    return render(request, 'app/brasileirao_form.html', data)

class PalpiteUpdate(LoginRequiredMixin, UpdateView):
    model = Brasileirao
    fields = '__all__'
    success_url = reverse_lazy('palpites')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PalpiteUpdate, self).form_valid(form)


class PalpiteDelete(DeleteView):
    model = Brasileirao
    success_url = reverse_lazy('palpites')


def pontuacao(request):
    current_user = request.user
    data = {}
    data['form'] = Brasileirao.objects.all()
    data['form'] = data['form'].filter(user=current_user)
    return render(request, 'app/pontuacao.html', data)