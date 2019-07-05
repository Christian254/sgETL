"""sgCibercachadas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include,path

urlpatterns = [
    path('',include(('general.urls','general'),namespace='general')),
    path('resumen/',include(('estrategico.urls','estrategico'),namespace='estrategico')),
    path('semiresumen/',include(('tactico.urls','tactico'),namespace='tactico')),
    path('admin/',include(('administrador.urls','administrador'),namespace='administrador')),
    path('etl/',include(('etl.urls','etl'),namespace='etl'))
]
