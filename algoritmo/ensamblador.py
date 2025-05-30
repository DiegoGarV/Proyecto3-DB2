from database.driver import driver, close_driver
import os

def ensamblar_rompecabezas(pieza_id, rompecabezas_nombre):
    from collections import deque

    pieza_id = int(pieza_id)
    rompecabezas_nombre = rompecabezas_nombre.lower()

    with driver.session() as session:
        # Obtener info del rompecabezas
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

        # Obtener todas las conexiones
        resultado = session.run("""
            MATCH (a:Pieza)-[r:CONECTA_CON]->(b:Pieza)
            WHERE a.rompecabezas = $nombre AND b.rompecabezas = $nombre
            RETURN a.id AS desde_id, b.id AS hacia_id,
                   r.direccion AS direccion,
                   r.desde_tipo AS desde_tipo,
                   r.hacia_tipo AS hacia_tipo,
                   r.entrada AS entrada
        """, nombre=nombre_rompecabezas)

        # Construir grafo y mapa de relaciones
        grafo = {}
        relaciones_map = {}  # clave: (desde, hacia) → datos

        for record in resultado:
            desde = int(record["desde_id"])
            hacia = int(record["hacia_id"])
            entrada = record["entrada"] or "unica"

            if desde not in grafo:
                grafo[desde] = []
            grafo[desde].append(hacia)

            relaciones_map[(desde, hacia)] = {
                "direccion": record["direccion"],
                "desde_tipo": record["desde_tipo"],
                "hacia_tipo": record["hacia_tipo"],
                "entrada": entrada
            }

        # Recorrer el grafo desde la pieza inicial (BFS)
        visitadas = set()
        ensambladas = []
        instrucciones = [f"Inicia desde la pieza {pieza_id}"]
        cola = deque()
        cola.append(pieza_id)
        visitadas.add(pieza_id)
        ensambladas.append(pieza_id)

        while cola:
            actual = cola.popleft()

            for vecino in grafo.get(actual, []):
                if vecino in visitadas:
                    continue
                visitadas.add(vecino)
                ensambladas.append(vecino)

                rel = relaciones_map.get((actual, vecino))
                if rel:
                    paso = (
                        f"Continua colocando la pieza {vecino} al {rel['direccion']} "
                        f"de la pieza {actual}, conectando del {rel['desde_tipo']} "
                    )
                    if rel["entrada"] != "unica":
                        paso += f"de {rel['entrada']} "
                    paso += f"del {actual} al {rel['hacia_tipo']} del {vecino}"
                    instrucciones.append(paso)

                cola.append(vecino)

        # Guardar instrucciones en archivo
        filename = f"instrucciones_{nombre_rompecabezas.lower().replace(' ', '_')}_desde_{pieza_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{instrucciones_generales}\n\n")
            for paso in instrucciones:
                f.write(paso + "\n")

        print(f"\n📋 Instrucciones escritas en {filename}")
        close_driver()
        return ensambladas


def ensamblar_rompe_piezasperdidas(pieza_id, rompecabezas_nombre, piezas_faltantes):
    pieza_id = int(pieza_id)
    piezas_faltantes = set(map(int, piezas_faltantes))
    rompecabezas_nombre = rompecabezas_nombre.lower()

    with driver.session() as session:
        # Obtener info general
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

        # Obtener relaciones CONECTA_CON del rompecabezas
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
        for record in resultado:
            desde = int(record["desde_id"])
            hacia = int(record["hacia_id"])
            if desde not in grafo:
                grafo[desde] = []
            grafo[desde].append((hacia, record))

        # BFS ampliado
        instrucciones = [f"Inicia desde la pieza {pieza_id}"]
        visitadas = set()
        conexiones_vistas = set()
        ensambladas = set()
        cola = [pieza_id]

        while cola:
            actual = cola.pop(0)
            if actual in visitadas:
                continue
            visitadas.add(actual)

            for hacia, record in grafo.get(actual, []):
                par_directo = (actual, hacia)
                par_inverso = (hacia, actual)
                if par_directo in conexiones_vistas or par_inverso in conexiones_vistas:
                    continue
                conexiones_vistas.add(par_directo)

                entrada = record["entrada"] or "unica"
                detalle_conexion = (
                    f"conectando del {record['desde_tipo']} "
                )
                if entrada != "unica":
                    detalle_conexion += f"de {entrada} "
                detalle_conexion += f"del {actual} al {record['hacia_tipo']} del {hacia}"

                # Piezas faltantes
                if actual in piezas_faltantes:
                    instrucciones.append(
                        f"Deja un espacio porque acá iría la pieza {actual}, {detalle_conexion}"
                    )
                    if hacia not in visitadas:
                        cola.append(hacia)
                    continue

                if hacia in piezas_faltantes:
                    instrucciones.append(
                        f"Deja un espacio porque acá iría la pieza {hacia}, {detalle_conexion}"
                    )
                    if hacia not in visitadas:
                        cola.append(hacia)
                    continue

                # Construcción de paso normal
                paso = (
                    f"Continua colocando la pieza {hacia} al {record['direccion']} "
                    f"de la pieza {actual}, conectando del {record['desde_tipo']} "
                )
                if entrada != "unica":
                    paso += f"de {entrada} "
                paso += f"del {actual} al {record['hacia_tipo']} del {hacia}"

                instrucciones.append(paso)
                ensambladas.add(actual)
                ensambladas.add(hacia)

                if hacia not in visitadas:
                    cola.append(hacia)

        # Escritura en archivo
        filename = f"instrucciones_{nombre_rompecabezas.lower().replace(' ', '_')}_incompleto.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{instrucciones_generales}\n\n")
            for paso in instrucciones:
                f.write(paso + "\n")

        print(f"\n📋 Instrucciones escritas en {filename}")
        close_driver()
        return list(ensambladas)
