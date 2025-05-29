from database.driver import driver, close_driver
import os

def ensamblar_rompecabezas(pieza_id, rompecabezas_nombre):
    pieza_id = int(pieza_id)
    rompecabezas_nombre = rompecabezas_nombre.lower()

    with driver.session() as session:
        # Obtener datos del rompecabezas
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

        # Obtener todas las conexiones del rompecabezas
        resultado = session.run("""
            MATCH (a:Pieza)-[r:CONECTA_CON]->(b:Pieza)
            WHERE a.rompecabezas = $nombre AND b.rompecabezas = $nombre
            RETURN a.id AS desde_id, b.id AS hacia_id,
                   r.direccion AS direccion,
                   r.desde_tipo AS desde_tipo,
                   r.hacia_tipo AS hacia_tipo,
                   r.entrada AS entrada
        """, nombre=nombre_rompecabezas)

        conexiones_vistas = set()
        pasos = []
        piezas_usadas = set()

        for record in resultado:
            desde = int(record["desde_id"])
            hacia = int(record["hacia_id"])

            # Evitar duplicar instrucciones por múltiples caminos
            if (desde, hacia) in conexiones_vistas:
                continue
            conexiones_vistas.add((desde, hacia))

            entrada = record["entrada"] or "unica"
            paso = (
                f"Continua colocando la pieza {hacia} al {record['direccion']} "
                f"de la pieza {desde}, conectando del {record['desde_tipo']} "
            )
            if entrada != "unica":
                paso += f"de {entrada} "
            paso += f"del {desde} al {record['hacia_tipo']} del {hacia}"
            pasos.append(paso)

            piezas_usadas.add(hacia)
            piezas_usadas.add(desde)

        # Escribir archivo de instrucciones
        filename = f"instrucciones_{nombre_rompecabezas.lower().replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{instrucciones_generales}\n\n")
            f.write(f"Inicia desde la pieza {pieza_id}\n")
            for paso in pasos:
                f.write(paso + "\n")

        print(f"\n📋 Instrucciones escritas en {filename}")
        close_driver()
        return [pieza_id] + list(piezas_usadas)

def ensamblar_rompe_piezasperdidas(pieza_id, rompecabezas_nombre, piezas_faltantes):
    pieza_id = int(pieza_id)
    rompecabezas_nombre = rompecabezas_nombre.lower()

    with driver.session() as session:
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

        resultado = session.run("""
            MATCH (a:Pieza)-[r:CONECTA_CON]->(b:Pieza)
            WHERE a.rompecabezas = $nombre AND b.rompecabezas = $nombre
            RETURN a.id AS desde_id, b.id AS hacia_id,
                   r.direccion AS direccion,
                   r.desde_tipo AS desde_tipo,
                   r.hacia_tipo AS hacia_tipo,
                   r.entrada AS entrada
        """, nombre=nombre_rompecabezas)

        instrucciones_inicio = [f"Inicia desde la pieza {pieza_id}"]
        instrucciones_otros = []
        conexiones_vistas = set()
        piezas_omitidas = set()
        ensambladas = set()

        for record in resultado:
            desde = int(record["desde_id"])
            hacia = int(record["hacia_id"])

            if (desde, hacia) in conexiones_vistas:
                continue
            conexiones_vistas.add((desde, hacia))

            # Construcción de paso o espacio
            if desde in piezas_faltantes:
                paso = f"Deja un espacio porque acá iría la pieza {desde}"
                piezas_omitidas.add(desde)
            elif hacia in piezas_faltantes:
                paso = f"Deja un espacio porque acá iría la pieza {hacia}"
                piezas_omitidas.add(hacia)
            else:
                entrada = record["entrada"] or "unica"
                paso = (
                    f"Continua colocando la pieza {hacia} al {record['direccion']} "
                    f"de la pieza {desde}, conectando del {record['desde_tipo']} "
                )
                if entrada != "unica":
                    paso += f"de {entrada} "
                paso += f"del {desde} al {record['hacia_tipo']} del {hacia}"
                ensambladas.add(desde)
                ensambladas.add(hacia)

            # Clasificar instrucción
            if desde == pieza_id:
                instrucciones_inicio.append(paso)
            else:
                instrucciones_otros.append(paso)

        # Crear archivo de salida
        filename = f"instrucciones_{nombre_rompecabezas.lower().replace(' ', '_')}_incompleto.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{instrucciones_generales}\n\n")
            for paso in instrucciones_inicio + instrucciones_otros:
                f.write(paso + "\n")

        print(f"\n📋 Instrucciones escritas en {filename}")
        close_driver()

        return list(ensambladas)
