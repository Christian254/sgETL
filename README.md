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
Realizar migraciones
    `` python manage.py migrate ``
