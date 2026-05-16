import csv

def main():
    inversiones_por_provincia()

def organizaciones():
    archivo_origen = 'organizaciones.csv'
    archivo_destino = 'organizaciones_procesadas.csv'

    columnas = ['organizacion_id', 'nombre', 'tipo_institucion_id']

    try:
        with open(archivo_origen, mode='r', encoding='utf-8') as infile, \
            open(archivo_destino, mode='w', encoding='utf-8', newline='') as outfile:
            
            lector = csv.DictReader(infile, delimiter=';')
            escritor = csv.DictWriter(outfile, fieldnames=columnas, delimiter=';', extrasaction='ignore')
            escritor.writeheader()
            
            contador_procesados = 0
            contador_guardados = 0

            for fila in lector:
                contador_procesados += 1
                
                id_org = fila.get('organizacion_id')
                tipo_institucion = fila.get('tipo_institucion_id')

                nivel = fila.get('nivel')
                nombre = fila.get(f'institucion_nivel{nivel}_descripcion')

                if id_org is None or tipo_institucion is None or nombre is None:
                    continue  
                
                id_org = id_org.strip()
                tipo_institucion = tipo_institucion.strip()
                nombre = nombre.strip()

                if id_org == '' or tipo_institucion == '' or nombre == '':
                    continue  
                    
                fila_limpia = {
                    'organizacion_id': id_org,
                    'tipo_institucion_id': tipo_institucion,
                    'nombre': nombre
                }
                
                escritor.writerow(fila_limpia)
                contador_guardados += 1
                
        print("¡Proceso de limpieza completado con éxito!")
        print(f"Registros totales evaluados: {contador_procesados}")
        print(f"Registros guardados en '{archivo_destino}': {contador_guardados}")
        print(f"Registros vacíos o corruptos eliminados: {contador_procesados - contador_guardados}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_origen}' en la carpeta actual.")
    except Exception as e:
        print(f"Error inesperado: {e}")


