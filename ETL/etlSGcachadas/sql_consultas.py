st_extraccion = ('''
  SELECT nombre
  FROM prueba;
''')

sg_carga=('''
    INSERT INTO gerencial_categoria(nombre)  values( %s )
''')

class ConsultaSQL:
    def __init__(self, consulta_extraccion, consulta_carga):
        self.consulta_extraccion = consulta_extraccion
        self.consulta_carga = consulta_carga
    
    
psql_consulta_categoria = ConsultaSQL(st_extraccion, sg_carga)

# store as list for iteration
psql_consultas=[psql_consulta_categoria]