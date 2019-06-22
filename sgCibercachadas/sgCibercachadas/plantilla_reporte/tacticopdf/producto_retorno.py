import io
from django.conf import settings
from plantilla_reporte.funciones.funciones import insert_data_pdf,texto_pdf
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

registerFont(TTFont('Arial', 'Arial.ttf'))

def reporte(request,datos,nombre,inicio,fin,categoria):
    ##Esta data nosotros la generaremos con django serán las consultas
    # esta siendo generado aleatoriamente todo lo saqué de un ejemplo de inter y lo fui modificando 
   
    response =HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(nombre)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer,pagesize=A4)
    w, h = A4
    max_rows_per_page = 25 #Aquí ponemos cuantos registros queremos por páginas
    # Margin.
    x_offset = 50
    y_offset = 150
    # Space between rows.
    padding = 15
    #Imagen
    c.drawImage(settings.MEDIA_ROOT+'/logo/logo.png', x_offset, h - 75, width=50, height=50) #Aquí vamos a buscar la ubicación del logo

    #titulos
    periodo = "Periodo inicio: {} Periodo Fin: {}".format(inicio,fin)
    texto_pdf(c,h,w,"CiberCachada",14,65)
    texto_pdf(c,h,w,"Retornos de equipo con garantía",12,80)
    texto_pdf(c,h,w,periodo,12,95)
    if(categoria):
        data = [("Producto Retornado", "Proveedor","Cantidad")] # Este es el encabezado
        for i in datos:
            data.append((i['idProducto__nombre'],'{}'.format(i['idProveedor__razon_social']), '$ {}'.format(i['cantidad__sum'])))
        xlist = [x + x_offset for x in [50, 275,440,500]]
        ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]

        
    else:
        data = [("Producto", "Categoria","Proveedor", "Cantidad")] # Este es el encabezado
        for i in datos:
            data.append((i['idProducto__nombre'],i['idProducto__idCategoria__nombre'],i['idProveedor__razon_social'],'{}'.format(i['cantidad__sum'])))
        xlist = [x + x_offset for x in [50, 200, 330,440,500]]
        ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    #Aquí es donde inserta la data
    insert_data_pdf(data, max_rows_per_page,xlist,ylist,c,padding)
    
    c.save()
    pdf= buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def clave_orden(e):
    return e['cantidad__sum']