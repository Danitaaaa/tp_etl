//Provincia con mayor inversión cientifica
SELECT
    provincia.nombre, SUM(inversion_cientifica) AS total_inversion_cientifica
FROM provincia inner join inversion on provincia.id = inversion.provincia_id
GROUP BY provincia.nombre
ORDER BY total_inversion DESC
LIMIT 1;

//Cantidad de organizaciones por provincia
SELECT
    provincia.nombre, COUNT(organizacion.id) AS cantidad_organizaciones
FROM provincia inner join organizacion on organizacion.provincia_id = provincia.id
GROUP BY provincia.nombre
ORDER BY cantidad_organizaciones DESC;

//Cantidad de organizaciones segun tipo de institucion
SELECT
    tipo_institucion.nombre, COUNT(organizacion.id) AS cantidad_organizaciones
FROM tipo_institucion inner join organizacion on organizacion.tipo_institucion_id = tipo_institucion.id
GROUP BY tipo_institucion.nombre
ORDER BY cantidad_organizaciones DESC;
