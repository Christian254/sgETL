from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timezone
from etl.forms import RetornoForm, PotencialForm,ConsignaForm
from gerencial.models import *
from subprocess import Popen, PIPE
import openpyxl

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
        form= RetornoForm(request.POST,request.FILES)
        if form.is_valid():
            archivo=request.FILES.get("file_retorno")
            archivo= openpyxl.load_workbook(archivo)
            hoja1=archivo.get_sheet_by_name('Hoja1')
            
            for row in hoja1.rows:
                for cell in row:
                        print (cell.value)       

            messages.add_message(request, messages.SUCCESS, 'Carga de producto retorno realizada con exito')
            return redirect('etl:carga_menu')
        else:
            return render(request,'etl/index.html',{'form':form})
            

class CargaPotencial(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    login_url='general:login'
    permission_required = 'gerencial.etl'

    def get(self,request,*args,**kwargs):
        return redirect('/etl')
    
    def post(self,request,*args,**kwargs):
        form= PotencialForm(request.POST,request.FILES)
        if form.is_valid():

            messages.add_message(request, messages.SUCCESS, 'Carga de producto potenciales realizada con exito')
            return redirect('etl:carga_menu')
        else:
            return render(request,'etl/index.html',{'form':form})


class CargaConsigna(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    login_url='general:login'
    permission_required = 'gerencial.etl'

    def get(self,request,*args,**kwargs):
        return redirect('/etl')
    
    def post(self,request,*args,**kwargs):
        form= ConsignaForm(request.POST,request.FILES)
        if form.is_valid():

            messages.add_message(request, messages.SUCCESS, 'Carga de productos en consigna realizada con exito')
            return redirect('etl:carga_menu')
        else:
            return render(request,'etl/index.html',{'form':form})


