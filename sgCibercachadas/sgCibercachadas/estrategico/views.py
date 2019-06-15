from django.shortcuts import render,redirect
from django.views import generic
from general.reporte import plantilla_reporte
from django.contrib import messages
# Create your views here.

class ProductosGeneranGananciasView(generic.TemplateView):
    template_name='estrategico/productos_mas_ganancias.html'
    def post(self, request, *args, **kwargs):
        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        if(inicio==None or fin==None):
            messages.add_message(request, messages.WARNING, 'Las fechas son obligatorias')
            return redirect(self.request.path_info)
        else:
            nota = []
            return plantilla_reporte(request,nota,'prueba')

class ProductosPotencialesView(generic.TemplateView):
    template_name='estrategico/productos_potenciales.html'

class ProductosGananciasClientesView(generic.TemplateView):
    template_name='estrategico/productos_ganancias_clientes.html'

class ProductosVendidosView(generic.TemplateView):
    template_name='estrategico/productos_vendidos.html'

class ProductosTardanzaProductosView(generic.TemplateView):
    template_name='estrategico/productos_tardanzas_movimiento.html'