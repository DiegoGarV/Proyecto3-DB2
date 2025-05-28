from database.driver import driver

def ensamblar_rompecabezas(pieza_id: str):
    with driver.session() as session:
        query = """
            MATCH (start:Pieza {id: $pieza_id})-[:CONECTA*]->(p:Pieza)
            RETURN DISTINCT p.id AS id
        """
        result = session.run(query, pieza_id=pieza_id)
        piezas_conectadas = [record["id"] for record in result]
    return piezas_conectadas
