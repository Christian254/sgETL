from django.urls import include, path
from estrategico.views import *

urlpatterns = [
    path('productosgeneranganancias',ProductosGeneranGananciasView.as_view(),name='re_producto_generan_ganancias'),
    path('productospotenciales',ProductosPotencialesView.as_view(),name='re_producto_potenciales'),
    path('productosgananciasclientes',ProductosGananciasClientesView.as_view(),name='re_producto_ganancias_clientes'),
    path('productosmasvendidos',ProductosVendidosView.as_view(),name='re_producto_vendido'),
    path('productostardanzaproductos',ProductosTardanzaProductosView.as_view(),name='re_producto_tardanza_productos'),
]