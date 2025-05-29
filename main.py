from algoritmo.ensamblador import ensamblar_rompecabezas, ensamblar_rompe_piezasperdidas
from database.driver import driver, close_driver
from load_puzzle import cargar_rompecabezas
from data.puzzle_data import rompecabezas_data
from neo4j.exceptions import Neo4jError


def cargar_puzzles():
    with driver.session() as session:
        for puzzle in rompecabezas_data:
            try:
                session.execute_write(cargar_rompecabezas, puzzle)
                print(f"-> Puzzle '{puzzle['nombre']}' cargado correctamente.")
            except Neo4jError as e:
                print(f"XX Error al cargar '{puzzle['nombre']}': {e}")
    print("\n Todos los rompecabezas fueron procesados.\n")


def obtener_nombres_puzzles():
    with driver.session() as session:
        result = session.run("MATCH (r:Rompecabezas) RETURN DISTINCT r.nombre AS nombre ORDER BY nombre")
        return [record["nombre"] for record in result]


def ensamblar():
    nombres = obtener_nombres_puzzles()
    if not nombres:
        print("\n No hay puzzles cargados en la base de datos.\n")
        return

    print("\n---------------------------\nPuzzles disponibles:")
    for i, nombre in enumerate(nombres, 1):
        print(f"{i}. {nombre}")

    try:
        opcion = int(input("\nSeleccione el número del puzzle a ensamblar: "))
        rompecabezas_nombre = nombres[opcion - 1]
    except (ValueError, IndexError):
        print("XX Opción inválida.")
        return

    pieza_id = input("Ingrese el ID de la pieza inicial: ").strip()

    print("\n¿Faltan piezas en el rompecabezas?")
    print("1. Sí")
    print("2. No")
    faltan_input = input("Seleccione una opción: ").strip()

    piezas_faltantes = []

    if faltan_input == "1":
        ids_faltantes = input("Ingrese los IDs de las piezas faltantes, separados por comas (sin espacios): ").strip()
        piezas_faltantes = ids_faltantes.split(",") if ids_faltantes else []

    try:
        if piezas_faltantes:
            resultado = ensamblar_rompe_piezasperdidas(pieza_id, rompecabezas_nombre, piezas_faltantes)
        else:
            resultado = ensamblar_rompecabezas(pieza_id, rompecabezas_nombre)
    except Exception as e:
        print(f"Error durante el ensamblaje: {e}")
        return

    if resultado:
        print("\n🧩 Piezas conectadas en orden de ensamblaje:")
        for id in resultado:
            print(f" - {id}")
        print(f"\nTotal: {len(resultado)} piezas ensambladas.")
        if piezas_faltantes:
            print(f"{len(piezas_faltantes)} piezas faltantes fueron omitidas.")
    else:
        print("No se pudo ensamblar el rompecabezas.")
    print()


def menu():
    while True:
        print("=== Menú Principal ===")
        print("1. Cargar puzzles")
        print("2. Ensamblar puzzle")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            cargar_puzzles()
        elif opcion == "2":
            ensamblar()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("XX Opción no válida.\n")

    close_driver()


if __name__ == "__main__":
    menu()
