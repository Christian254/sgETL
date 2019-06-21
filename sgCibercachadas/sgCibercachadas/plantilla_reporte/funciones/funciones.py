import itertools
from itertools import groupby
from operator import itemgetter
from reportlab.pdfbase.pdfmetrics import stringWidth

#Funciones para PDF
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)

def insert_data_pdf(data, max_rows_per_page,xlist,ylist,c,padding):
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()

def texto_pdf(c,h, w, cadena,size,y):    
    titulo = cadena
    texto =  c.beginText((w-stringWidth(titulo,'Arial',size))/2, h - y)
    texto.textLine(titulo)
    c.drawText(texto)

def agrupar(lista,llave,campo_sumar):
        agrupacion = [llave]
        key = itemgetter(*agrupacion)
        lista.sort(key=key)
        lista = [{**dict(zip(agrupacion,k)),campo_sumar:sum(map(itemgetter(campo_sumar),g))}
        for k,g in groupby(lista,key=key)]
        return lista