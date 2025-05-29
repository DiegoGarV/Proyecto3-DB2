rompecabezas_data = [
    {
        "nombre": "Rompecabezas Rectangular",
        "forma": "Rectangular",
        "instrucciones": "Armar de izquierda a derecha",
        "piezas": [
            {"id": 1, "estado": True},
            {"id": 2, "estado": True},
            {"id": 3, "estado": False},  # pieza faltante
        ],
        "conexiones": [
            {
                "desde": 1,
                "hacia": 2,
                "direccion": "E",
                "desde_tipo": "macho",
                "hacia_tipo": "hembra",
                "entrada": "unica"
            },
            {
                "desde": 2,
                "hacia": 3,
                "direccion": "E",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "unica"
            },
        ],
    },
    {
        "nombre": "Rompecabezas Zorros",
        "forma": "Contorno de familia de zorros",
        "instrucciones": "Empieza por la oreja izquierda",
        "piezas": [
            {"id": 1, "estado": True},
            {"id": 2, "estado": True},
            {"id": 3, "estado": True},
        ],
        "conexiones": [
            {
                "desde": 1,
                "hacia": 2,
                "direccion": "O_arriba",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "arriba"
            },
            {
                "desde": 1,
                "hacia": 3,
                "direccion": "O_abajo",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "abajo"
            },
        ],
    }
]
