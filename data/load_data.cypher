CREATE (:Rompecabezas {id: "r1", nombre: "Animales", dimensiones: "3x3"});
CREATE (p1:Pieza {id: "p_1_1", posicion_x: 1, posicion_y: 1, estado: "presente"});
CREATE (p2:Pieza {id: "p_1_2", posicion_x: 1, posicion_y: 2, estado: "presente"});
CREATE (p1)-[:CONECTA {direccion: "este", slot: 0, tipo: "macho"}]->(p2);
CREATE (p1)-[:PERTENECE_A]->(:Rompecabezas {id: "r1"});
CREATE (p2)-[:PERTENECE_A]->(:Rompecabezas {id: "r1"});
