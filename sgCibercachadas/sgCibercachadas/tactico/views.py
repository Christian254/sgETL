from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from estrategico.forms import FechasForm
from general.reporte import plantilla_reporte
from general.excel import hoja_calculo
from django.contrib import messages
from datetime import datetime
from gerencial.models import *
from django.db.models import Sum,Count,Q
from estrategico.forms import  FechasForm
from plantilla_reporte.tacticopdf import producto_vendido, producto_ganancia,producto_retorno,producto_cliente,producto_consigna,cliente_frecuente
from plantilla_reporte.tacticoxls import producto_vendidoxls, producto_gananciaxls,producto_retornoxls
from plantilla_reporte.funciones.funciones import agrupar_cliente_tactico, agrupar_cliente_frecuente
import operator

# Create your views here.

class ProductosMasVendidosView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
    template_name='tactico/productos_mas_vendidos.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_vendidos'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        categoria = Categoria.objects.all()
        return render(request, self.template_name, {'form': form,'fecha':fecha,'categoria':categoria})

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
            detalle_vendido = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)) & Q(idProducto__idCategoria__nombre=categoria)).values('idProducto__nombre','idProducto').annotate(Sum('total'),Sum('cantidad')))
        else: 
            detalle_vendido = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto__nombre','idProducto__idCategoria__nombre','idProducto').annotate(Sum('total'),Sum('cantidad')))
               
        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')
        for det in detalle_vendido:
            prod = Kardex.objects.filter(Q(fecha__lte=fecha_fin)& Q(idProducto=det['idProducto'])).order_by('-fecha').first()
            if(prod):
                det['costo'] = prod.precExistencia
                det['inventario'] = prod.cantExistencia
            else:
                det['costo'] = 0  
                det['inventario'] = 0
            ganancia = det['total__sum']-(det['cantidad__sum']*det['costo'])
            det['ganancia'] = ganancia
        
        detalle_vendido.sort(key=producto_vendido.clave_orden,reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_vendido.reporte(request,detalle_vendido[:30],'producto_vendido_tactico',inicio,fin,categoria)
        elif(tipo==3):
            return producto_vendidoxls.hoja_calculo(request,detalle_vendido[:30],'producto_vendido_tactico',inicio,fin,categoria)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ProductosGeneranGananciaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/productos_generan_ganancias.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_ganancias'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        categoria = Categoria.objects.all()
        return render(request, self.template_name, {'form': form,'fecha':fecha,'categoria':categoria})

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
            detalle_vendido = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)) & Q(idProducto__idCategoria__nombre=categoria)).values('idProducto__nombre','idProducto').annotate(Sum('total'),Sum('cantidad')))
        else: 
            detalle_vendido = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto__nombre','idProducto__idCategoria__nombre','idProducto').annotate(Sum('total'),Sum('cantidad')))
        
        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')

        for det in detalle_vendido:
            prod = Kardex.objects.filter(Q(fecha__lte=fecha_fin)& Q(idProducto=det['idProducto'])).order_by('-fecha').first()
            if(prod):
                det['costo'] = prod.precExistencia
                det['inventario'] = prod.cantExistencia
            else:
                det['costo'] = 0  
                det['inventario'] = 0
            ganancia = det['total__sum']-det['cantidad__sum']*det['costo']
            det['ganancia'] = ganancia
        
        detalle_vendido.sort(key=producto_ganancia.clave_orden,reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_ganancia.reporte(request,detalle_vendido[:30],'producto_ganancia_tactico',inicio,fin,categoria)
        elif(tipo==3):
            return producto_gananciaxls.hoja_calculo(request,detalle_vendido[:30],'producto_ganancia_tactico',inicio,fin,categoria)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class RetornoEquiposGarantiaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/retorno_equipos_garantia.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_retornos_equipos'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        categoria = Categoria.objects.all()
        return render(request, self.template_name, {'form': form,'fecha':fecha,'categoria':categoria})

    def post(self, request, *args, **kwargs):
        form = FechasForm(request.POST)
        if form.is_valid():
            print("valido")
        else:
            form.AddIsInvalid()
            return render(request, self.template_name, {'form':form})

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))
        categoria = request.POST.get('categoria',None)

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')
        if(categoria):
            retorno = list(ProductoRetorno.objects.filter(Q(fecha__range=(fecha_inicio,fecha_fin)) & Q(idProducto__idCategoria__nombre=categoria)).values('idProducto__nombre','idProveedor__razon_social').annotate(Sum('cantidad')))
        else:
            retorno = list(ProductoRetorno.objects.filter(fecha__range=(fecha_inicio,fecha_fin)).values('idProducto__nombre','idProveedor__razon_social','idProducto__idCategoria__nombre').annotate(Sum('cantidad')))

        retorno.sort(key=producto_retorno.clave_orden,reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_retorno.reporte(request,retorno[:15],'producto_retorno_tactico',inicio,fin,categoria)
        elif(tipo==3):
            return producto_retornoxls.hoja_calculo(request,retorno[:15],'producto_retorno_tactico',inicio,fin,categoria)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class RetornoEnConsignaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/productos_consigna.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_productos_consigna'

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

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')

        consigna = list(ProductoConsigna.objects.filter(fechaFin__gte=fecha_fin).values('idProducto__nombre','idProducto__idCategoria__nombre','fechaInicio','fechaFin','idCliente__nombre').annotate(Sum('cantidad')))
        consigna.sort(key=producto_consigna.clave_orden,reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return producto_consigna.reporte(request,consigna[:20],'producto_consigna',inicio,fin)
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ClientesGananciaView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/ganancia_clientes.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_ganancias_clientes'

    def get(self,request,*args,**kwargs):
        form=FechasForm()
        fecha=datetime.now()
        fecha=datetime.strftime(fecha,'%d/%m/%Y')
        venta_cliente = list(DetalleVenta.objects.filter(idVenta__idCliente__isnull=False).values('idVenta__idCliente','idVenta__idCliente__nombre','idVenta__idCliente__apellido').annotate(Count('idVenta__idCliente')))
        return render(request, self.template_name, {'form': form,'fecha':fecha,'venta_cliente':venta_cliente})

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
        cliente_id = request.POST.get("cliente",None)

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        #Consulta
        if(cliente_id):
            detalle_cliente = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin))&Q(idVenta__idCliente=cliente_id)).values('idProducto','idVenta__idCliente__nombre','idProducto__nombre','idProducto__idCategoria__nombre','idVenta__fecha_hora').annotate(Count('idProducto'),Sum('cantidad'),Sum('total')))
        else:
            detalle_cliente = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin))&Q(idVenta__idCliente__isnull=False)).values('idProducto','idVenta__idCliente__nombre','idProducto__nombre','idProducto__idCategoria__nombre').annotate(Count('idProducto'),Sum('cantidad'),Sum('total')))
        
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

        detalle_cliente.sort(key=producto_cliente.clave_orden,reverse=True)
        cliente_agrupado = agrupar_cliente_tactico(detalle_cliente,'idVenta__idCliente__nombre')
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            if(cliente_id):
                return producto_cliente.reporte(request,detalle_cliente[:15],'producto_cliente_tactico',inicio,fin,cliente_id)
            else:
                return producto_cliente.reporte(request,cliente_agrupado[:15],'producto_cliente_tactico',inicio,fin,cliente_id)
        elif(tipo==3):
            return producto_clientexls.hoja_calculo(request,cliente_agrupado[:15],'producto_cliente',inicio,fin)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)

class ClientesFrecuentesView(LoginRequiredMixin,PermissionRequiredMixin,generic.TemplateView):
    template_name='tactico/clientes_frecuentes.html'
    login_url='general:login'
    permission_required = 'gerencial.semi_clientes_frecuentes'

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

        inicio = request.POST.get('fechainicio',None)
        fin = request.POST.get('fechafin',None)
        tipo = int(request.POST.get('tipo',None))
        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d %H:%M:%S')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d %H:%M:%S')
        #Consulta
        detalle_cliente = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin))&Q(idVenta__idCliente__isnull=False)).values('idVenta__idCliente__nombre','idVenta__fecha_hora','idVenta__idCliente').annotate(Sum('cantidad'),Sum('total')))
        frecuente = agrupar_cliente_frecuente(detalle_cliente)
        frecuente.sort(key=cliente_frecuente.clave_orden,reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            return cliente_frecuente.reporte(request,frecuente[:20],'cliente_frecuente',inicio,fin)
        elif(tipo==3):
            nota = []
            return hoja_calculo(request,nota,'prueba')
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)
