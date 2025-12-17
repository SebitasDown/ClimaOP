# 🎓 Aprende Docker: Guía "Paso a Paso"

Esta guía te explica cómo construir los archivos de Docker desde cero para cualquier proyecto de Python/FastAPI.

---

## 1. El Dockerfile (La Receta)
Imagina que el `Dockerfile` es una receta de cocina. Le dice a la computadora cómo "cocinar" tu aplicación para que quede lista para servirse.

Vamos a desglosar el archivo que usamos:

```dockerfile
# 1. ELIGIENDO LA BASE
# "Traeme un Linux ligero que ya tenga Python 3.12 instalado".
# slim = versión ligera (ocupa menos espacio).
FROM python:3.12-slim

# 2. PREPARANDO LA COCINA
# "Crea una carpeta llamada /code y trabaja allí".
# Todo lo que hagamos a partir de ahora, ocurrirá dentro de esa carpeta en el contenedor.
WORKDIR /code

# 3. LAS DEPENDENCIAS (Ingredientes)
# Primero copiamos SOLO el archivo de requerimientos.
# ¿Por qué? Porque Docker es inteligente y "guarda en caché" este paso. 
# Si tu código cambia pero tus librerías no, Docker se salta este paso y ahorra tiempo.
COPY ./requirements.txt /code/requirements.txt

# 4. INSTALANDO (Cocinar ingredientes)
# Instalamos las librerías.
# --no-cache-dir: Para no guardar basura temporal y que la imagen pese menos.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. EL CÓDIGO (El plato principal)
# Ahora sí, copiamos tu carpeta 'app' completa dentro del contenedor.
COPY ./app /code/app

# 6. VARIABLE DE ENTORNO (El truco del chef)
# Esto fue lo que nos arregló el problema inicial.
# Le decimos a Python: "Oye, si buscas módulos, búscalos también en /code/app".
ENV PYTHONPATH=/code/app

# 7. SERVIR EL PLATO
# El comando final que ejecuta la aplicación.
# host 0.0.0.0: Es vital en Docker. Significa "escucha conexiones desde fuera del contenedor".
# Si pones 127.0.0.1, nadie desde fuera podrá entrar.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 2. Docker Compose (El Jefe de Cocina)
Mientras que el `Dockerfile` crea una sola imagen, el `docker-compose.yml` organiza cómo corre esa imagen. Es útil para no escribir comandos larguísimos en la terminal.

```yaml
services:
  api:  # Nombre del servicio (puede ser cualquiera)
    build: .  # "Construye el Dockerfile que está en este directorio (.)"
    
    # PERMISOS DE PUERTOS
    # Formato: "PUERTO_PC:PUERTO_CONTENEDOR"
    # "Lo que llegue al puerto 8000 de mi PC, mándalo al 8000 del contenedor".
    ports:
      - "8000:8000"
    
    # PERSISTENCIA (Volúmenes)
    # Formato: "RUTA_PC:RUTA_CONTENEDOR"
    # "Haz un espejo: que el archivo clima.db de mi PC sea el mismo que el de dentro".
    # Si la app escribe en la DB de dentro, aparece mágicamente en tu PC.
    volumes:
      - ./clima.db:/code/clima.db
    
    # REINICIO
    # "Si la app falla o se cae, vuélvela a levantar automáticamente".
    restart: always
```

---

## 🧪 ¿Cómo practicar?

Para tu próximo proyecto, intenta esto:

1.  Crea un archivo vacío llamado `Dockerfile`.
2.  Copia la estructura básica: `FROM` -> `WORKDIR` -> `COPY` -> `RUN` -> `CMD`.
3.  Ajusta el nombre del archivo principal en el `CMD`.
4.  Ejecuta `docker build -t mi-app .` para ver si construye.

¡Esa es la mejor forma de aprender!
