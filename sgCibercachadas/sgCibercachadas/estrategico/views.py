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
from plantilla_reporte.funciones.funciones import agrupar_cliente
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
        tipo=int(request.POST.get("tipo",None))

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        #Consulta
        detalle_venta = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto','idProducto__nombre').annotate(Sum('cantidad'),Sum('total')))
        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')
        kardex = []
        total_ganancia = 0
        for det in detalle_venta:
            prod = Kardex.objects.filter(Q(fecha__lte=fecha_fin)& Q(idProducto=det['idProducto'])).order_by('-fecha').first()
            kardex.append(prod)
            if(prod):
                det['costo'] = prod.precExistencia
            else:
                det['costo'] = 0

            det['ganancia'] = det['total__sum'] - det['cantidad__sum'] * det['costo']
            total_ganancia += det['ganancia']
        detalle_venta.sort(key=producto_ganancia.clave_orden, reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_ganancia.reporte(request,detalle_venta[:50], 'prod_ganancia',inicio,fin, total_ganancia)
        elif(tipo==3):
            return producto_gananciaxls.hoja_calculo(request,detalle_venta,'prueba',inicio,fin,total_ganancia)
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
        tipo=int(request.POST.get("tipo",None))

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        #Consulta
        detalle_cliente = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin))&Q(idVenta__idCliente__isnull=False)).values('idProducto','idVenta__idCliente__nombre').annotate(Sum('cantidad'),Sum('total')))
        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')
        total_ganancia = 0
        for det in detalle_cliente:
            prod = Kardex.objects.filter(Q(fecha__lte=fecha_fin)& Q(idProducto=det['idProducto'])).order_by('-fecha').first()
            if(prod):
                det['costo'] = prod.precExistencia
            else:
                det['costo'] = 0        
            det['ganancia'] = det['total__sum'] - det['cantidad__sum'] * det['costo']
            total_ganancia += det['ganancia']

        cliente_agrupado = agrupar_cliente(detalle_cliente,'idVenta__idCliente__nombre')
        cliente_agrupado.sort(key=producto_ganancia.clave_orden,reverse=True)
        
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_cliente.reporte(request,cliente_agrupado,'producto_cliente',inicio,fin,total_ganancia)
        elif(tipo==3):
            return producto_clientexls.hoja_calculo(request,cliente_agrupado,'producto_cliente',inicio,fin,total_ganancia)
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
        tipo=int(request.POST.get("tipo",None))
        categoria = request.POST.get('categoria',None)

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        
        if(categoria):
            detalle_vendido = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)) & Q(idProducto__idCategoria__nombre=categoria)).values('idProducto__nombre').annotate(Sum('cantidad')))
        else: 
            detalle_vendido = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto__nombre').annotate(Sum('cantidad')))
        detalle_vendido.sort(key=producto_vendido.clave_orden,reverse=True)
        
        total_cantidad = 0
        for det in detalle_vendido:
            total_cantidad += det['cantidad__sum']

        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_vendido.reporte(request,detalle_vendido,'producto_vendido',inicio,fin,total_cantidad)
        elif(tipo==3):
            return producto_vendidoxls.hoja_calculo(request,detalle_vendido,'producto_vendido',inicio,fin,total_cantidad)
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