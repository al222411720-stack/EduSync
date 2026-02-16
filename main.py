import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# --- IMPORTANTE: Añade esta línea para conectar con tu database.py ---
from database import db 

# 1. Iniciar App
app = FastAPI()

# 2. Configurar archivos
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

# 3. Ruta principal
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 4. Ruta de registro (Ya corregida para recibir los datos de tu JS)
@app.post("/registro")
async def registro_usuario(datos: dict):
    try:
        # Aquí insertamos los datos en tu colección de MongoDB
        await db.usuarios.insert_one(datos)
        return {"message": "Usuario registrado con éxito"}
    except Exception as e:
        return {"error": str(e)}

# 5. Configuración para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
