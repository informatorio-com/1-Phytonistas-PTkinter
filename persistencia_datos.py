import csv
import os

def cargar_contactos_desde_csv(ruta_archivo, nombres_campos):
    """
    Carga los contactos desde un archivo CSV.
    Retorna una lista de diccionarios de contactos.
    Si el archivo no existe o hay un error, retorna una lista vacía.
    """
    contactos_cargados = []
    if not os.path.exists(ruta_archivo):
        print(f"El archivo '{ruta_archivo}' no existe. Creando uno nuevo vacío.")
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=nombres_campos)
            escritor.writeheader()
        return [] # Retorna lista vacía porque el archivo estaba vacío
    
    try:
        with open(ruta_archivo, mode='r', newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Crear un diccionario para cada contacto con los campos especificados
                # Si un campo no existe en la fila, se asigna una cadena vacía
                contacto = {campo: fila.get(campo, '') for campo in nombres_campos}
                contactos_cargados.append(contacto)
        print(f"Contactos cargados exitosamente desde '{ruta_archivo}'.")
        return contactos_cargados
    except Exception as e:
        print(f"Error al cargar contactos desde '{ruta_archivo}': {e}")
        return [] # Retorna una lista vacía si hay un error de lectura

def guardar_contactos_en_csv(contactos, ruta_archivo, nombres_campos):
    """
    Guarda una lista de contactos en un archivo CSV.
    Retorna True si se guardó correctamente, False en caso contrario.
    """
    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=nombres_campos)
            escritor.writeheader() # Escribir los nombres de los campos como encabezado
            escritor.writerows(contactos) # Escribir todos los contactos de la lista
        print(f"Contactos guardados exitosamente en '{ruta_archivo}'.")
        return True
    except Exception as e:
        print(f"Error al guardar contactos en '{ruta_archivo}': {e}")
        return False