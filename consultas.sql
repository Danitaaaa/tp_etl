// Provincia con mayor inversión cientifica
SELECT 
    p.nombre AS provincia,
    SUM(i.monto) AS total_inversion
FROM provincia p
JOIN inversion i ON p.id = i.id_provincia
GROUP BY p.id, p.nombre
ORDER BY total_inversion DESC
LIMIT 1;

// Cantidad de organizaciones por provincia
SELECT 
    p.nombre AS provincia,
    COUNT(ol.id_organizacion) AS cantidad_organizaciones
FROM provincia p
LEFT JOIN organizacion_locacion ol ON p.id = ol.id_provincia
GROUP BY p.id, p.nombre
ORDER BY cantidad_organizaciones DESC;

// Cantidad de organizaciones segun tipo de institucion
SELECT
    tipo_institucion.nombre, COUNT(organizacion.id_organizacion) AS cantidad_organizaciones
FROM tipo_institucion inner join organizacion on organizacion.id_tipo = tipo_institucion.id
GROUP BY tipo_institucion.nombre
ORDER BY cantidad_organizaciones DESC;
