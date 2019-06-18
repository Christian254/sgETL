import itertools
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def plantilla_reporte(request,datos,nombre):
    ##Esta data nosotros la generaremos con django serán las consultas
    # esta siendo generado aleatoriamente todo lo saqué de un ejemplo de inter y lo fui modificando 
    data = [("NOMBRE", "Total", "Cantidad", "NOTA 3", "PROM.")] # Este es el encabezado
    for i in datos:        
        avg = 0
        data.append((i['idProducto__nombre'], i['total__sum'],i['idProducto__count'],0, 0))
    
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
    #c.drawImage("logo.png", x_offset, h - 75, width=50, height=50) #Aquí vamos a buscar la ubicación del logo
    #titulos
    titulo = "CompuOfertas"
    texto =  c.beginText((w-len(titulo))/2-50, h - 50)
    texto.setFont("Times-Roman", 14)
    texto.textLine(titulo)
    c.drawText(texto)
    subtitulo = "Productos mas vendidos"
    texto =  c.beginText((w-len(subtitulo))/2-50, h - 65)
    texto.textLine(subtitulo)    
    c.drawText(texto)
    #Aqui le vamos a mandar los periodos por parametros y concatenarlos
    periodo = "Periodo inicio: dd/mm/aa Periodo Fin: dd/mm/aa"
    texto =  c.beginText((w-len(periodo))/2-50, h - 80)
    texto.textLine(periodo)
    c.drawText(texto)

    xlist = [x + x_offset for x in [50, 140, 230, 320, 410, 500]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    #Aquí es donde inserta la data
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
    c.save()
    pdf= buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response