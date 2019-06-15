from django.shortcuts import render,redirect
from django.views import generic
from general.reporte import plantilla_reporte
from django.contrib import messages
from datetime import datetime
# Create your views here.

class ProductosMasVendidosView(generic.TemplateView):
    template_name='tactico/productos_mas_vendidos.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')

class ProductosGeneranGananciaView(generic.TemplateView):
    template_name='tactico/productos_generan_ganancias.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')

class RetornoEquiposGarantiaView(generic.TemplateView):
    template_name='tactico/retorno_equipos_garantia.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')

class RetornoEnConsignaView(generic.TemplateView):
    template_name='tactico/productos_consigna.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')

class ClientesGananciaView(generic.TemplateView):
    template_name='tactico/ganancia_clientes.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')

class ClientesFrecuentesView(generic.TemplateView):
    template_name='tactico/clientes_frecuentes.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fechas de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')