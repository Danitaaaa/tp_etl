-- ELIMINAR TABLAS ANTERIORES SI EXISTEN
DROP TABLE IF EXISTS inversiones CASCADE;
DROP TABLE IF EXISTS organizaciones CASCADE;
DROP TABLE IF EXISTS organizaciones_locacion CASCADE;
DROP TABLE IF EXISTS provincias CASCADE;
DROP TABLE IF EXISTS tipo_institucion CASCADE;


-- CREAR TABLAS
CREATE TABLE IF NOT EXISTS provincias (
    id BIGINT PRIMARY KEY,
    nombre VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS inversiones (
    id_inversion BIGSERIAL PRIMARY KEY,
    anio INT,
    monto INT,
    id_provincia BIGINT REFERENCES provincias(id)
);

CREATE TABLE IF NOT EXISTS tipo_institucion (
    id BIGINT PRIMARY KEY,
    nombre VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS organizaciones (
    id_organizacion BIGINT PRIMARY KEY,
    nombre VARCHAR(150),
    id_tipo BIGINT REFERENCES tipo_institucion(id)
);

CREATE TABLE IF NOT EXISTS organizaciones_locacion (
    id BIGSERIAL PRIMARY KEY,
    id_organizacion BIGINT REFERENCES organizaciones(id_organizacion),
    id_provincia BIGINT REFERENCES provincias(id)
);


-- CREAR TABLAS TEMPORALES QUE RECIBEN LOS CSVs
CREATE TEMP TABLE tmp_provincias (
    provincia_id BIGINT,
    nombre TEXT
);

CREATE TEMP TABLE tmp_inversiones (
    provincia_id BIGINT,
    anio INT,
    monto_inversion INT
);

CREATE TEMP TABLE tmp_organizaciones (
    organizacion_id BIGINT,
    nombre TEXT,
    tipo_institucion_id BIGINT
);

CREATE TEMP TABLE tmp_organizaciones_locacion (
    organizacion_id BIGINT,
    provincia_id BIGINT
);

CREATE TEMP TABLE tmp_tipo_institucion (
    tipo_institucion_id BIGINT,
    tipo_institucion_desc TEXT
);


-- COPIAR LOS CSVs EN CADA TABLA TEMP
COPY tmp_provincias
FROM '/csv/provincias.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

COPY tmp_inversiones
FROM '/csv/inversionesXprovincia.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

COPY tmp_organizaciones
FROM '/csv/organizaciones.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

COPY tmp_organizaciones_locacion
FROM '/csv/organizaciones_locacion.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');

COPY tmp_tipo_institucion
FROM '/csv/tipo_instituciones.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', QUOTE '"');


-- CARGAR LOS DATOS EN LAS TABLAS PERMANENTES PARA SU ANALISIS
INSERT INTO provincias (id, nombre)
SELECT provincia_id, nombre FROM tmp_provincias
ON CONFLICT DO NOTHING;

INSERT INTO tipo_institucion (id, nombre)
SELECT tipo_institucion_id, tipo_institucion_desc FROM tmp_tipo_institucion
ON CONFLICT DO NOTHING;

INSERT INTO organizaciones (id_organizacion, nombre, id_tipo)
SELECT DISTINCT o.organizacion_id, o.nombre, o.tipo_institucion_id
FROM tmp_organizaciones o
JOIN tipo_institucion t ON t.id = o.tipo_institucion_id
ON CONFLICT DO NOTHING;

INSERT INTO inversiones (anio, monto, id_provincia)
SELECT i.anio, i.monto_inversion, i.provincia_id
FROM tmp_inversiones i
JOIN provincias p ON p.id = i.provincia_id
ON CONFLICT DO NOTHING;

INSERT INTO organizaciones_locacion (id_organizacion, id_provincia)
SELECT ol.organizacion_id, ol.provincia_id
FROM tmp_organizaciones_locacion ol
JOIN organizaciones o ON o.id_organizacion = ol.organizacion_id
JOIN provincias p ON p.id = ol.provincia_id
ON CONFLICT DO NOTHING;
