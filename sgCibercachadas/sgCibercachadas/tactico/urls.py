from django.urls import include, path
from tactico.views import *

urlpatterns = [
    path('productosmasvendidos',ProductosMasVendidosView.as_view(),name='re_producto_mas_vendidos'),
    path('productosgeneranganancia',ProductosGeneranGananciaView.as_view(),name='re_producto_generan_ganancia'),

]