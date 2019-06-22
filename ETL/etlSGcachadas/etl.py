import psycopg2
from consultas_carga import diccionario_tablas_persistentes as tbls_persistentes, tablas_dependencias_persistentes as tbls_dependientes
from consultas_carga import lista_tablas_gerencial

def procesar_etl(consultas,conexion_objetivo,configuracion_db_recurso,platoforma_db):

    #realiza conexion de la base de datos recurso
    if platoforma_db=='psql':
        conexion_recurso=psycopg2.connect(**configuracion_db_recurso)
    else:
        return 'Error! no se ha reconocido la fuente de datos' 

    #se crea el cursos para moverse en la db
    cursor_objetivo=conexion_objetivo.cursor()
    #almacenara  diccionario de cantidad de datos por tabla cantidad_por_tabla {"nombre_tabla":cantidad,"nombre_tabla":cantidad ...}
    cantidad_por_tabla={}

    #recorre todas las consultas para generar el diccionario
    for consulta in consultas:
        cursor_objetivo.execute(consulta.consulta_contador_gerencial)
        conteo_tabla_objetivo=cursor_objetivo.fetchone()
        cantidad_por_tabla[consulta.nombre_tabla_gerencial]=conteo_tabla_objetivo[0]
    
    print("==== Cantidad de datos por tabla ====")
    #imprime los datos del diccionario para brindar informacion
    for tabla, cantidad in cantidad_por_tabla.items():
        print("{} => {}".format(tabla,cantidad))
    
    #se ejecuta el volcado  en ciclo si almenos una tabla dispone de datos
    for tabla, cantidad in cantidad_por_tabla.items():
        if cantidad>0:
            volcando_datos(conexion_objetivo,tbls_persistentes) #si se encuentra un mayor a cero se vuelca la tabla
            break

    
        

    #se ejecuta siendo primera vez o despues de volcado
    for consulta in consultas:
        etl(consulta,conexion_recurso,conexion_objetivo)
    
    conexion_recurso.close()

def etl(consulta, conexion_recurso, conexion_objetivo):
    #se crean los cursores de cada bd
    cursor_recurso=conexion_recurso.cursor()
    cursor_objetivo=conexion_objetivo.cursor()

    #se extraen los datos de la consulta extraccion
    cursor_recurso.execute(consulta.consulta_extraccion)
    datos=cursor_recurso.fetchall()
    cursor_recurso.close()
    
    #si la data existe
    if datos:   
        cursor_objetivo.executemany(consulta.consulta_carga,datos)
        conexion_objetivo.commit()
        print('Los datos han sido extraidos de la tabla: {} \n  cargados a la tabla: {}'
            .format(consulta.nombre_tabla_trans,consulta.nombre_tabla_gerencial))
        cursor_objetivo.close()
    else:
        print("No hay datos que extraer en la tabla : {}".format(consulta.nombre_tabla_trans))


def volcando_datos(conexion,lista):
    cursor=conexion.cursor()
    #preparacion de id referencia
    id_almacenados={}
    #obteniendo los id por cada referencia
    for tabla,relaciones in lista.items():
        for relacion in relaciones:
            if relacion in id_almacenados:
                cursor.execute("select {} from {}".format(relacion,tabla))
                resultado = [item[0] for item in cursor.fetchall()]
                id_almacenados[relacion]+=resultado
            else:
                id_almacenados[relacion]=[]
                cursor.execute("select {} from {}".format(relacion,tabla))
                resultado = [item[0] for item in cursor.fetchall()]
                id_almacenados[relacion]=resultado


    #limpiando los id existentes
    for key,lista_repetidos in id_almacenados.items():
        lista_limpia=list(dict.fromkeys(lista_repetidos)) #limpiando data de id repetida
        id_almacenados[key]=lista_limpia #agregando al diccionario la data limpia

    #borrando los datos que 
    for tabla_lista_borrar in (reversed(lista_tablas_gerencial)):

        if  tabla_lista_borrar in tbls_dependientes.keys():
            relacion=tbls_dependientes.get(tabla_lista_borrar)
            ids=id_almacenados[relacion]
            longitud=len(ids)

            if longitud>0:
                parentesis_not_in="("
                for id in ids:
                    parentesis_not_in+="{},".format(id)
                parentesis_not_in=parentesis_not_in[:-1] #eliminando ultima ,
                parentesis_not_in+=")" #agregando el ultimo ) => (1,1,1,1,1)
                
                print("delete from {} where id not in  {}".format(tabla_lista_borrar,parentesis_not_in))
                cursor.execute("delete from {} where id not in  {}".format(tabla_lista_borrar,parentesis_not_in))
                conexion.commit()
            else:
                cursor.execute("delete from {}".format(tabla_lista_borrar))
        else:
            cursor.execute("delete from {} ".format(tabla_lista_borrar))
            conexion.commit()


    