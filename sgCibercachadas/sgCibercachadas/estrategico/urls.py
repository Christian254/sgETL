from django.urls import include, path
from estrategico.views import ProductosVendidosView

urlpatterns = [
    path('productosmasvendidos',ProductosVendidosView.as_view(),name='re_producto_vendido'),
  
]