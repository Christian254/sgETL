import psycopg2

def procesar_etl(consultas,conexion_objetivo,configuracion_db_recurso,platoforma_db):

    if platoforma_db=='psql':
        conexion_recurso=psycopg2.connect(**configuracion_db_recurso)
    else:
        return 'Error! no se ha reconocido la fuente de datos' 

    for consulta in consultas:
        etl(consulta,conexion_recurso,conexion_objetivo)
    
    conexion_recurso.close()

def etl(consulta, conexion_recurso, conexion_objetivo):
    #extraccion
    cursor_recurso=conexion_recurso.cursor()
    cursor_recurso.execute(consulta.consulta_extraccion)
    datos=cursor_recurso.fetchall()
    cursor_recurso.close()

    #si la data existe
    if datos:
        cursor_objetivo=conexion_objetivo.cursor()
        cursor_objetivo.executemany(consulta.consulta_carga,datos)
        conexion_objetivo.commit()
        print('Los datos han sido cargados: {} {} '.format(consulta.consulta_extraccion,consulta.consulta_carga))
        cursor_objetivo.close()
    else:
        print("datos estan vacios")






    