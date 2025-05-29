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
        "nombre": "Rompecabezas Dinosaurio",
        "forma": "Brachiosaurus",
        "instrucciones": "Empieza por la cabeza a la izquierda",
        "piezas": [
            {"id": 1, "estado": True},
            {"id": 2, "estado": True},
            {"id": 3, "estado": True},
            {"id": 4, "estado": True},
            {"id": 5, "estado": True},
            {"id": 6, "estado": True},
            {"id": 7, "estado": True},
            {"id": 8, "estado": True},
            {"id": 9, "estado": True},
            {"id": 10, "estado": True}
            
        ],
        "conexiones": [
            {
                "desde": 1,
                "hacia": 2,
                "direccion": "Sur",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "abajo"
            },
            {
                "desde": 2,
                "hacia": 3,
                "direccion": "Sur",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "abajo"
            },
            {
                "desde": 3,
                "hacia": 4,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 4,
                "hacia": 5,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 4,
                "hacia": 6,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 5,
                "hacia": 6,
                "direccion": "Sur",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "abajo"
            },
            {
                "desde": 5,
                "hacia": 7,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 6,
                "hacia": 8,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 7,
                "hacia": 8,
                "direccion": "Sur",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "abajo"
            },
            {
                "desde": 7,
                "hacia": 9,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 8,
                "hacia": 9,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
            {
                "desde": 9,
                "hacia": 10,
                "direccion": "Este",
                "desde_tipo": "hembra",
                "hacia_tipo": "macho",
                "entrada": "derecha"
            },
        ],
    }
]
