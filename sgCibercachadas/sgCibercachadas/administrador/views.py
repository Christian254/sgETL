from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import Http404

from administrador.forms import *

class AdminUsuariosView(generic.ListView):
    model = User
    template_name='administrador/admin_usuarios.html'
    context_object_name = "obj"
    ordering=['-id']
    paginate_by = 6


class CrearUsuariosView(generic.TemplateView):
    template_name='administrador/crear_usuarios.html'
    
    def get(self,request,*args,**kwargs):
        form= UsuarioForm()
        return render(request,self.template_name,{"form":form})    
    def post(self,request,*args,**kwargs):   
        form= UsuarioForm(request.POST)
        if form.is_valid():
            my_group = get_object_or_404(Group, pk=request.POST.get('rol'))

            #en caso de que el grupo no sea permitido
            if my_group.id!=3:


                user = User.objects.create_user(
                                    username=request.POST.get('username'),
                                    first_name=request.POST.get('nombres'),
                                    last_name=request.POST.get('apellidos'),
                                    email=request.POST.get('email'),
                                    password=request.POST.get('password'))

                my_group.user_set.add(user)

                messages.add_message(request, messages.SUCCESS, 'Ingreso del Usuario con Username: '
                +request.POST.get('username')+' Contraseña: '+request.POST.get('password'))
            else:
                messages.add_message(request, messages.WARNING, 'Perfil de acceso no permitido ')
            return redirect(self.request.path_info)
        else:
            form.AddIsInvalid()
            return render(request,self.template_name,{"form":form})

class InhabilitarUsuarios(generic.TemplateView):
    template_name="administrador/admin_usuarios.html"

    def post(self,*args, **kwargs):
        user= get_object_or_404(User, pk=self.kwargs['id'])
        user.is_active= (True,False)[user.is_active]   
        user.save()
        return redirect("administrador:admin_gestion_usuarios")




class EditarUsuariosView(generic.TemplateView):
    template_name='administrador/editar_usuarios.html'


    def get(self,request,*args,**kwargs):
        usuario= get_object_or_404(User, pk=self.kwargs['id'])

        form= UsuarioEditForm(initial={
        "username":usuario.username,
        "nombres":usuario.first_name,
        "apellidos":usuario.last_name,
        "email":usuario.email}
        )

        return render(request,self.template_name,{
        "form":form,
        "group":usuario.groups.all()[0].id,
        "groups":Group.objects.all()}
        )

    def post(self,request,*args,**kwargs):   
        form= UsuarioEditForm(request.POST, id=self.kwargs['id'])
        current_user=User.objects.filter(pk=self.kwargs["id"]).first()
        
        if form.is_valid():
           
            #accesing through the user to its groups
            user_groups = User.groups.through.objects.get(user=current_user)
            #overriding the rol from the form
            user_groups.group= get_object_or_404(Group, pk=request.POST.get('rol'))

            #only update if the group has id not equals to 3 (admin user).
            if user_groups.group.id!=3:
                user_groups.save()
             

            #updating only the user data 
            User.objects.filter(pk=self.kwargs['id']).update(username=request.POST.get("username"),
            first_name=request.POST.get("nombres"), last_name=request.POST.get("apellidos"),email=request.POST.get("email"))

            messages.add_message(request, messages.SUCCESS, 'Actualizacion del Usuario con Username: '
            +request.POST.get('username'))

            return redirect(self.request.path_info)
        else:
        
            form.AddIsInvalid()
            return render(request,self.template_name,{"form":form,"group":current_user.groups.all()[0].id,
        "groups":Group.objects.all()})
