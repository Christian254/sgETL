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
    #se crean los cursores de cada bd
    cursor_recurso=conexion_recurso.cursor()
    cursor_objetivo=conexion_objetivo.cursor()

    #ejecuta la consulta select count(*)
    cursor_objetivo.execute(consulta.consulta_contador)
    contador=cursor_objetivo.fetchone()
    #si el count de la tablas es mayor que cero altera la consulta con off count
    if contador[0]>0:
        cursor_recurso.execute(consulta.consulta_extraccion+" offset {}".format(contador[0]))
        datos=cursor_recurso.fetchall()

        if datos:
            print("\ntabla: {} agregando desde el offset: {}".format(consulta.nombre_tabla,contador[0]))
        else:
            print("\nlos datos siguen lo mismo en la tabla: {}".format(consulta.nombre_tabla))
        
        cursor_recurso.close()
    else:        
        cursor_recurso.execute(consulta.consulta_extraccion)
        datos=cursor_recurso.fetchall()
        cursor_recurso.close()
            #si la data existe
    if datos:   
        cursor_objetivo.executemany(consulta.consulta_carga,datos)
        conexion_objetivo.commit()
        print('Los datos han sido cargados en la bd gerencial: {} '.format(consulta.nombre_tabla))
        cursor_objetivo.close()
    else:
        print("datos estan vacios en tabla: {}".format(consulta.nombre_tabla))



    






    