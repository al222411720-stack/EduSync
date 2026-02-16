import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import db  # Conexión a tu MongoDB

app = FastAPI()

# 1. Configuración de archivos
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

# 2. Ruta principal (Carga el HTML)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 3. RUTA DE REGISTRO (Esto es lo que faltaba)
@app.post("/registro")
async def registro_usuario(datos: dict):
    try:
        # Verificamos si el usuario ya existe para no duplicarlo
        existe = await db.usuarios.find_one({"usuario": datos["usuario"]})
        if existe:
            return {"detail": "El nombre de usuario ya está en uso"}, 400
        
        await db.usuarios.insert_one(datos)
        return {"message": "¡Registro exitoso!"}
    except Exception as e:
        return {"detail": str(e)}, 500

# 4. RUTA DE LOGIN (Esto es lo que causaba el Error de acceso)
@app.post("/login")
async def login_usuario(credenciales: dict):
    user = await db.usuarios.find_one({
        "usuario": credenciales["usuario"],
        "password": credenciales["password"]
    })
    
    if user:
        user["_id"] = str(user["_id"]) # Convertimos el ID de MongoDB a texto
        return user
    else:
        # Si no lo encuentra, mandamos error 401
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# 5. Configuración para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

