from django.shortcuts import render
from django.views import generic
# Create your views here.

class ProductosMasVendidosView(generic.TemplateView):
    template_name='tactico/productos_mas_vendidos.html'

class ProductosGeneranGananciaView(generic.TemplateView):
    template_name='tactico/productos_generan_ganancias.html'

class RetornoEquiposGarantiaView(generic.TemplateView):
    template_name='tactico/retorno_equipos_garantia.html'

class RetornoEnConsignaView(generic.TemplateView):
    template_name='tactico/productos_consigna.html'

class ClientesGananciaView(generic.TemplateView):
    template_name='tactico/ganancia_clientes.html'

class ClientesFrecuentesView(generic.TemplateView):
    template_name='tactico/clientes_frecuentes.html'