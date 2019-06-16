from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from general.reporte import plantilla_reporte
from general.excel import hoja_calculo
from django.contrib import messages
from datetime import datetime
# Create your views here.

class ProductosMasVendidosView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
    template_name='tactico/productos_mas_vendidos.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_vendidos'

    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        validacionfecha(inicio,fin)
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

class ProductosGeneranGananciaView(generic.TemplateView):
    template_name='tactico/productos_generan_ganancias.html'
    def post(self, request, *args, **kwargs):
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

class RetornoEquiposGarantiaView(generic.TemplateView):
    template_name='tactico/retorno_equipos_garantia.html'
    def post(self, request, *args, **kwargs):
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

class RetornoEnConsignaView(generic.TemplateView):
    template_name='tactico/productos_consigna.html'
    def post(self, request, *args, **kwargs):
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

class ClientesGananciaView(generic.TemplateView):
    template_name='tactico/ganancia_clientes.html'
    def post(self, request, *args, **kwargs):
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

class ClientesFrecuentesView(generic.TemplateView):
    template_name='tactico/clientes_frecuentes.html'
    def post(self, request, *args, **kwargs):
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

def validacionfecha(inicio,fin):
    print ("hol")