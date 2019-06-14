from django.shortcuts import render
from django.views import generic
# Create your views here.

class ProductosGeneranGananciasView(generic.TemplateView):
    template_name='estrategico/productos_mas_ganancias.html'

class ProductosPotencialesView(generic.TemplateView):
    template_name='estrategico/productos_potenciales.html'

class ProductosGananciasClientesView(generic.TemplateView):
    template_name='estrategico/productos_ganancias_clientes.html'

class ProductosVendidosView(generic.TemplateView):
    template_name='estrategico/productos_vendidos.html'

class ProductosTardanzaProductosView(generic.TemplateView):
    template_name='estrategico/productos_tardanzas_movimiento.html'