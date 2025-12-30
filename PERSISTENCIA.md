# Guía de Persistencia y Comandos Docker

Este archivo documenta cómo ejecutar el proyecto asegurando la persistencia de datos y cómo gestionar el ciclo de vida del contenedor.

## 🚀 Levantar el proyecto

Para iniciar la aplicación y asegurar que los datos guardados en `clima.db` se mantengan (persistan) incluso si reinicias el contenedor:

```bash
sudo docker compose up --build
```
*El flag `--build` reconstruye la imagen si hubo cambios en el código.*

## 🛑 Detener el proyecto

Para detener y eliminar los contenedores (sin borrar tu base de datos):

```bash
sudo docker compose down
```

## 💾 ¿Por qué persisten mis datos?

En el archivo `docker-compose.yml`, hemos configurado un **volumen**:

```yaml
volumes:
  - ./clima.db:/code/clima.db
```

Esto "mapea" o conecta el archivo `clima.db` de tu carpeta actual con el archivo dentro del contenedor. Todo lo que la API guarde dentro, se guarda realmente en tu disco duro.

## 🛠 Generar Dockerfile automáticamente

Si quieres generar estos archivos de configuración (`Dockerfile`, `compose.yaml`) en un proyecto nuevo, puedes usar el comando interactivo oficial:

```bash
docker init
```
*Nota: Este comando analizará tu proyecto y creará los archivos necesarios automáticamente.*
