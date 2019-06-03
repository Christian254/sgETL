from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic


class Home(generic.TemplateView):
    template_name = 'general/home.html'

class Login(generic.TemplateView):
    template_name = 'general/login.html'

