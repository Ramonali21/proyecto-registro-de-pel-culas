# Reporte Obligatorio - Sistema de Registro de Películas (Tema #2)
# Desarrollado por: Integrante 4


def mostrar_promedio_por_genero(peliculas):
    """
    Calcula y muestra en consola el reporte obligatorio del Tema #2:
    Promedio de calificación agrupado por cada género registrado,
    junto con la cantidad de películas por género y el promedio general.
    """
    print("\n" + "=" * 65)
    print("       REPORTE: PROMEDIO DE CALIFICACIÓN POR GÉNERO")
    print("=" * 65)

    if not peliculas:
        print("No hay películas registradas para calcular el reporte de promedios.")
        print("=" * 65)
        return

    # Agrupar las calificaciones por género
    calificaciones_por_genero = {}
    for peli in peliculas:
        genero = peli["genero"].strip().title()
        calificacion = float(peli["calificacion"])
        if genero not in calificaciones_por_genero:
            calificaciones_por_genero[genero] = []
        calificaciones_por_genero[genero].append(calificacion)

    print(f"{'Género':<28} | {'Cantidad':<12} | {'Promedio'}")
    print("-" * 65)

    suma_total = 0.0
    conteo_total = 0

    # Ordenar alfabéticamente por género para una mejor presentación
    for genero in sorted(calificaciones_por_genero.keys()):
        lista_calif = calificaciones_por_genero[genero]
        cantidad = len(lista_calif)
        promedio = sum(lista_calif) / cantidad
        suma_total += sum(lista_calif)
        conteo_total += cantidad

        print(f"{genero:<28} | {cantidad:<12} | {promedio:.2f} / 10")

    promedio_general = suma_total / conteo_total if conteo_total > 0 else 0.0
    print("-" * 65)
    print(f"{'PROMEDIO GENERAL DEL CATÁLOGO':<28} | {conteo_total:<12} | {promedio_general:.2f} / 10")
    print("=" * 65)