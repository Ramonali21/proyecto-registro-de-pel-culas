# Lógica CRUD y Validaciones - Sistema de Registro de Películas
import importlib
import json
from pathlib import Path
# CONFIGURACIÓN DE PERSISTENCIA Y GUARDADO
try:
    # Intenta cargar la función de guardado desde un módulo externo llamado "persistencia"
    guardar_datos = importlib.import_module("persistencia").guardar_datos
except ModuleNotFoundError as error:
    # Si el error es por otro módulo que falta "levanta la excepción normalmente"
    if error.name != "persistencia":
        raise

    # Si no existe el módulo persistencia, crea esta función de respaldo para que el programa no colapse
    def guardar_datos(peliculas):
        """Guarda los datos localmente si el módulo persistencia no está disponible."""
        try:
            # Abre (o crea) el archivo peliculas.json en modo escritura ("w") con formato utf-8
            with Path("peliculas.json").open("w", encoding="utf-8") as archivo:
                # Convierte la lista de diccionarios a formato JSON y la guarda con indentación para que sea legible
                json.dump(peliculas, archivo, ensure_ascii=False, indent=4)
        except OSError as error:
            # Captura errores del sistema operativo (ej. falta de permisos o disco lleno)
            print(f"Error al guardar las películas: {error}")

#funciones de entrada 
def solicitar_texto_no_vacio(mensaje):
    """
    Solicita una cadena de texto al usuario y valida que no esté vacía.
    """
    while True: # Bucle infinito que se rompe solo cuando el usuario ingresa un dato válido
        try:
            # Captura la entrada y elimina espacios en blanco al inicio y al final con .strip()
            texto = input(mensaje).strip()
            if texto:
                return texto # Si el texto contiene caracteres, lo devuelve
            print("   Error: Este campo no puede quedar vacío. Intente nuevamente.")
        except (EOFError, KeyboardInterrupt):
            # Atrapa si el usuario presiona Ctrl+C o Ctrl+D para cancelar sin que el programa explote
            print("\n   Entrada cancelada.")
            return ""


