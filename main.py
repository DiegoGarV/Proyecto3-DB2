from algoritmo.ensamblador import ensamblar_rompecabezas

if __name__ == "__main__":
    rompecabezas_nombre = input("Ingrese el nombre del rompecabezas: ").strip()
    pieza_id = input("Ingrese el ID de la pieza inicial: ").strip()
    
    resultado = ensamblar_rompecabezas(pieza_id, rompecabezas_nombre)
    print("\nPiezas conectadas en orden de ensamblaje:")
    for id in resultado:
        print(f" - {id}")
