from credenciales import postgres_config_sg, postgres_config_st
from etl import procesar_etl
from sql_consultas import postgresqlConsultas as psql_consultas
import psycopg2

def main():
    print("iniciando ETL ")

    conexion_objetivo=psycopg2.connect(** postgres_config_sg)
    try:
        print("cargando base de datos: {}".format(postgres_config_st['dbname']))
        procesar_etl(psql_consultas,conexion_objetivo,postgres_config_st,'psql')
    except Exception as error:
        print("etl para {} tiene un error".format(postgres_config_st['dbname']))
        print("mensaje de error: {}".format(error))


if __name__ == "__main__":
  main()