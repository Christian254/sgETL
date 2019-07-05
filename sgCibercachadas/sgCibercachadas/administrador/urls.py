from django.urls import include, path
from administrador.views import AdminUsuariosView,CrearUsuariosView,InhabilitarUsuarios,EditarUsuariosView

urlpatterns = [
    path('adminusuarios',AdminUsuariosView.as_view(),name='admin_gestion_usuarios'),
    path('crearusuarios',CrearUsuariosView.as_view(),name='admin_crear_usuarios'),
    path('editarusuarios/<int:id>',EditarUsuariosView.as_view(),name='admin_editar_usuarios'),
    path('inhabilitar/<int:id>',InhabilitarUsuarios.as_view(),name="admin_inhabilitar_usuarios")
]