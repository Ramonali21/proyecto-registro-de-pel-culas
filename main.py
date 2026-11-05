# Menú Principal - Sistema de Registro de Películas (Tema #2)

from persistencia import cargar_datos
from logica import (
    registrar_pelicula,
    listar_peliculas,
    buscar_peliculas,
    modificar_pelicula,
    eliminar_pelicula,
)
from reportes import mostrar_promedio_por_genero


def mostrar_menu():
    """
    Muestra las opciones del menú interactivo en consola.
    """
    print("\n" + "=" * 55)
    print("   SISTEMA DE GESTIÓN Y REGISTRO DE PELÍCULAS ")
    print("=" * 55)
    print("  1. Registrar una nueva película")
    print("  2. Listar todas las películas")
    print("  3. Buscar películas (por título o género)")
    print("  4. Modificar los datos de una película")
    print("  5. Eliminar una película")
    print("  6. Reporte: Promedio de calificación por género")
    print("  7. Salir del sistema")
    print("=" * 55)


def main():
    """
    Función principal que carga los datos desde el archivo JSON y ejecuta
    el ciclo interactivo del menú hasta que el usuario decida salir.
    """
    peliculas = cargar_datos()
    print("\n¡Bienvenido al Sistema de Registro de Películas!")
    print(f"Se cargaron {len(peliculas)} película(s) almacenadas previamente.")

    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción (1-7): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSaliendo del programa de forma segura. ¡Hasta luego!")
            break

        if opcion == "1":
            registrar_pelicula(peliculas)
        elif opcion == "2":
            listar_peliculas(peliculas)
        elif opcion == "3":
            buscar_peliculas(peliculas)
        elif opcion == "4":
            modificar_pelicula(peliculas)
        elif opcion == "5":
            eliminar_pelicula(peliculas)
        elif opcion == "6":
            mostrar_promedio_por_genero(peliculas)
        elif opcion == "7":
            print("\nDatos guardados correctamente. ¡Gracias por usar el sistema!")
            break
        else:
            print("\n  [!] Opción no válida. Por favor, ingrese un número del 1 al 7.")


if __name__ == "__main__":
    main()