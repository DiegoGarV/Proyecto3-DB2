rompecabezas_data = [
    {
        "nombre": "Rompecabezas Rectangular",
        "forma": "Rectangular",
        "instrucciones": "Armar de izquierda a derecha",
        "piezas": [
            {"id": 1, "estado": True},
            {"id": 2, "estado": True},
            {"id": 3, "estado": False},
        ],
        "conexiones": [
            {
                "desde": 1,
                "hacia": 2,
                "direccion": "Este",
                "desde_tipo": "macho",
                "hacia_tipo": "hembra",
                "entrada": "unica"
            },
            {
                "desde": 2,
                "hacia": 3,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "unica"
            },
            {
                "desde": 2,
                "hacia": 1,
                "direccion": "Oeste",
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
                "direccion": "Oeste",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "arriba"
            },
            {
                "desde": 1,
                "hacia": 3,
                "direccion": "Oeste",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "abajo"
            },
        ],
    },
    {
        "nombre": "Aviones Puzzle",
        "forma": "Rectangular",
        "instrucciones": "Empieza por la oreja derecha",
        "piezas": [
            {"id": 1},
            {"id": 2},
            {"id": 3},
            {"id": 4},
            {"id": 5},
            {"id": 6},
            {"id": 7},
            {"id": 8},
            {"id": 9},
            {"id": 10},
            {"id": 11},
            {"id": 12},
            {"id": 13},
            {"id": 14},
            {"id": 15},
            {"id": 16},
            {"id": 17},
            {"id": 18},
            {"id": 19},
            {"id": 20},
            {"id": 21},
            {"id": 22},
            {"id": 23},
            {"id": 24},
        ],
        "conexiones": [
            {
                "desde": 1,
                "hacia": 2,
                "direccion": "Este",
                "desde_tipo": "macho",
                "hacia_tipo": "hembra",
                "entrada": "derecha"
            },
            {
                "desde": 2,
                "hacia": 3,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 2,
                "hacia": 3,
                "direccion": "Oeste",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
        ],
    },
]
