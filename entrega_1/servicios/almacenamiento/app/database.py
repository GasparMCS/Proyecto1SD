from pymongo import MongoClient
import os
import certifi  # Para manejar certificados SSL

# Construcción de URI con variables de entorno y CA
MONGO_URI = os.getenv(
    "MONGO_URI",
    f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@"
    f"{os.getenv('MONGO_CLUSTER')}/{os.getenv('MONGO_DB', 'eventos')}"
    "?retryWrites=true&w=majority&tls=true&tlsCAFile={}".format(certifi.where())
)

client = MongoClient(
    MONGO_URI,
    connectTimeoutMS=5000,
    socketTimeoutMS=30000,
    serverSelectionTimeoutMS=5000
)

# Selección de base de datos (por defecto: eventos)
db = client.get_database(os.getenv("MONGO_DB", "eventos"))

# Definición explícita de colecciones
events_collection = db["eventos_scrapeados"]
cache_collection = db["cache"]