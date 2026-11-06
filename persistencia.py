# Persistencia de Datos - Sistema de Registro de Películas (Tema #2)
# Desarrollado por: Integrante 3

import json

ARCHIVO_DATOS = "peliculas.json"


def cargar_datos():
    """
    Carga la lista de películas desde el archivo JSON.
    Si el archivo no existe (FileNotFoundError) o está corrupto,
    retorna una lista vacía sin cerrar el programa.
    """
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            if isinstance(datos, list):
                return datos
            return []
    except FileNotFoundError:
        # Si el archivo aún no existe, se retorna una lista vacía para iniciar desde cero
        return []
    except json.JSONDecodeError:
        print("\n[Aviso] El archivo de datos estaba vacío o tenía un formato inválido. Se iniciará una lista nueva.")
        return []
    except Exception as e:
        print(f"\n[Error] No se pudieron cargar los datos: {e}")
        return []


def guardar_datos(peliculas):
    """
    Guarda la lista actual de películas en el archivo JSON.
    """
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(peliculas, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"\n[Error] No se pudieron guardar los datos en '{ARCHIVO_DATOS}': {e}")