def solicitar_anio(mensaje):
    """
    Solicita el año de estreno como un número entero válido (entre 1888 y 2100).
    Usa bloques try/except para evitar cierres por ValueError.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            anio = int(entrada) # Intenta convertir el texto a número entero
            # Verifica que el año sea coherente (1888 fue el año de la primera película de la historia)
            if 1920 <= anio <= 2100:
                return anio
            print("   Error: Ingrese un año válido (entre 1920 y 2100).")
        except ValueError:
            # Si el usuario escribe letras en lugar de números, se atrapa el error aquí
            print("  Error: Debe ingresar un número entero válido para el año (ej. 2067).")


def solicitar_calificacion(mensaje):
    """
    Solicita la calificación de la película (número decimal o entero de 1 a 10).
    Usa bloques try/except para evitar cierres por ValueError.
    """
    while True:
        try:
            # Reemplaza la coma por un punto para que Python pueda convertir el string a float correctamente
            entrada = input(mensaje).strip().replace(",", ".")
            calificacion = float(entrada)
            # Valida el rango de calificación
            if 1.0 <= calificacion <= 10.0:
                return round(calificacion, 2) # Devuelve el número redondeado a máximo 2 decimales
            print("   Error: La calificación debe estar en el rango de 1 a 10.")
        except ValueError:
            print("   Error: Debe ingresar un valor numérico válido (ej. 8.5 o 9).")

#operaciones de registro, listado y búsqueda

def registrar_pelicula(peliculas):
    """
    Captura los datos de una nueva película, la agrega a la lista y guarda en JSON.
    """
    print("\n" + "=" * 55)
    print("              REGISTRAR NUEVA PELÍCULA")
    print("=" * 55)

    # Solicita el título. Si la función devuelve vacío (porque canceló), sale del registro.
    titulo = solicitar_texto_no_vacio("Título de la película: ")
    if not titulo:
        return

    # Solicita el género y le aplica .title() para que la primera letra de cada palabra sea mayúscula
    genero = solicitar_texto_no_vacio("Género (ej. Acción, Ciencia Ficción, Drama): ").title()
    if not genero:
        return

    # Solicita el año y la calificación usando sus respectivas validaciones numéricas
    anio = solicitar_anio("Año de estreno: ")
    calificacion = solicitar_calificacion("Calificación (1 a 10): ")

    # Empaqueta todos los datos validados en un diccionario
    nueva_pelicula = {
        "titulo": titulo,
        "genero": genero,
        "anio": anio,
        "calificacion": calificacion
    }

    # Agrega el diccionario a la lista principal en memoria
    peliculas.append(nueva_pelicula)
    # Ejecuta el guardado en el archivo externo
    guardar_datos(peliculas)
    print(f"\n[Éxito] La película '{titulo}' fue registrada y guardada correctamente.")


def listar_peliculas(peliculas):
    """
    Muestra todas las películas registradas en formato de tabla por consola.
    """
    print("\n" + "=" * 75)
    print("                         LISTADO DE PELÍCULAS")
    print("=" * 75)

    # Si la lista está vacía, avisa al usuario y corta la ejecución de la función
    if not peliculas:
        print("No hay películas registradas en el sistema actualmente.")
        print("=" * 75)
        return

    # Imprime la cabecera de la tabla dándole anchos fijos a cada columna (ej. <30 alinea a la izquierda ocupando 30 espacios)
    print(f"{'N°':<4} | {'Título':<30} | {'Género':<18} | {'Año':<6} | {'Calif.'}")
    print("-" * 75)
    
    # enumerate() recorre la lista obteniendo tanto la posición (índice) como los datos, arrancando en 1
    for indice, peli in enumerate(peliculas, start=1):
        # Acorta los títulos y géneros si exceden el límite de caracteres para evitar que se desarme el formato de la tabla
        titulo_corto = (peli["titulo"][:27] + "...") if len(peli["titulo"]) > 30 else peli["titulo"]
        genero_corto = (peli["genero"][:15] + "...") if len(peli["genero"]) > 18 else peli["genero"]
        
        # Imprime la fila completa inyectando las variables formateadas (.1f obliga a mostrar 1 decimal)
        print(f"{indice:<4} | {titulo_corto:<30} | {genero_corto:<18} | {peli['anio']:<6} | {peli['calificacion']:.1f}/10")
    
    print("=" * 75)
    print(f"Total de películas registradas: {len(peliculas)}")


def buscar_peliculas(peliculas):
    """
    Permite buscar películas por coincidencia parcial en el título o en el género.
    """
    print("\n" + "=" * 55)
    print("                  BUSCAR PELÍCULAS")
    print("=" * 55)

    if not peliculas:
        print("No hay películas registradas para realizar búsquedas.")
        return

    # Captura la palabra a buscar y la convierte a minúscula para que la búsqueda no sea sensible a mayúsculas
    criterio = solicitar_texto_no_vacio("Ingrese el título o género a buscar: ").lower()
    if not criterio:
        return

    # Comprensión de listas: construye una nueva lista filtrando las películas que coincidan
    # Guarda una tupla (indice, datos_pelicula) si el criterio se encuentra dentro del título o el género
    resultados = [
        (indice, peli)
        for indice, peli in enumerate(peliculas, start=1)
        if criterio in peli["titulo"].lower() or criterio in peli["genero"].lower()
    ]

    # Verifica si la lista de resultados quedó vacía
    if not resultados:
        print(f"\nNo se encontraron películas que coincidan con '{criterio}'.")
        return

    # Muestra la cantidad de coincidencias
    print(f"\nSe encontraron {len(resultados)} coincidencia(s):")
    print("-" * 75)
    print(f"{'N°':<4} | {'Título':<30} | {'Género':<18} | {'Año':<6} | {'Calif.'}")
    print("-" * 75)
    
    # Itera sobre la lista filtrada imprimiendo los resultados con el mismo formato que la función de listar
    for indice, peli in resultados:
        titulo_corto = (peli["titulo"][:27] + "...") if len(peli["titulo"]) > 30 else peli["titulo"]
        genero_corto = (peli["genero"][:15] + "...") if len(peli["genero"]) > 18 else peli["genero"]
        print(f"{indice:<4} | {titulo_corto:<30} | {genero_corto:<18} | {peli['anio']:<6} | {peli['calificacion']:.1f}/10")
    print("-" * 75)


# Modificar pelicula

def modificar_pelicula(peliculas):
    print("\n" + "=" * 55)
    print("\tMODIFICAR PELI")
    print("=" * 55)

    if not peliculas:
        print("no hay peliculas disponibles para modificar")
        return
    listar_peliculas(peliculas)
    
    try:
        seleccion = int(input("\nIngrese el numero de la pelicula que desea modificar (0 para cancelar): ").strip())
        if seleccion == 0:
            print("Operacion detenida")
            return
        if seleccion < 1 or seleccion > len(peliculas):
            print("El numero ingresado no corresponde a ninguna pelicula de la lista")
            return
    except ValueError:
        print("Debe ingresar un numero entero valido")
        return
    
    peli = peliculas[seleccion - 1]
    print(f"\nEditando: '{peli['titulo']}' (Presione Enter para conservar el valor actual)")

    nuevo_titulo = input(f"Nuevo titulo [{peli['titulo']}]: ").strip()
    if nuevo_titulo:
        peli["titulo"] = nuevo_titulo

    nuevo_genero = input(f"Nuevo género [{peli['genero']}]: ").strip()
    if nuevo_genero:
        peli["genero"] = nuevo_genero.title()

    while True:
        nuevo_anio_str = input(f"Nuevo año [{peli['anio']}]: ").strip()
        if not nuevo_anio_str:
            break
        try:
            nuevo_anio = int(nuevo_anio_str)
            if 1920 <= nuevo_anio <= 2100:
                peli["anio"] = nuevo_anio
                break
            print("El año debe estar entre 1920 y 2100.")
        except ValueError:
            print("Ingrese un número entero válido para el año.")
    
    while True:
        nueva_calif_str = input(f"Nueva calificación (1-10) [{peli['calificacion']}]: ").strip().replace(",", ".")
        if not nueva_calif_str:
            break
        try:
            nueva_calif = float(nueva_calif_str)
            if 1.0 <= nueva_calif <= 10.0:
                peli["calificacion"] = round(nueva_calif, 2)
                break
            print(" La calificación debe estar entre 1 y 10.")
        except ValueError:
            print("Ingrese un número válido para la calificación.")

def eliminar_pelicula(peliculas):
    print("\n" + "=" * 55)
    print("                  ELIMINAR PELÍCULA")
    print("=" * 55)

    if not peliculas:
        print("no hay pelis para eliminar, si quieres eliminar una, agregue una primero")
        return
    
    listar_peliculas(peliculas)

    try:
        seleccion = int(input("\nIngrese el número (N°) de la película que desea eliminar (0 para cancelar): ").strip())
        if seleccion == 0:
            print("Operacion cancelá")
            return
        if seleccion < 1 or seleccion > len(peliculas):
            print("  [!] Error: El número ingresado no corresponde a ninguna película de la lista.")
            return
    except ValueError:
        print("  [!] Error: Debe ingresar un número entero válido.")
        return
        
    peli_a_borrar = peliculas[seleccion - 1]
    confirmacion = input(f"¿Está seguro de que desea eliminar '{peli_a_borrar['titulo']}'? (s/n): ").strip().lower()

    if confirmacion == "s":
        eliminada = peliculas.pop(seleccion - 1)
        guardar_datos(peliculas)
        print(f"\n[Éxito] La película '{eliminada['titulo']}' fue eliminada del sistema.")
    else:
        print("\nEliminación cancelada.")
