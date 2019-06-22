from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth.models import User

class AdminUsuariosView(generic.ListView):
    model = User
    template_name='administrador/admin_usuarios.html'
    context_object_name = "obj"
    paginate_by = 10

