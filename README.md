## Sistema gerencial CiberCachadas
### Requisitos
    PostgreSQL >= 9.0
    Python >= 3.6

### Instrucciones

1. Posicionarse en ```bash cd sgCiberCachadas/ ```
2. Crear entorno virtual con el nombre siguiente:
    ```bash python -m venv enviroment ```

3. Activar entorno virtual en linux
    ```bash enviroment/bin/activate.sh ```
4. Activar entorno virtual en windows
	```bash enviroment/Scripts/activate.bat ```

5. Instalar dependencias del proyecto
    ```bash pip install -r requirements.txt ```


#### Base de datos (setup)
6. Crear usuario postgreSQL con nombre **usuario** con password **holamundo*
 ``` create user usuario password 'holamundo' ```
7. Crear base de datos en PotsgreSQL con nombre **db_sg** asignarla a usuario **usuario**
 ``` create database db_sg owner usuario ```
8. ubicarse un directorio arriba ```bash cd sgCibercachadas/sgCibercachadas ```
9. Realizar migraciones
    ```bash python manage.py migrate ```
10. Agregar fixtures
	```bash python manage.py loaddata groups.json users.json ```

## ETL Script

### Instrucciones
1. Posicionarse en ```bash cd ETL/ ```
2. Crear entorno virtual con el nombre siguiente:
    ```bash python -m venv etl_env ```

3. Activar entorno virtual en linux
    ```bash source etl_env/bin/activate ```
4. Activar entorno virtual en windows
	```bash etl_env/Scripts/activate.bat ```

5. Instalar dependencias del proyecto
    ```bash pip install -r requirements.txt ```

#### Base de datos (setup)
6. Crear base de datos en PotsgreSQL con nombre **db_st** asignarla a usuario **usuario**
 ``` create database db_sg owner usuario ```
7. Cargar backup de ubicado en la carpeta ```bash BD-Transaccional/dsi-backup.backup```
8. ubicarse un directorio arriba ```bash cd ETL/etlSGcachadas ```
9. ejecutar script ```bash python main.py ```
 