from django.urls import include, path
from tactico.views import *

urlpatterns = [
    path('productosmasvendidos',ProductosMasVendidosView.as_view(),name='semire_producto_mas_vendidos'),
    path('productosgeneranganancia',ProductosGeneranGananciaView.as_view(),name='semire_producto_generan_ganancia'),
    path('retornoequiposgarantia',RetornoEquiposGarantiaView.as_view(),name='semire_retorno_equipos_garantia'),
    path('productosenconsigna',RetornoEnConsignaView.as_view(),name='semire_productos_consigna'),
    path('clientesganancia',ClientesGananciaView.as_view(),name='semire_clientes_ganancia'),
    path('clientesfrecuentes',ClientesFrecuentesView.as_view(),name='semire_clientes_frecuentes'),
]