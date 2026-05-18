# Proceso de Instalación, Carga y Consultas 

## Instalación de Docker

- **Windows:** 
    1. Instalar Docker Descktop desde: https://docs.docker.com/desktop/setup/install/windows-install/
    2. Logearse en la aplicación.

- **Linux:**
    1. `sudo apt-get update`
    2. `sudo apt-get install ca-certificates curl gnupg`
    3. `sudo install -m 0755 -d /etc/apt/keyrings`
    4. `sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc`
    5. `sudo chmod a+r /etc/apt/keyrings/docker.asc`
    6. ```
        echo \ 
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        ```
    8. `sudo apt-get update`
    9. `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`


## Instalación de PostgresSQL en Docker 
- `docker pull postgres:18.4`


## Creación de base de datos y carga
Para crear la base de datos y levantar el contenedor se configura el archivo docker-compose.yml

```
version: '3.9'

services:
  postgres:
    image: postgres
    container_name: postgre_practico_etl
    restart: always
    environment:
      POSTGRES_USER: valentino
      POSTGRES_PASSWORD: 0000
      POSTGRES_DB: practico_etl
    ports:
      - "5432:5432"
    volumes:
      - ./csv:/csv
      - ./initdb:/docker-entrypoint-initdb.d

```

## Procesamiento previo de datos

Fue necesario procesar los datos previamente antes de cargalos a la base debido a que los archivos.csv originales contenían: problemas de codificación, datos adicionales que no necesitabamos y, en caso de organizaciones.csv, una estructura más compleja para almacenar la información.

Para realizar dicha transformación creamos un script en python, en el cual manejamos los conflictos mencionados. "limpieza.py" contiene una función por cada archivo csv a tratar.

