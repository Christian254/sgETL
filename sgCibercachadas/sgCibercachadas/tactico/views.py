from django.shortcuts import render
from django.views import generic
# Create your views here.

class ProductosMasVendidosView(generic.TemplateView):
    template_name='tactico/productos_mas_vendidos.html'

class ProductosGeneranGananciaView(generic.TemplateView):
    template_name='tactico/productos_generan_ganancias.html'
