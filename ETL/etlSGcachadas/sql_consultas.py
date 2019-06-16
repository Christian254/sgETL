from consultas_carga import lista_carga,lista_tablas_gerencial as nombre_tablas
from consultas_extraccion import lista_extraccion

class ConsultaSQL:
    def __init__(self, consulta_extraccion, consulta_carga,nombre_tabla_gerencial):
        self.consulta_extraccion = consulta_extraccion
        self.consulta_carga = consulta_carga
        self.consulta_contador="select count(*) from {}".format(nombre_tabla_gerencial)
        self.nombre_tabla=nombre_tabla_gerencial
    
        
cantidad=len(lista_carga)
postgresqlConsultas= []


for i in range(cantidad):
    consulta= ConsultaSQL(lista_extraccion[i],lista_carga[i],nombre_tablas[i])
    postgresqlConsultas.append(consulta)

