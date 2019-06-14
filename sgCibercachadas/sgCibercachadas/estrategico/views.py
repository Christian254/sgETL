from django.shortcuts import render
from django.views import generic
from general.reporte import plantilla_reporte
# Create your views here.

def ProductosGeneranGananciasView(request):
    if request.method == 'POST':
        nota = []
        return plantilla_reporte(request, nota, 'prueba')
    return render(request, 'estrategico/productos_mas_ganancias.html',{})

class ProductosPotencialesView(generic.TemplateView):
    template_name='estrategico/productos_potenciales.html'

class ProductosGananciasClientesView(generic.TemplateView):
    template_name='estrategico/productos_ganancias_clientes.html'

class ProductosVendidosView(generic.TemplateView):
    template_name='estrategico/productos_vendidos.html'

class ProductosTardanzaProductosView(generic.TemplateView):
    template_name='estrategico/productos_tardanzas_movimiento.html'