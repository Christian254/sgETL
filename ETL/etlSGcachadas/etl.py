#!/usr/bin/python
import psycopg2
import time
from credenciales import postgres_config_sg,postgres_config_st
from consultas_carga import diccionario_tablas_persistentes as tbls_persistentes, tablas_dependencias_persistentes as tbls_dependientes
from consultas_carga import lista_tablas_gerencial

def procesar_etl(consultas,conexion_objetivo,configuracion_db_recurso,platoforma_db):

    #realiza conexion de la base de datos recurso
    if platoforma_db=='psql':
        conexion_recurso=psycopg2.connect(**configuracion_db_recurso)
    else:
        return '* Error! no se ha reconocido la fuente de datos' 

    #se crea el cursos para moverse en la db
    cursor_objetivo=conexion_objetivo.cursor()
    #almacenara  diccionario de cantidad de datos por tabla cantidad_por_tabla {"nombre_tabla":cantidad,"nombre_tabla":cantidad ...}
    cantidad_por_tabla={}

    #recorre todas las consultas para generar el diccionario
    for consulta in consultas:
        cursor_objetivo.execute(consulta.consulta_contador_gerencial)
        conteo_tabla_objetivo=cursor_objetivo.fetchone()
        cantidad_por_tabla[consulta.nombre_tabla_gerencial]=conteo_tabla_objetivo[0]
    
    print(
        '''
================================================================== 
  CANTIDAD DATOS POR TABLA PRESENTE EN LA BASE DE DATOS OBJETIVO  
==================================================================

    ''')
    #imprime los datos del diccionario para brindar informacion
    for tabla, cantidad in cantidad_por_tabla.items():
        print("{} => {}".format(tabla,cantidad))

    time.sleep(2) # espera en segundos

    #se ejecuta el volcado  en ciclo si almenos una tabla dispone de datos
    for tabla, cantidad in cantidad_por_tabla.items():
        if cantidad>0:
            volcando_datos(conexion_objetivo,tbls_persistentes) #si se encuentra un mayor a cero se vuelca la tabla
            break

    
        
    print(
        '''
===================================================================== 
   EXTRAYENDO REGISTROS DE LAS TABLAS DE LA BASE DE DATOS: {}  
   INSERTANDO REGISTROS DE LAS TABLAS A LA BASE DE DATOS:  {}
=====================================================================

    '''.format(postgres_config_st["dbname"],postgres_config_sg["dbname"]))    
    #se ejecuta siendo primera vez o despues de volcado
    for consulta in consultas:
        etl(consulta,conexion_recurso,conexion_objetivo)

    time.sleep(1)
    #ejecutando la funcion para recuperar las tablas persistentes
    insertandoPersistentes(conexion_objetivo)

    conexion_recurso.close()

def insertandoPersistentes(conexion_objetivo):
    print(
        '''
===================================================================== 
 EXTRAYENDO REGISTROS DE LAS TABLAS HISTORICAS DE LA BASE DE DATOS: {} 
=====================================================================

    '''.format(postgres_config_sg["dbname"]))

    #preservando data historica producto potencial
    cursor_objetivo=conexion_objetivo.cursor()
    cursor_objetivo.execute('select  id, "idCliente","idProducto",cantidad,"fechaInicio","fechaFin" from gerencial_productoconsignahistorico')
    datosProductoConsigna=cursor_objetivo.fetchall()
    cursor_objetivo.executemany('insert into gerencial_productoconsigna (id, "idCliente","idProducto",cantidad,"fechaInicio","fechaFin") values(%s, %s, %s, %s,%s,%s)',datosProductoConsigna)
    conexion_objetivo.commit()
    if datosProductoConsigna:
        print('* Los datos han sido extraidos de la tabla: {}\n\t+ cargados a la tabla: {}\n'
                .format("gerencial_productoconsignahistorico","gerencial_productoconsigna"))
    
    #preservando data historica producto potencial
    cursor_objetivo.execute(' select  id,"idCliente",nombre,fecha,cantidad from gerencial_productopotencialhistorico')
    datosProductosPotencial=cursor_objetivo.fetchall()
    cursor_objetivo.executemany(' insert into  gerencial_productopotencial(id,"idCliente",nombre,fecha,cantidad ) values (%s,%s,%s,%s,%s)',datosProductosPotencial)
    conexion_objetivo.commit()
    if datosProductosPotencial:
        print('* Los datos han sido extraidos de la tabla: {}\n\t+ cargados a la tabla: {}\n'
            .format("gerencial_productopotencialhistorico","gerencial_productopotencial"))

    #preservando data historica producto retorno
    cursor_objetivo.execute('select id,"idCliente","idProducto","idProveedor",cantidad,nombre_cliente,nombre_producto,codigo,fecha from gerencial_productoretornohistorico')
    datosProductoRetorno=cursor_objetivo.fetchall()
    cursor_objetivo.executemany('insert into gerencial_productoretorno into( id,"idCliente","idProducto","idProveedor",cantidad,nombre_cliente,nombre_producto,codigo,fecha) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ',datosProductoRetorno)

    if datosProductoRetorno:
        print('* Los datos han sido extraidos de la tabla: {}\n\t+ cargados a la tabla: {}\n'
            .format("gerencial_productoretornohistorico","gerencial_productoretonrno"))

    
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
        print('* Los datos han sido extraidos de la tabla: {}\n\t+ cargados a la tabla: {}\n'
            .format(consulta.nombre_tabla_trans,consulta.nombre_tabla_gerencial))
        cursor_objetivo.close()
    else:
        print("No hay datos que extraer en la tabla : {}".format(consulta.nombre_tabla_trans))


