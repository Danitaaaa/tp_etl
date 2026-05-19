# Trabajo Práctico: ETL y Análisis de Datos Públicos (Argentina)

##  Integrantes - Grupo N° 11

- Diez Gomez, Dana               - 16730 -                <danita.ddg5@gmail.com>
- Heredia, Alba Agustina         - 16739 -                <albaheredia1902@gmail.com>
- Leguizamon, Facundo            - 17018 -                <fleguizamonmarquisio@gmail.com> 
- Magagnini, Carolina            - 16677 -                <carolinamagagninii@gmail.com>
- Pagani, Valentino              - 16619 -                <paganivalentino06@gmail.com>
- Peretti, Ludmila               - 16769 -                <perettiludmila2005@gmail.com>
- Rodriguez, Paul                - 15666 -                <paulfacundo30@gmail.com>

---

## 📌 1. Descripción del Proyecto

Este proyecto implementa un flujo de datos (ETL) automatizado utilizando contenedores. Extrae datos del Portal de Datos Abiertos de la República Argentina, los transforma para garantizar su integridad y los carga en una base de datos relacional para su posterior análisis mediante consultas SQL avanzadas.

### Datasets Seleccionados:

1. **provincias**: catálogo de las 24 provincias argentinas con su ID oficial.
2. **tipo_institucion**: referencia de categorías institucionales (universidades, organismos del estado, empresas, etc.).
3. **inversiones**: montos anuales de inversión en I+D desagregados por provincia.
4. **organizaciones** entidades del sistema científico-tecnológico, clasificadas por tipo.

---

## Modelado Entidad-Relación (DER)

El modelo sigue una estructura relacional normalizada donde la tabla central de control territorial es **Provincia**. Las tablas se vinculan mediante las siguientes relaciones:

* **Provincia e Inversion (1:N):** Se relacionan mediante el campo `id_provincia`. Una provincia puede recibir múltiples inversiones a lo largo de los años, pero cada inversión se asigna a una única provincia específica.
* **Provincia y Organizacion (1:N):** Se relacionan mediante el campo `id_provincia`. Una provincia puede albergar muchas organizaciones instaladas en su territorio, mientras que cada organización pertenece a una sola provincia.
* **Tipo_Institucion y Organizacion (1:N):** Se relacionan mediante el campo `id_tipo`. Un tipo de institución  puede clasificarse y aplicarse a muchas organizaciones, pero cada organización posee un único tipo asignado.

![modelado](<Esquema BD.png>)

---

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

### `docker-compose.yml`
```yaml
services:
  postgres:
    image: postgres:16
    container_name: postgres_tp

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 1234
      POSTGRES_DB: tp_elt

    ports:
      - "5432:5432"

    volumes:
      - ./csv:/csv

  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin_tp

    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin123

    ports:
      - "5050:80"

```


## Procesamiento previo de datos

Fue necesario procesar los datos previamente antes de cargarlos a la base debido a que los 
archivos CSV originales contenían problemas de codificación, columnas innecesarias y, en el 
caso de `organizaciones.csv`, una estructura más compleja para extraer el nombre de cada entidad.

El script `limpieza.py` contiene una función por cada archivo CSV. En todos los casos se 
descartan filas con campos críticos vacíos o nulos, y los archivos resultantes se guardan 
en `csv_procesados/` con separador `;` y codificación UTF-8.

---

### `provincias()` — caso base

El CSV original usa coma como separador. Se seleccionan solo las columnas necesarias y 
se renombran al esquema de destino:

```python
lector = csv.DictReader(infile, delimiter=',')   # original: coma
escritor = csv.DictWriter(outfile, fieldnames=['provincia_id', 'nombre'], delimiter=';')

for fila in lector:
    id_provincia = fila.get('id')
    nombre       = fila.get('nombre')
    if not id_provincia or not nombre:
        continue                          # descarta filas incompletas
    escritor.writerow({'provincia_id': id_provincia.strip(), 'nombre': nombre.strip()})
```

---

### `organizaciones()` — nombre dinámico según nivel jerárquico

Cada organización tiene un campo `nivel` (1, 2 o 3) que indica en qué columna se 
encuentra su nombre descriptivo. Se resuelve dinámicamente:

```python
nivel  = fila.get('nivel')
nombre = fila.get(f'institucion_nivel{nivel}_descripcion')  # columna varía según nivel
```

---

### `inversiones_por_provincia()` — re-codificación y mapeo de provincias

El archivo de inversiones viene en codificación **Latin-1** y referencia las provincias 
por nombre textual en lugar de ID numérico. Se resuelve abriendo con la codificación 
correcta y usando un diccionario construido desde el CSV de provincias ya procesado:

```python
# El archivo original está en Latin-1 → se convierte a UTF-8 al escribir
with open(archivo_origen, mode='r', encoding='latin-1') as infile, \
     open(archivo_destino, mode='w', encoding='utf-8', newline='') as outfile:

    for fila in lector:
        nombre = fila.get('PROVINCIA')
        id_provincia = mapear_nombre_id(diccionario, nombre)  # busca ID por nombre
        if id_provincia is None:
            continue       # descarta provincias no reconocidas
```

El diccionario se construye una sola vez antes del loop:

