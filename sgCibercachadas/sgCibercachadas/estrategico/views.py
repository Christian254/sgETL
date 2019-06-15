from django.shortcuts import render,redirect
from django.views import generic
from general.reporte import plantilla_reporte
from django.contrib import messages
from datetime import datetime
# Create your views here.

class ProductosGeneranGananciasView(generic.TemplateView):
    template_name='estrategico/productos_mas_ganancias.html'
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

class ProductosPotencialesView(generic.TemplateView):
    template_name='estrategico/productos_potenciales.html'
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

class ProductosGananciasClientesView(generic.TemplateView):
    template_name='estrategico/productos_ganancias_clientes.html'
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

class ProductosVendidosView(generic.TemplateView):
    template_name='estrategico/productos_vendidos.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(not(inicio) or not(fin)):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)

        elif(str(datetime.strptime(inicio,'%d/%m/%Y')) > str(datetime.strptime(fin,'%d/%m/%Y'))):
            messages.add_message(request, messages.WARNING, 'Las fecha de inicio debe ser menor que la fecha de fin')
            return redirect(self.request.path_info)
        else:
            nota =[]
            return plantilla_reporte(request,nota,'prueba')

class ProductosTardanzaProductosView(generic.TemplateView):
    template_name='estrategico/productos_tardanzas_movimiento.html'
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