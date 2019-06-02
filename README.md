## Sistema gerencial CiberCachadas
### Requisitos
    PostgreSQL >= 9.0
    Python >= 3.6

### Instrucciones
Crear entorno virtual con el nombre siguiente:
    `` python -m venv enviroment ``

Activar entorno virtual
    `` enviroment/bin/activate.sh ``

Instalar dependencias del proyecto
    `` pip install -r requirements.txt ``


### Base de datos (setup)

Crear base de datos en PotsgreSQL con nombre **db_sg**

Crear usuario postgreSQL con nombre **usuario** con password 
**holamundo**  

Realizar migraciones
    `` python manage.py migrate ``
