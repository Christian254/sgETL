#!/usr/bin/python
from credenciales import postgres_config_sg, postgres_config_st
from etl import procesar_etl
from sql_consultas import postgresqlConsultas as psql_consultas
import psycopg2
import time
from colorama import init, Fore

init()

def main():
    print(Fore.GREEN+
'''
|  ____|__   __| |     
| |__     | |  | |     
|  __|    | |  | |     
| |____   | |  | |____ 
|______|  |_|  |______| cibercachadas
                        ''')

    print("* (fuente de datos) {} \n* (destino) {}".format(postgres_config_st['dbname'],postgres_config_sg['dbname']))
    time.sleep(1) # espera en segundos

    conexion_objetivo=psycopg2.connect(** postgres_config_sg)
    try:
        print("* cargando bases de datos: {} {}".format(postgres_config_st['dbname'],postgres_config_sg['dbname']))
        procesar_etl(psql_consultas,conexion_objetivo,postgres_config_st,'psql')
    except Exception as error:
        print(Fore.RED+"* ETL en la base de datos {} o en la base de datos {} tiene un error".format(postgres_config_st['dbname'],postgres_config_sg['dbname']))
        print("* mensaje de error: {}".format(error))

    conexion_objetivo.close()
if __name__ == "__main__":
  main()