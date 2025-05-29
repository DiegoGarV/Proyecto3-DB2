from dotenv import load_dotenv
from database.driver import driver, close_driver
from data.puzzle_data import rompecabezas_data

load_dotenv()

def cargar_rompecabezas(tx, data):
    # Crear o reutilizar el nodo rompecabezas y guardar en variable `r`
    tx.run("""
        MERGE (r:Rompecabezas {nombre: $nombre})
        SET r.forma = $forma, r.instrucciones = $instrucciones
    """, nombre=data["nombre"], forma=data["forma"], instrucciones=data["instrucciones"])

    # Crear piezas y relacionarlas al mismo nodo `r`
    for pieza in data["piezas"]:
        tx.run("""
            MATCH (r:Rompecabezas {nombre: $nombre})
            MERGE (p:Pieza {id: $id, rompecabezas: $nombre})
            SET p.estado = $estado
            MERGE (p)-[:PERTENECE_A]->(r)
        """, id=pieza["id"], estado=pieza["estado"], nombre=data["nombre"])

    # Crear relaciones CONECTA_CON
    for c in data["conexiones"]:
        tx.run("""
            MATCH (a:Pieza {id: $desde, rompecabezas: $nombre})
            MATCH (b:Pieza {id: $hacia, rompecabezas: $nombre})
            MERGE (a)-[r:CONECTA_CON]->(b)
            SET r.direccion = $direccion,
                r.desde_tipo = $desde_tipo,
                r.hacia_tipo = $hacia_tipo,
                r.entrada = $entrada
        """, nombre=data["nombre"], **c)

def main():
    with driver.session() as session:
        for puzzle in rompecabezas_data:
            session.execute_write(cargar_rompecabezas, puzzle)

    print("¡Rompecabezas cargados correctamente!")
    close_driver()

if __name__ == "__main__":
    main()
