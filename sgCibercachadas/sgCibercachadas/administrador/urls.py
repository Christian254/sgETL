from django.urls import include, path
from administrador.views import *

urlpatterns = [
    path('adminusuarios',AdminUsuariosView.as_view(),name='admin_gestion_usuarios'),
  
]