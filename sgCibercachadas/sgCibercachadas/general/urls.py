from django.urls import include, path
from django.contrib.auth import views as auth_views
from general.views import *
from general.views import Home

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='general/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='general/login.html'),name='logout'),
    path('perfil',PerfilView.as_view()),
    path('perfil/cambiar',PerfilPasswordView.as_view())
]