from motor.motor_asyncio import AsyncIOMotorClient
import certifi
import sys

# =================================================================
# CONFIGURACIÓN FINAL - EDUSYNC PRO
# =================================================================

# Tu enlace definitivo con las credenciales de la imagen image_97c32e.png
uri = "mongodb+srv://admin:12345Aa@cluster0.l7n1ory.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    # Conexión asíncrona usando certifi para evitar bloqueos en Windows
    client = AsyncIOMotorClient(uri, tlsCAFile=certifi.where())
    
    # Nombre de tu base de datos
    db = client.edusync_db
    
    print("🚀 ¡Conexión exitosa a la nueva base de datos MongoDB Atlas!")

except Exception as e:
    print(f"🛑 Error crítico al conectar a MongoDB: {e}")
    sys.exit(1)