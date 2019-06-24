from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import Http404

from administrador.forms import *

class AdminUsuariosView(generic.ListView):
    model = User
    template_name='administrador/admin_usuarios.html'
    context_object_name = "obj"
    paginate_by = 8

class CrearUsuariosView(generic.TemplateView):
    template_name='administrador/crear_usuarios.html'
    
    def get(self,request,*args,**kwargs):
        form= UsuarioForm()
        return render(request,self.template_name,{"form":form})    
    def post(self,request,*args,**kwargs):   
        form= UsuarioForm(request.POST)
        if form.is_valid():
            my_group = Group.objects.get(id=request.POST.get('rol')) 
            user = User.objects.create_user(
                                username=request.POST.get('username'),
                                first_name=request.POST.get('nombres'),
                                last_name=request.POST.get('apellidos'),
                                email=request.POST.get('email'),
                                password=request.POST.get('password'))
            my_group.user_set.add(user)
            messages.add_message(request, messages.SUCCESS, 'Ingreso del Usuario con Username: '+request.POST.get('username')+' Contraseña: '+request.POST.get('password'))

            return redirect(self.request.path_info)
        else:
            form.AddIsInvalid()
            return render(request,self.template_name,{"form":form})

class EditarUsuariosView(generic.TemplateView):
    template_name='administrador/editar_usuarios.html'


    def get(self,request,*args,**kwargs):
        form= UsuarioEditForm()
        usuario=User.objects.filter(pk=self.kwargs['id']).first
        if not usuario:
           return redirect('administrador:admin_gestion_usuarios')
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):   
        form= UsuarioEditForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Actualizacion del Usuario con Username: '+request.POST.get('username'))

            return redirect(self.request.path_info)
        else:
            form.AddIsInvalid()
            return render(request,self.template_name,{"form":form})
