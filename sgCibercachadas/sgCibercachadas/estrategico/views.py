from django.shortcuts import render
from django.views import generic
# Create your views here.
class ProductosVendidosView(generic.TemplateView):
    template_name='estrategico/productos_vendidos.html'
