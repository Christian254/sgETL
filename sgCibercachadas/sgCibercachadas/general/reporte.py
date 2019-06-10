import itertools
from random import randint
from statistics import mean

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def plantilla_reporte(data,nombre):
    c = canvas.Canvas(f"{nombre}.pdf", pagesize=A4)
    w, h = A4
    max_rows_per_page = 25 #Aquí ponemos cuantos registros queremos por páginas
    # Margin.
    x_offset = 50
    y_offset = 150
    # Space between rows.
    padding = 15
    #Imagen
    c.drawImage("logo.png", x_offset, h - 75, width=50, height=50) #Aquí vamos a buscar la ubicación del logo
    #titulos
    texto =  c.beginText(w/2, h - 50)
    texto.setFont("Times-Roman", 14)
    texto.textLine("CompuOfertas")
    c.drawText(texto)
    texto =  c.beginText((w/2 - 15), h - 65)
    texto.textLine("Productos mas vendidos")    
    c.drawText(texto)
    #Aqui le vamos a mandar los periodos por parametros y concatenarlos
    texto =  c.beginText((w/2 - 60), h - 80)
    texto.textLine("Periodo inicio: dd/mm/aa Periodo Fin: dd/mm/aa")
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


##Esta data nosotros la generaremos con django serán las consultas
# esta siendo generado aleatoriamente todo lo saqué de un ejemplo de inter y lo fui modificando 
data = [("NOMBRE", "NOTA 1", "NOTA 2", "NOTA 3", "PROM.")] # Este es el encabezado
for i in range(1, 30):
    exams = [randint(0, 10) for _ in range(3)]
    avg = round(mean(exams), 2)
    data.append((f"Alumno {i}", *exams, avg))
plantilla_reporte(data,"rep") #Aqui es donde se invoca la funcion se le manda la data y el nombre del reporte