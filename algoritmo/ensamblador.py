from database.driver import driver, close_driver
import os

def ensamblar_rompecabezas(pieza_id, rompecabezas_nombre):
    pieza_id = int(pieza_id)
    rompecabezas_nombre = rompecabezas_nombre.lower()

    with driver.session() as session:
        # Buscar el nodo del rompecabezas (ignorando mayúsculas)
        rompecabezas = session.run("""
            MATCH (r:Rompecabezas)
            WHERE toLower(r.nombre) = $nombre
            RETURN r.instrucciones AS instrucciones, r.nombre AS nombre
        """, nombre=rompecabezas_nombre).single()

        if not rompecabezas:
            print("Rompecabezas no encontrado.")
            return []

        instrucciones = rompecabezas["instrucciones"]
        nombre_rompecabezas = rompecabezas["nombre"]

        # Buscar las piezas conectadas desde la inicial
        resultado = session.run("""
            MATCH path = (inicio:Pieza {id: $pieza_id, rompecabezas: $nombre})-[:CONECTA_CON*]->(p:Pieza)
            WITH nodes(path) AS piezas, relationships(path) AS relaciones
            RETURN piezas, relaciones
        """, pieza_id=pieza_id, nombre=nombre_rompecabezas)

        pasos = []
        piezas_usadas = set()
        for record in resultado:
            piezas = record["piezas"]
            relaciones = record["relaciones"]

            if not piezas or not relaciones:
                continue

            piezas_ids = [pieza["id"] for pieza in piezas]
            for i in range(1, len(piezas)):
                anterior = piezas[i - 1]
                actual = piezas[i]
                conexion = relaciones[i - 1]

                if actual["id"] in piezas_usadas:
                    continue
                piezas_usadas.add(actual["id"])

                entrada = conexion.get("entrada", "unica")
                paso = (
                    f"Continua colocando la pieza {actual['id']} al {conexion['direccion']} "
                    f"de la pieza {anterior['id']}, conectando del {conexion['desde_tipo']} "
                )
                if entrada != "unica":
                    paso += f"de {entrada} "
                paso += f"del {anterior['id']} al {conexion['hacia_tipo']} del {actual['id']}"
                pasos.append(paso)

        # Escribir archivo de instrucciones
        filename = f"instrucciones_{nombre_rompecabezas.lower().replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{instrucciones}\n\n")
            f.write(f"Inicia desde la pieza {pieza_id}\n")
            for paso in pasos:
                f.write(paso + "\n")

        print(f"Instrucciones escritas en {filename}")
        close_driver()
        return [pieza_id] + list(piezas_usadas)