```python
def crear_diccionario_provincias():
    with open('provincias_procesadas.csv', encoding='utf-8') as infile:
        lector = csv.DictReader(infile, delimiter=';')
        return {fila['provincia_id']: fila['nombre'] for fila in lector}
```
---

## Creación de tablas y carga en PostgreSQL

El archivo `create_tables.sql` centraliza todo el proceso en tres etapas que se ejecutan 
en orden. Se corre una sola vez al levantar el contenedor (o manualmente desde pgAdmin).

---

### Etapa 1 — Definición del esquema

Se crean las tablas definitivas respetando el orden de dependencias: primero las tablas 
sin FK, luego las que las referencian. El `CASCADE` en el `DROP` permite limpiar todo 
sin errores por dependencias circulares:

```sql
DROP TABLE IF EXISTS inversiones CASCADE;
DROP TABLE IF EXISTS organizaciones CASCADE;
DROP TABLE IF EXISTS organizaciones_locacion CASCADE;
DROP TABLE IF EXISTS provincias CASCADE;
DROP TABLE IF EXISTS tipo_institucion CASCADE;

CREATE TABLE IF NOT EXISTS provincias (
    id     BIGINT PRIMARY KEY,
    nombre VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS organizaciones (
    id_organizacion BIGINT PRIMARY KEY,
    nombre          VARCHAR(150),
    id_tipo         BIGINT REFERENCES tipo_institucion(id)   -- FK
);

CREATE TABLE IF NOT EXISTS inversiones (
    id_inversion BIGSERIAL PRIMARY KEY,
    anio         INT,
    monto        INT,
    id_provincia BIGINT REFERENCES provincias(id)            -- FK
);
```

---

### Etapa 2 — Tablas temporales y carga de CSVs

Para cargar los CSVs sin violar restricciones de integridad, primero se vuelcan en 
tablas temporales (sin PK ni FK) usando `COPY`, que lee directamente del volumen Docker:

```sql
CREATE TEMP TABLE tmp_inversiones (
    provincia_id    BIGINT,
    anio            INT,
    monto_inversion INT
);

COPY tmp_inversiones
FROM '/csv/inversionesXprovincia.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');
```

---

### Etapa 3 — Transferencia a tablas definitivas

Una vez cargadas las temporales, se transfieren los datos a las tablas definitivas 
usando `INSERT ... SELECT` con `JOIN` para validar integridad referencial: solo se 
insertan filas cuyas FK existen en las tablas padre. El `ON CONFLICT DO NOTHING` 
evita errores por duplicados:

```sql
INSERT INTO inversiones (anio, monto, id_provincia)
SELECT i.anio, i.monto_inversion, i.provincia_id
FROM tmp_inversiones i
JOIN provincias p ON p.id = i.provincia_id   -- solo inserta si la provincia existe
ON CONFLICT DO NOTHING;
```

Este patrón se repite para cada tabla, respetando siempre el orden de carga: 
`provincias` y `tipo_institucion` primero (no tienen FK), luego `organizaciones`, 
y finalmente `inversiones` y `organizaciones_locacion`.



### Consulta 1: Provincia con mayor inversión cientifica

* **Objetivo:** : Identifica qué provincia concentró la mayor suma histórica de inversión en I+D.

```sql
SELECT 
    p.nombre AS provincia,
    SUM(i.monto) AS total_inversion
FROM provincia p
JOIN inversion i ON p.id = i.id_provincia
GROUP BY p.id, p.nombre
ORDER BY total_inversion DESC
LIMIT 1;
```
**Resultado esperado:**

| provincia | total_inversion |
|---|---|
| Buenos Aires | 1.793.210 |



### Consulta 2: Cantidad de organizaciones por provincia

* **Objetivo:** Muestra el ranking de provincias según cuántas organizaciones del sistema científico tienen radicación allí.
```sql

SELECT 
    p.nombre AS provincia,
    SUM(i.monto) AS total_inversion
FROM provincia p
JOIN inversion i ON p.id = i.id_provincia
GROUP BY p.id, p.nombre
ORDER BY total_inversion DESC
LIMIT 1;
```

**Resultado esperado (primeras filas):**

| provincia | cantidad_organizaciones |
|---|---|
| Buenos Aires | 3425 |
| Santa Fe | 1451 |
| Córdoba | 1287 |
| Tucumán | 600 |
| Mendoza | 592 |

### Consulta 3: Cantidad de organizaciones segun tipo de institucion

* **Objetivo:** : Permite analizar la composición del sistema científico argentino según la naturaleza jurídica de sus organizaciones.

```sql
SELECT
    tipo_institucion.nombre, COUNT(organizacion.id_organizacion) AS cantidad_organizaciones
FROM tipo_institucion inner join organizacion on organizacion.id_tipo = tipo_institucion.id
GROUP BY tipo_institucion.nombre
ORDER BY cantidad_organizaciones DESC;
```
**Resultado esperado (primeras filas):**

| tipo_institucion | cantidad_organizaciones |
|---|---|
| Universidad o instituto universitario estatal | 7539 |
| Empresa | 4365 |
| Organismo gubernamental de ciencia y tecnología | 1776 |
| Entidad administrativa de gobierno | 1641 |
| Universidad o instituto universitario privado | 1307 |

----


