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
from plantilla_reporte.tacticoxls import producto_vendidoxls, producto_gananciaxls,producto_retornoxls,producto_consignaxls,producto_clientexls,cliente_frecuentexls
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
            if(detalle_vendido):
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos mas vendidos (pdf)")

                return producto_vendido.reporte(request,detalle_vendido[:30],'producto_vendido_tactico',inicio,fin,categoria)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos en el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(detalle_vendido):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos mas vendidos (xls)")

                return producto_vendidoxls.hoja_calculo(request,detalle_vendido[:30],'producto_vendido_tactico',inicio,fin,categoria)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos en el periodo seleccionado')
                return redirect(self.request.path_info)
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
            if(detalle_vendido):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos ganancia (pdf)")

                return producto_ganancia.reporte(request,detalle_vendido[:30],'producto_ganancia_tactico',inicio,fin,categoria)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante este periodo')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(detalle_vendido):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos ganancia (xls)")

                return producto_gananciaxls.hoja_calculo(request,detalle_vendido[:30],'producto_ganancia_tactico',inicio,fin,categoria)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante este periodo')
                return redirect(self.request.path_info)
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
            if(retorno):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos retorno (pdf)")

                return producto_retorno.reporte(request,retorno[:15],'producto_retorno_tactico',inicio,fin,categoria)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos en el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(retorno):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos retorno (xls)")

                return producto_retornoxls.hoja_calculo(request,retorno[:15],'producto_retorno_tactico',inicio,fin,categoria)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos en el periodo seleccionado')
                return redirect(self.request.path_info)
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
            if(consigna):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos en consigna (pdf)")

                return producto_consigna.reporte(request,consigna[:20],'producto_consigna',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos en el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(consigna):

                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: productos en consigna (xls)")

                return producto_consignaxls.hoja_calculo(request,consigna[:20],'producto_consigna',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos en el periodo seleccionado')
                return redirect(self.request.path_info)
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
        cliente_agrupado = []

        if(detalle_cliente):
            cliente_agrupado = agrupar_cliente_tactico(detalle_cliente,'idVenta__idCliente__nombre')
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            if(cliente_id):
                if(detalle_cliente):
                    
                    #bitacora 
                    Bitacora.objects.create(
                    usuario=request.user.first_name+" "+request.user.last_name,
                    accion="Generado reporte tactico: clientes ganancia (pdf)")

                    return producto_cliente.reporte(request,detalle_cliente[:15],'producto_cliente_tactico',inicio,fin,cliente_id)
                else:
                    messages.add_message(request, messages.WARNING, 'El cliente seleccionado no realizó compras durante el periodo consultado')
                    return redirect(self.request.path_info)
            else:
                if(cliente_agrupado):

                    #bitacora 
                    Bitacora.objects.create(
                    usuario=request.user.first_name+" "+request.user.last_name,
                    accion="Generado reporte tactico: clientes ganancia (pdf)")                    

                    return producto_cliente.reporte(request,cliente_agrupado[:15],'producto_cliente_tactico',inicio,fin,cliente_id)
                else:
                    messages.add_message(request, messages.WARNING, 'No existen compras durante este periodo')
                    return redirect(self.request.path_info) 
        elif(tipo==3):
            if(cliente_id):
                if(detalle_cliente):
                    
                    #bitacora 
                    Bitacora.objects.create(
                    usuario=request.user.first_name+" "+request.user.last_name,
                    accion="Generado reporte tactico: clientes ganancia (xls)")

                    return producto_clientexls.hoja_calculo(request,detalle_cliente[:15],'producto_cliente',inicio,fin,cliente_id)
                else:
                    messages.add_message(request, messages.WARNING, 'El cliente seleccionado no realizó compras durante el periodo consultado')
                    return redirect(self.request.path_info)
            else:
                if(cliente_agrupado):
                    #bitacora 
                    Bitacora.objects.create(
                    usuario=request.user.first_name+" "+request.user.last_name,
                    accion="Generado reporte tactico: clientes ganancia (xls)")

                    return producto_clientexls.hoja_calculo(request,cliente_agrupado[:15],'producto_cliente',inicio,fin,cliente_id)
                else:
                    messages.add_message(request, messages.WARNING, 'No existen compras durante este periodo')
                    return redirect(self.request.path_info)
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
        frecuente = []

        if(detalle_cliente):
            frecuente = agrupar_cliente_frecuente(detalle_cliente)
            frecuente.sort(key=cliente_frecuente.clave_orden,reverse=True)
        if(tipo==1):
            messages.add_message(request, messages.WARNING, 'AUN ESTA EN DESARROLLO')
            return redirect(self.request.path_info)
        elif(tipo==2):
            if(frecuente):
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: clientes frecuentes (pdf)")

                return cliente_frecuente.reporte(request,frecuente[:20],'cliente_frecuente',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante este periodo')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(frecuente):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte tactico: clientes frecuentes (xls)")
                
                return cliente_frecuentexls.hoja_calculo(request,frecuente[:20],'cliente_frecuente',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante este periodo')
                return redirect(self.request.path_info)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)
