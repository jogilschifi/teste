"""teste URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import bemvindo, dashboard, grupos, PalpiteList, PalpiteDetail, PalpiteCreate, PalpiteUpdate, PalpiteDelete, CustomLoginView, RegisterPage, pontuacao, desempate, rodada, resultado, classificacao, classificacaogrupo, classificacaoporrodada, classificacaoporrodadagrupo, classificacaodoispontozero, caminhocalculadora, calculadoradoispontozero, perfilusuarios, CopadoBrasilList, CopadoBrasilCreate, CopadoBrasilUpdate, CopadoBrasilDetail
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bemvindo),
    path('ligas/', grupos, name='ligas'),
    path('classificacao/<group>/', classificacaogrupo, name='classificacao'),
    path('home/', dashboard, name='home'),
    path('brasileirao/', PalpiteList.as_view(), name='palpites'),
    path('<int:pk>/<user>/', perfilusuarios, name='perfilusuarios'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('palpite/<int:pk>/', PalpiteDetail.as_view(), name='palpitedetail'),
    path('palpitecreate/', PalpiteCreate.as_view(), name='palpitecreate'),
    path('palpiteupdate/<int:pk>/', PalpiteUpdate.as_view(), name='palpiteupdate'),
    path('copadobrasil/', CopadoBrasilList.as_view(), name='copadobrasil'),
    path('copadobrasilcreate/', CopadoBrasilCreate.as_view(), name='copadobrasilcreate'),
    path('copadobrasilupdate/<int:pk>/', CopadoBrasilUpdate.as_view(), name='copadobrasilupdate'),
    path('copadobrasil/<int:pk>/', CopadoBrasilDetail.as_view(), name='copadobrasildetail'),
    #path('palpitedelete/<int:pk>/', PalpiteDelete.as_view(), name='palpitedelete'),
    path('pontuacao/', pontuacao),
    path('desempate/', desempate),
    path('rodada/', rodada),
    path('resultado/', resultado),
    path('classificacao/', classificacao),
    path('classificacaoporrodada/', classificacaoporrodada),
    path('classificacaoporrodadagrupo/', classificacaoporrodadagrupo),
    path('classificacaodoispontozero/', classificacaodoispontozero),
    path('caminhocalculadora/', caminhocalculadora),
    path('calculadoradoispontozero/', calculadoradoispontozero),

]
