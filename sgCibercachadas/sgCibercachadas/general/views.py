from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from general.forms import PasswordForm
from django.views import generic 
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class Home(LoginRequiredMixin,generic.TemplateView):
    template_name = 'general/home.html'
    login_url='general:login'
    

class Login(LoginRequiredMixin,generic.TemplateView):
    template_name = 'general/login.html'
    login_url='general:login'


class PerfilView(LoginRequiredMixin,generic.TemplateView):
    template_name='general/perfil.html'
    login_url='general:login'

class PerfilPasswordView(LoginRequiredMixin,generic.TemplateView):
    template_name='general/passwd.html'
    login_url="general:login"
    def post(self,request,*args,**kwargs):
        form =  PasswordForm(user=request.user, data=request.POST or None)
    
        if form.is_valid():
            user_to_update=User.objects.get(username=request.user)
            user_to_update.set_password(request.POST.get('new_password'))
            user_to_update.save()

            messages.add_message(request, messages.SUCCESS, 'Se actualizo contraseña con exito')
            update_session_auth_hash(request,user_to_update)

            return redirect('/perfil')
        else:
            return render(request,self.template_name,{'form':form})