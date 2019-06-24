from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic


class Home(LoginRequiredMixin,generic.TemplateView):
    template_name = 'general/home.html'
    login_url='general:login'
    

class Login(generic.TemplateView):
    template_name = 'general/login.html'

class PerfilView(generic.TemplateView):
    template_name='general/perfil.html'
