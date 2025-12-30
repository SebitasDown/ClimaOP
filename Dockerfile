# Usamos una imagen ligera de Python 3.12
FROM python:3.12-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copiamos las dependencias e instalamos
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiamos el código de la aplicación
COPY ./app /code/app

# IMPORTANTE: Agregamos /code/app al PYTHONPATH para que los imports funcionen
ENV PYTHONPATH=/code/app

# Comando para correr la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]