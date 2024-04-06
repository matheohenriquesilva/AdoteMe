from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.logar, name="login"),
    path('sair/', views.sair, name='sair'),
    path('', views.welcome, name='welcome'),
    path('admin/', views.admin, name='admin'),
    path('guia/', views.guia, name='guia'),
    path('creditos/', views.creditos, name='creditos')
]