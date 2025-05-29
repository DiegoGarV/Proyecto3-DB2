from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import ssl

# Crear contexto SSL inseguro
insecure_ssl_context = ssl.create_default_context()
insecure_ssl_context.check_hostname = False
insecure_ssl_context.verify_mode = ssl.CERT_NONE

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
    ssl_context=insecure_ssl_context  # ✅ Sin `encrypted=True`
)

def close_driver():
    driver.close()
