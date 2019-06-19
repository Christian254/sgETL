from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from plantilla_reporte.estretegicopdf import producto_ganancia,producto_cliente,producto_vendido
from plantilla_reporte.estrategicoxls import producto_gananciaxls,producto_clientexls,producto_vendidoxls
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timezone
from gerencial.models import *
from django.db.models import Sum,Count,Q
from estrategico.forms import  FechasForm
import operator
# Create your views here.
#LOS CALCULOS DE LOS PORCENTAJES NO SE HAN REALIZADO
class ProductosGeneranGananciasView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='estrategico/productos_mas_ganancias.html'
    login_url='general:login'
    permission_required = 'gerencial.resumen_productos_ganancias'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio=request.POST.get("fechainicio",None)
        fin=request.POST.get("fechafin",None)
        tipo=request.POST.get("tipo",None)

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        #Consulta
        detalle_venta = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto','idProducto__nombre','idProducto__idInventario__precio_promedio_compra').annotate(Sum('total'),Count('idProducto')))
        #Calculando Ganancia por cada uno
        for det in detalle_venta:
            ganancia = det['total__sum']-(det['idProducto__count']*det['idProducto__idInventario__precio_promedio_compra'])
            det['ganancia']=ganancia
        #Ordenando
        detalle_venta.sort(key=producto_ganancia.clave_orden,reverse=True)

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_ganancia.reporte(request,detalle_venta, 'prod_ganancia',inicio,fin)
        elif(tipo==3):
            return producto_gananciaxls.hoja_calculo(request,detalle_venta,'prueba',inicio,fin)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)
        

class ProductosPotencialesView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='estrategico/productos_potenciales.html'
    login_url='general:login'
    permission_required = 'gerencial.resumen_productos_potenciales'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio=request.POST.get("fechainicio",None)
        fin=request.POST.get("fechafin",None)
        tipo=request.POST.get("tipo",None)

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ProductosGananciasClientesView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='estrategico/productos_ganancias_clientes.html'
    login_url='general:login'
    permission_required = 'gerencial.resumen_ganancias_clientes'
    
    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})
        
        inicio=request.POST.get("fechainicio",None)
        fin=request.POST.get("fechafin",None)
        tipo=request.POST.get("tipo",None)

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        #Consulta
        detalle_cliente = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto__idInventario__precio_promedio_compra','idVenta__idCliente__nombre').annotate(Count('idProducto'),Sum('total')))
        for det in detalle_cliente:
            ganancia = det['total__sum']-(det['idProducto__count']*det['idProducto__idInventario__precio_promedio_compra'])
            det['ganancia']=ganancia
        detalle_cliente.sort(key=producto_ganancia.clave_orden,reverse=True)
        ##FALTA AGRUPAR A LOS CLIENTES Y SUMAR LA GANANCIA
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_cliente.reporte(request,detalle_cliente,'producto_cliente',inicio,fin)
        elif(tipo==3):
            return producto_clientexls.hoja_calculo(request,detalle_cliente,'producto_cliente',inicio,fin)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ProductosVendidosView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='estrategico/productos_vendidos.html'
    login_url='general:login'
    permission_required = 'gerencial.resumen_productos_vendidos'
    
    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio=request.POST.get("fechainicio",None)
        fin=request.POST.get("fechafin",None)
        tipo=request.POST.get("tipo",None)
        categoria = request.POST.get('categoria',None)

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        
        if(categoria):
            detalle_vendido = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)) & Q(idProducto__idCategoria__nombre=categoria)).values('idProducto__nombre').annotate(Count('idProducto'),Sum('total')))
        else: 
            detalle_vendido = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto__nombre').annotate(Count('idProducto'),Sum('total')))
        detalle_vendido.sort(key=producto_vendido.clave_orden,reverse=True)

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_vendido.reporte(request,detalle_vendido,'producto_vendido',inicio,fin)
        elif(tipo==3):
            return producto_vendidoxls.hoja_calculo(request,detalle_vendido,'producto_vendido',inicio,fin)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ProductosTardanzaProductosView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='estrategico/productos_tardanzas_movimiento.html'
    login_url='general:login'
    permission_required = 'gerencial.resumen_tardanzas_productos'

    
    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        return render(request, self.template_name, {'form': form,'fecha':fecha})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio=request.POST.get("fechainicio",None)
        fin=request.POST.get("fechafin",None)
        tipo=request.POST.get("tipo",None)
        
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            nota =[]
            return plantilla_reporte(request,nota,'prueba')
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)