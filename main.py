import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import db 

app = FastAPI()

# Configuración de archivos (Jinja2 para el HTML y Static para el CSS)
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- RUTA DE REGISTRO ---
@app.post("/registro")
async def registro_usuario(datos: dict):
    try:
        # Verificamos si ya existe el usuario
        existe = await db.usuarios.find_one({"usuario": datos["usuario"]})
        if existe:
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
        await db.usuarios.insert_one(datos)
        return {"message": "¡Registro exitoso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- RUTA DE LOGIN ---
@app.post("/login")
async def login_usuario(credenciales: dict):
    user = await db.usuarios.find_one({
        "usuario": credenciales["usuario"],
        "password": credenciales["password"]
    })
    if user:
        user["_id"] = str(user["_id"])
        return user
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# --- RUTAS DE SOPORTE PARA EL DASHBOARD ---
@app.get("/mis_clases/{usuario}")
async def mis_clases(usuario: str):
    clases = await db.clases.find({"$or": [{"profesor": usuario}, {"alumnos": usuario}]}).to_list(100)
    for c in clases: c["_id"] = str(c["_id"])
    return clases

@app.get("/eventos/{usuario}")
async def mis_eventos(usuario: str):
    evs = await db.eventos.find({"usuario": usuario}).to_list(100)
    for e in evs: e["_id"] = str(e["_id"])
    return evs

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

