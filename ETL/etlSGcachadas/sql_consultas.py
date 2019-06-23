#!/usr/bin/python
from consultas_carga import lista_carga,lista_tablas_gerencial as nombre_tablas
from consultas_extraccion import lista_extraccion, lista_tablas_transaccional as nombre_tabla_trans

class ConsultaSQL:
    def __init__(self, consulta_extraccion, consulta_carga,nombre_tabla_gerencial,nombre_tabla_transaccional):
        self.consulta_extraccion = consulta_extraccion
        self.consulta_carga = consulta_carga
        self.consulta_contador_gerencial="select count(*) from {}".format(nombre_tabla_gerencial)
        self.consulta_contador_transaccional="select count(*) from {}".format(nombre_tabla_transaccional)
        self.nombre_tabla_gerencial=nombre_tabla_gerencial
        self.nombre_tabla_trans=nombre_tabla_transaccional
    
        
cantidad=len(lista_carga)
postgresqlConsultas= []


for i in range(cantidad):
    consulta= ConsultaSQL(lista_extraccion[i],lista_carga[i],nombre_tablas[i],nombre_tabla_trans[i])
    postgresqlConsultas.append(consulta)

