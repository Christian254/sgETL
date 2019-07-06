from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic
from plantilla_reporte.estretegicopdf import producto_ganancia,producto_cliente,producto_vendido,producto_potencial,producto_tardanza
from plantilla_reporte.estrategicoxls import producto_gananciaxls,producto_clientexls,producto_vendidoxls, producto_tardanzaxls, producto_potencialxls
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timezone
from gerencial.models import *
from django.db.models import Sum,Count,Q
from estrategico.forms import  FechasForm
from plantilla_reporte.funciones.funciones import agrupar_cliente,agrupar_producto_potencial
import operator
from django.http import JsonResponse
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
            return JsonResponse(detalle_venta[:10],safe=False)
        elif(tipo==2):
            if(detalle_venta):
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos que generan mas ganancia (pdf)",
                )
                return producto_ganancia.reporte(request,detalle_venta[:10], 'prod_ganancia',inicio,fin, total_ganancia)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(detalle_venta):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos que generan mas ganancia (xls)",
                )

                return producto_gananciaxls.hoja_calculo(request,detalle_venta[:10],'prod_ganancia',inicio,fin,total_ganancia)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
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
        tipo=int(request.POST.get("tipo",None))

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')

        potencial = list(ProductoPotencial.objects.filter(fecha__range=(fecha_inicio,fecha_fin)).values('nombre','cantidad','idCliente__nombre'))
        if(potencial):
            potencial=agrupar_producto_potencial(potencial)
        potencial.sort(key=producto_potencial.clave_orden,reverse=True)
        if(tipo==1):
            return JsonResponse(potencial[:5],safe=False)
        elif(tipo==2):

            if(potencial):

                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos potenciales (pdf)",
                )
                return producto_potencial.reporte(request,potencial[:5],'producto_potencial',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(potencial):
                                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos potenciales (xls)",
                )

                return producto_potencialxls.hoja_calculo(request,potencial[:5],'producto_potencial',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
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
        if(detalle_cliente):
            detalle_cliente = agrupar_cliente(detalle_cliente,'idVenta__idCliente__nombre')
        detalle_cliente.sort(key=producto_ganancia.clave_orden,reverse=True)
        
        if(tipo==1):
            return JsonResponse(detalle_cliente[:10],safe=False)
        elif(tipo==2):

            if(detalle_cliente):
                            #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos Mayor Ganancia (pdf)",
                )

                return producto_cliente.reporte(request,detalle_cliente[:10],'producto_cliente',inicio,fin,total_ganancia)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(detalle_cliente):
                                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos Mayor Ganancia (xls)",
                )
                return producto_clientexls.hoja_calculo(request,detalle_cliente[:10],'producto_cliente',inicio,fin,total_ganancia)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
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
            detalle_vendido = list(DetalleVenta.objects.filter(Q(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)) & Q(idProducto__idCategoria__nombre=categoria)).values('idProducto__nombre').annotate(Sum('cantidad')))
        else: 
            detalle_vendido = list(DetalleVenta.objects.filter(idVenta__fecha_hora__range=(fecha_inicio,fecha_fin)).values('idProducto__nombre').annotate(Sum('cantidad')))
        detalle_vendido.sort(key=producto_vendido.clave_orden,reverse=True)
        
        total_cantidad = 0
        for det in detalle_vendido:
            total_cantidad += det['cantidad__sum']

        if(tipo==1):
            return JsonResponse(detalle_vendido[:10],safe=False)
        elif(tipo==2):

            if(detalle_vendido):
                
                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos Mas Vendidos (pdf)")
                
                return producto_vendido.reporte(request,detalle_vendido[:10],'producto_vendido',inicio,fin,total_cantidad)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(detalle_vendido):
                                #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Productos Mas Vendidos (xls)")

                return producto_vendidoxls.hoja_calculo(request,detalle_vendido[:10],'producto_vendido',inicio,fin,total_cantidad)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
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
        tipo=int(request.POST.get("tipo",None))

        fecha_inicio = datetime.strptime(inicio,'%d/%m/%Y')
        fecha_inicio = datetime.strftime(fecha_inicio,'%Y-%m-%d')

        fecha_fin = datetime.strptime(fin,'%d/%m/%Y')
        fecha_fin = datetime.strftime(fecha_fin,'%Y-%m-%d')
        
        prod_kardex = Kardex.objects.filter(Q(fecha__gte=fecha_inicio)and Q(fecha__lte=fecha_fin)).distinct('idProducto')
        
        idProducto = []
        
        producto_existencia = []
        #Todos los productos ordenado 
        for p in prod_kardex:
            prod_ex = dict(Kardex.objects.filter(idProducto=p.idProducto).values('idProducto','cantExistencia','idProducto__nombre').order_by('-id').first())
            producto_existencia.append(prod_ex)
        
        
        prod_final = []
        for p in producto_existencia:
            pfin = Kardex.objects.filter(Q(idProducto = p['idProducto']) & Q(fecha = fecha_inicio)).values('idProducto','cantExistencia').first()
            if(pfin):
                prod_final.append(dict(pfin))
            else:
                pfin = Kardex.objects.filter(Q(idProducto = p['idProducto']) & Q(fecha__lte = fecha_inicio)).values('idProducto','cantExistencia').first()
                if(pfin):
                    prod_final.append(dict(pfin))
                else:
                    k = {}
                    k['fecha'] = fecha_inicio
                    k['cantExistencia'] = 0
                    k['idProducto'] = p['idProducto']
                    prod_final.append(k)

        fin_tardanza = []
        
        for i in prod_final:
            consigna = list(ProductoConsigna.objects.filter(Q(fechaFin__gte=fecha_fin)&Q(idProducto=i['idProducto'])).values('idProducto__nombre').annotate(Sum('cantidad')))
            for j in producto_existencia:
                if i['idProducto'] == j['idProducto']:
                    i['disponible'] = j['cantExistencia']
                    i['nombre'] = j['idProducto__nombre']
                    if(consigna): 
                        i['consigna'] = consigna[0]['cantidad__sum']
                    else:
                        i['consigna'] = 0
                    fin_tardanza.append(i)
        
        fin_tardanza.sort(key=producto_tardanza.clave_orden,reverse=True)
        if(tipo==1):
            return JsonResponse(fin_tardanza[:10],safe=False)
        elif(tipo==2):

            if(fin_tardanza):
                            #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Tardanza de productos (pdf)")

                return producto_tardanza.reporte(request,fin_tardanza[:10],'producto_tardanza',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
        elif(tipo==3):
            if(fin_tardanza):
                                        #bitacora 
                Bitacora.objects.create(
                usuario=request.user.first_name+" "+request.user.last_name,
                accion="Generado reporte estrategico: Tardanza de productos (xls)")

                return producto_tardanzaxls.hoja_calculo(request,fin_tardanza[:10],'producto_tardanza',inicio,fin)
            else:
                messages.add_message(request, messages.WARNING, 'No se encontraron datos durante el periodo seleccionado')
                return redirect(self.request.path_info)
        else:
            messages.add_message(request, messages.WARNING, 'Esta opción no es valida')
            return redirect(self.request.path_info)