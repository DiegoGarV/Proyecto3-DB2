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

def ensamblar_rompe_piezasperdidas(pieza_id, rompecabezas_nombre, piezas_faltantes):
    pieza_id = int(pieza_id)
    rompecabezas_nombre = rompecabezas_nombre.lower()

    with driver.session() as session:
        # Obtener datos generales
        rompecabezas = session.run("""
            MATCH (r:Rompecabezas)
            WHERE toLower(r.nombre) = $nombre
            RETURN r.instrucciones AS instrucciones, r.nombre AS nombre
        """, nombre=rompecabezas_nombre).single()

        if not rompecabezas:
            print("❌ Rompecabezas no encontrado.")
            return []

        instrucciones_generales = rompecabezas["instrucciones"]
        nombre_rompecabezas = rompecabezas["nombre"]

        # Obtener TODAS las conexiones entre piezas del rompecabezas
        resultado = session.run("""
            MATCH (a:Pieza)-[r:CONECTA_CON]->(b:Pieza)
            WHERE a.rompecabezas = $nombre AND b.rompecabezas = $nombre
            RETURN a.id AS desde_id, b.id AS hacia_id,
                   r.direccion AS direccion,
                   r.desde_tipo AS desde_tipo,
                   r.hacia_tipo AS hacia_tipo,
                   r.entrada AS entrada
        """, nombre=nombre_rompecabezas)

        # Construcción del grafo
        grafo = {}
        relaciones = []
        for record in resultado:
            desde = int(record["desde_id"])
            hacia = int(record["hacia_id"])
            relaciones.append(record)
            if desde not in grafo:
                grafo[desde] = []
            grafo[desde].append(hacia)

        # Ensamblaje por recorrido BFS desde la pieza inicial
        ensambladas = []
        piezas_omitidas = set()
        instrucciones = []

        visitadas = set()
        cola = [pieza_id]

        instrucciones.append(f"Inicia desde la pieza {pieza_id}")

        while cola:
            actual = cola.pop(0)
            if actual in visitadas:
                continue
            visitadas.add(actual)

            if actual in piezas_faltantes:
                instrucciones.append(f"Deja un espacio porque acá iría la pieza {actual}")
                piezas_omitidas.add(actual)
                continue
            else:
                ensambladas.append(actual)

            for r in relaciones:
                if int(r["desde_id"]) != actual:
                    continue

                siguiente = int(r["hacia_id"])
                entrada = r["entrada"] or "unica"
                if siguiente in piezas_faltantes:
                    instrucciones.append(f"Deja un espacio porque acá iría la pieza {siguiente}")
                    piezas_omitidas.add(siguiente)
                elif siguiente not in visitadas:
                    paso = (
                        f"Continua colocando la pieza {siguiente} al {r['direccion']} "
                        f"de la pieza {actual}, conectando del {r['desde_tipo']} "
                    )
                    if entrada != "unica":
                        paso += f"de {entrada} "
                    paso += f"del {actual} al {r['hacia_tipo']} del {siguiente}"
                    instrucciones.append(paso)
                    cola.append(siguiente)

        # Escribir archivo .txt
        filename = f"instrucciones_{nombre_rompecabezas.lower().replace(' ', '_')}_incompleto.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{instrucciones_generales}\n\n")
            for paso in instrucciones:
                f.write(paso + "\n")

        print(f"\n📋 Instrucciones escritas en {filename}")
        close_driver()

        return ensambladas
