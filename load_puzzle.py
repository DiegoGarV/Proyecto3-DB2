from dotenv import load_dotenv
from database.driver import driver, close_driver
from data.puzzle_data import rompecabezas_data

load_dotenv()
def invertir_direccion(direccion):
    mapa = {
        "Norte": "Sur",
        "Sur": "Norte",
        "Este": "Oeste",
        "Oeste": "Este"
    }
    return mapa.get(direccion, direccion)

def invertir_entrada(entrada):
    mapa = {
        "arriba": "abajo",
        "abajo": "arriba",
        "izquierda": "derecha",
        "derecha": "izquierda"
    }
    return mapa.get(entrada, entrada)
def cargar_rompecabezas(tx, data):
    # Crear o reutilizar el nodo rompecabezas
    tx.run("""
        MERGE (r:Rompecabezas {nombre: $nombre})
        SET r.forma = $forma, r.instrucciones = $instrucciones
    """, nombre=data["nombre"], forma=data["forma"], instrucciones=data["instrucciones"])

    # Crear piezas y vincularlas al rompecabezas
    for pieza in data["piezas"]:
        tx.run("""
            MATCH (r:Rompecabezas {nombre: $nombre})
            MERGE (p:Pieza {id: $id, rompecabezas: $nombre})
            SET p.estado = $estado
            MERGE (p)-[:PERTENECE_A]->(r)
        """, id=pieza["id"], estado=pieza["estado"], nombre=data["nombre"])

    # Crear relaciones CONECTA_CON en ambos sentidos
    for c in data["conexiones"]:
        # Relación directa
        tx.run("""
            MATCH (a:Pieza {id: $desde, rompecabezas: $nombre})
            MATCH (b:Pieza {id: $hacia, rompecabezas: $nombre})
            MERGE (a)-[r:CONECTA_CON]->(b)
            SET r.direccion = $direccion,
                r.desde_tipo = $desde_tipo,
                r.hacia_tipo = $hacia_tipo,
                r.entrada = $entrada
        """, nombre=data["nombre"], **c)

        # Relación inversa
        c_inversa = {
            "desde": c["hacia"],
            "hacia": c["desde"],
            "direccion": invertir_direccion(c["direccion"]),
            "desde_tipo": c["hacia_tipo"],
            "hacia_tipo": c["desde_tipo"],
            "entrada": invertir_entrada(c["entrada"])
        }

        tx.run("""
            MATCH (a:Pieza {id: $desde, rompecabezas: $nombre})
            MATCH (b:Pieza {id: $hacia, rompecabezas: $nombre})
            MERGE (a)-[r:CONECTA_CON]->(b)
            SET r.direccion = $direccion,
                r.desde_tipo = $desde_tipo,
                r.hacia_tipo = $hacia_tipo,
                r.entrada = $entrada
        """, nombre=data["nombre"], **c_inversa)

def main():
    with driver.session() as session:
        for puzzle in rompecabezas_data:
            session.execute_write(cargar_rompecabezas, puzzle)

    print("¡Rompecabezas cargados correctamente!")
    close_driver()

if __name__ == "__main__":
    main()