#conexion objetivo y lista de tablas
def volcando_datos(conexion,lista):
    cursor=conexion.cursor()

    #volcando ultima version de historico tablas persistentes
    for tabla_lista_borrar in tbls_persistentes.keys():
        cursor.execute("delete from {}".format(tabla_lista_borrar+"historico"))
        conexion.commit()

#insertando los datos que deben persistir en la base de datos historica
    print(
    '''
================================================================== 
              ACTUALIZANDO REGISTROS HISTORICOS                    
==================================================================

''')
    for tabla_lista_borrar in tbls_persistentes.keys():
        if tabla_lista_borrar=="gerencial_productoconsigna":
            cursor.execute('select  id, "idCliente","idProducto",cantidad,"fechaInicio","fechaFin" from gerencial_productoconsigna')
            datos=cursor.fetchall()
            if datos:
                print("* actualizando datos historicos de tabla: "+tabla_lista_borrar+"historico")
            cursor.executemany('insert into gerencial_productoconsignahistorico(id, "idCliente","idProducto",cantidad,"fechaInicio","fechaFin") values(%s,%s,%s,%s,%s,%s)',datos)
            conexion.commit()

        elif tabla_lista_borrar=="gerencial_productopotencial":
            cursor.execute('select  id,"idCliente",nombre,fecha,cantidad from gerencial_productopotencial')
            datos=cursor.fetchall()
            if datos:
                print("* actualizando datos historicos de tabla: "+tabla_lista_borrar+"historico")
            cursor.executemany('insert into  gerencial_productopotencialhistorico(id,"idCliente",nombre,fecha,cantidad) values(%s,%s,%s,%s,%s)',datos)
            conexion.commit()
        else:
            cursor.execute('select id,"idCliente","idProducto","idProveedor",cantidad,nombre_cliente,nombre_producto,codigo,fecha from gerencial_productoretorno')
            datos=cursor.fetchall()
            if datos:
                print("* actualizando datos historicos de tabla: "+tabla_lista_borrar+"historico")
            cursor.executemany('insert into  gerencial_productoretornohistorico(id,"idCliente","idProducto","idProveedor",cantidad,nombre_cliente,nombre_producto,codigo,fecha) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',datos)
            conexion.commit()

    time.sleep(1)
    print(
        '''
===================================================================== 
    VOLCANDO REGISTROS DE LAS TABLAS EN  LA BASE DE DATOS: {}     
=====================================================================

    '''.format(postgres_config_sg["dbname"]))    

    for tabla_lista_borrar in tbls_persistentes.keys():

        #borrando los datos totalmente siendo estas las tablas persistentes    
        cursor.execute("delete from {} ".format(tabla_lista_borrar))
        conexion.commit()
        print("- se han eliminado los registros de la tabla {} en la base de datos: {}".format(tabla_lista_borrar,postgres_config_sg["dbname"]))
    

    #borrando tablas no persistentes
    for tabla_lista_borrar in (reversed(lista_tablas_gerencial)):
        cursor.execute("delete from {} ".format(tabla_lista_borrar))
        print("- se han eliminado los registros de la tabla {} en la base de datos: {}".format(tabla_lista_borrar,postgres_config_sg["dbname"]))
    
        conexion.commit()
    time.sleep(1)

    