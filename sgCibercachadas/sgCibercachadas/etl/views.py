from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timezone
from gerencial.models import *
from subprocess import Popen, PIPE

class CargaDatos(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='etl/index.html'
    login_url='general:login'
    permission_required = 'gerencial.etl'

    def get(self,request,*args,**kwargs):
        
        return render(request, self.template_name)

class EtlBD(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    login_url='general:login'
    permission_required = 'gerencial.etl'

    def get(self,request,*args,**kwargs):
        return redirect('/etl')

    def post(self,request,*args,**kwargs):
        script_dir="../../ETL/etlSGcachadas"
        p = Popen(["python", "main.py"], cwd=script_dir, stdout=PIPE, stderr=PIPE)
        print(p.communicate())
        messages.add_message(request, messages.SUCCESS, 'ETL ejecutado con exito')
        return redirect('/etl')

class CargaRetorno(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    login_url='general:login'
    permission_required = 'gerencial.etl'

    def get(self,request,*args,**kwargs):
        return redirect('/etl')
    
    def post(self,request,*args,**kwargs):
        return redirect('/etl')