def organizaciones_localizaciones():
    archivo_origen = 'organizaciones_localizacion.csv'
    archivo_destino = 'organizaciones_localizacion_procesadas.csv'

    diccionario = crear_diccionario_provincias()

    print("Diccionario de provincias creado:", diccionario)

    columnas = ['organizacion_id', 'provincia_id']

    try:
        with open(archivo_origen, mode='r', encoding='utf-8') as infile, \
            open(archivo_destino, mode='w', encoding='utf-8', newline='') as outfile:
            
            lector = csv.DictReader(infile, delimiter=';')
            escritor = csv.DictWriter(outfile, fieldnames=columnas, delimiter=';', extrasaction='ignore')
            escritor.writeheader()
            
            contador_procesados = 0
            contador_guardados = 0

            for fila in lector:
                contador_procesados += 1
                
                id_org = fila.get('organizacion_id')
                nombre = fila.get('dpt_descripcion')
                id_provincia = mapear_nombre_id(diccionario, nombre)

                id_pais = fila.get('pais_id')


                if id_pais is None or id_pais.strip() != '1':
                    continue

                if id_org is None or nombre is None:
                    continue  

                if id_provincia is None:
                    continue
                
                id_org = id_org.strip()
                id_provincia = id_provincia.strip()

                if id_org == '' or id_provincia == '':
                    continue  
                    
                fila_limpia = {
                    'organizacion_id': id_org,
                    'provincia_id': id_provincia
                }
                
                escritor.writerow(fila_limpia)
                contador_guardados += 1
                
        print("¡Proceso de limpieza completado con éxito!")
        print(f"Registros totales evaluados: {contador_procesados}")
        print(f"Registros guardados en '{archivo_destino}': {contador_guardados}")
        print(f"Registros vacíos o corruptos eliminados: {contador_procesados - contador_guardados}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_origen}' en la carpeta actual.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def inversiones_por_provincia():
    archivo_origen = '06._inversion_provincia.csv'
    archivo_destino = 'inversiones_provincia_procesadas.csv'

    diccionario = crear_diccionario_provincias()

    print("Diccionario de provincias creado:", diccionario)

    columnas = ['provincia_id', 'anio', 'monto_inversion']

    try:
        with open(archivo_origen, mode='r', encoding='latin-1') as infile, \
            open(archivo_destino, mode='w', encoding='utf-8', newline='') as outfile:
            
            lector = csv.DictReader(infile, delimiter=';')
            escritor = csv.DictWriter(outfile, fieldnames=columnas, delimiter=';', extrasaction='ignore')
            escritor.writeheader()
            
            contador_procesados = 0
            contador_guardados = 0

            for fila in lector:
                contador_procesados += 1
                
                nombre = fila.get('PROVINCIA')
                anio = fila.get('ANIO')
                monto_inversion = fila.get('INV_ID_PESOS_CORR')


                if anio is None:
                    continue

                if nombre is None:
                    continue  

                id_provincia = mapear_nombre_id(diccionario, nombre)

                if id_provincia is None:
                    continue
                
                if monto_inversion is None:
                    continue

                
                id_provincia = id_provincia.strip()
                anio = anio.strip()
                monto_inversion = monto_inversion.strip()

                if id_provincia == '' or anio == '' or monto_inversion == '':
                    continue
                    
                fila_limpia = {
                    'provincia_id': id_provincia,
                    'anio': anio,
                    'monto_inversion': monto_inversion
                }
                
                escritor.writerow(fila_limpia)
                contador_guardados += 1
                
        print("¡Proceso de limpieza completado con éxito!")
        print(f"Registros totales evaluados: {contador_procesados}")
        print(f"Registros guardados en '{archivo_destino}': {contador_guardados}")
        print(f"Registros vacíos o corruptos eliminados: {contador_procesados - contador_guardados}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_origen}' en la carpeta actual.")
    except Exception as e:
        print(f"Error inesperado: {e}")


def crear_diccionario_provincias():
    archivo = 'provincias_procesadas.csv'

    try:
        diccionario_provincias = {}
        with open(archivo, mode='r', encoding='utf-8') as infile:
            lector = csv.DictReader(infile, delimiter=';')
            for fila in lector:
                id_provincia = fila.get('provincia_id')
                nombre_provincia = fila.get('nombre')
                    
                diccionario_provincias[id_provincia] = nombre_provincia

        return diccionario_provincias 

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}' en la carpeta actual.")
    except Exception as e:
        print(f"Error inesperado: {e}")


def mapear_nombre_id(diccionario, nombre):
    if nombre is None:
        return None
    if nombre.strip() == '':
        return None
    for clave, valor in diccionario.items():
        if valor == nombre:
            return clave
    return None

def provincias():
    archivo_origen = 'provincias.csv'
    archivo_destino = 'provincias_procesadas.csv'

    columnas = ['provincia_id', 'nombre']

    try:
        with open(archivo_origen, mode='r', encoding='utf-8') as infile, \
        open(archivo_destino, mode='w', encoding='utf-8', newline='') as outfile:
            
            lector = csv.DictReader(infile, delimiter=',')
            escritor = csv.DictWriter(outfile, fieldnames=columnas, delimiter=';', extrasaction='ignore')
            escritor.writeheader()
            
            contador_procesados = 0
            contador_guardados = 0

            for fila in lector:
                contador_procesados += 1
                
                id_provincia = fila.get('id')
                nombre = fila.get('nombre')
              

                if id_provincia is None or nombre is None:
                    continue  
                
                id_provincia = id_provincia.strip()
                nombre = nombre.strip()

                if id_provincia == '' or nombre == '':
                    continue  
                    
                fila_limpia = {
                    'provincia_id': id_provincia,
                    'nombre': nombre
                }
                
                escritor.writerow(fila_limpia)
                contador_guardados += 1

            print("¡Proceso de limpieza completado con éxito!")
            print(f"Registros totales evaluados: {contador_procesados}")
            print(f"Registros guardados en '{archivo_destino}': {contador_guardados}")
            print(f"Registros vacíos o corruptos eliminados: {contador_procesados - contador_guardados}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}' en la carpeta actual.")
    except Exception as e:
        print(f"Error inesperado: {e}")

main()