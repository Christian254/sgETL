from consultas_carga import lista_carga
from consultas_extraccion import lista_extraccion

class ConsultaSQL:
    def __init__(self, consulta_extraccion, consulta_carga):
        self.consulta_extraccion = consulta_extraccion
        self.consulta_carga = consulta_carga
    

cantidad=len(lista_carga)
postgresqlConsultas= []

for i in range(cantidad):
    consulta= ConsultaSQL(lista_extraccion[i],lista_carga[i])
    postgresqlConsultas.append(consulta)

