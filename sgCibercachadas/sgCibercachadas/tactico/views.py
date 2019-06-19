from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from estrategico.forms import FechasForm
from general.reporte import plantilla_reporte
from general.excel import hoja_calculo
from django.contrib import messages
from datetime import datetime
# Create your views here.

class ProductosMasVendidosView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
    template_name='tactico/productos_mas_vendidos.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_vendidos'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ProductosGeneranGananciaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/productos_generan_ganancias.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_ganancias'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))
        
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class RetornoEquiposGarantiaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/retorno_equipos_garantia.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_retornos_equipos'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class RetornoEnConsignaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/productos_consigna.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_consigna'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ClientesGananciaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/ganancia_clientes.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_ganancias_clientes'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ClientesFrecuentesView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/clientes_frecuentes.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_clientes_frecuentes'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)
