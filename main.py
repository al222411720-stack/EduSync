import random, string
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from database import db
from datetime import datetime
from bson import ObjectId

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- MODELOS ---
class User(BaseModel):
    nombre: str; usuario: str; password: str; rol: str
    matricula: str; escuela: str; correo: EmailStr; foto: str = "https://cdn-icons-png.flaticon.com/512/149/149071.png"

class ProfileUpdate(BaseModel):
    usuario: str; nombre: str; foto: str

class Evento(BaseModel):
    usuario: str; titulo: str; fecha: str; tipo: str; categoria: str

class Clase(BaseModel):
    nombre_clase: str; profesor_id: str; codigo: str = ""; alumnos: list = []

class Publicacion(BaseModel):
    clase_id: str; autor: str; contenido: str; tipo: str; archivo: str = ""; fecha: str = datetime.now().strftime("%d %b, %H:%M")

class Comentario(BaseModel):
    publicacion_id: str; autor: str; texto: str; fecha: str = datetime.now().strftime("%d %b, %H:%M")

class Mensaje(BaseModel):
    clase_id: str; usuario: str; texto: str; hora: str = datetime.now().strftime("%H:%M")

class GrupoPrivado(BaseModel):
    nombre: str; creador: str; codigo: str = ""; miembros: list = []

class ArchivoGrupo(BaseModel):
    grupo_id: str; usuario: str; nombre_archivo: str; fecha: str = datetime.now().strftime("%d %b, %H:%M")

class MensajeGrupo(BaseModel):
    grupo_id: str; usuario: str; texto: str; hora: str = datetime.now().strftime("%H:%M")

# --- RUTAS DE USUARIOS ---
@app.post("/registro")
async def registro(user: User):
    m_existe = await db.usuarios.find_one({"matricula": user.matricula})
    if m_existe: raise HTTPException(status_code=400, detail="La matrícula ya está registrada.")
    u_existe = await db.usuarios.find_one({"usuario": user.usuario})
    if u_existe: raise HTTPException(status_code=400, detail="El nombre de usuario ya existe.")
    await db.usuarios.insert_one(user.dict()); return {"msg": "ok"}

@app.post("/login")
async def login(credentials: dict):
    u = await db.usuarios.find_one({"usuario": credentials['usuario'], "password": credentials['password']})
    if u: return {**u, "_id": str(u["_id"])}
    raise HTTPException(status_code=401)

@app.put("/actualizar_perfil")
async def actualizar_perfil(upd: ProfileUpdate):
    res = await db.usuarios.update_one({"usuario": upd.usuario}, {"$set": {"nombre": upd.nombre, "foto": upd.foto}})
    if res.modified_count: return {"msg": "Perfil actualizado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- RUTAS DE CLASES, GRUPOS Y AGENDA (IGUALES) ---
@app.post("/crear_clase")
async def crear_clase(clase: Clase):
    clase.codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    await db.clases.insert_one(clase.dict()); return {"codigo": clase.codigo}

@app.post("/unirse_clase")
async def unirse_clase(data: dict):
    await db.clases.update_one({"codigo": data['codigo'].upper()}, {"$addToSet": {"alumnos": data['usuario']}})
    return {"msg": "ok"}

@app.get("/mis_clases/{usuario}")
async def mis_clases(usuario: str):
    cursor = db.clases.find({"$or": [{"profesor_id": usuario}, {"alumnos": usuario}]})
    res = await cursor.to_list(length=100); return [{**c, "_id": str(c["_id"])} for c in res]

@app.post("/publicar")
async def publicar(pub: Publicacion):
    await db.publicaciones.insert_one(pub.dict()); return {"msg": "ok"}

@app.get("/publicaciones/{clase_id}")
async def obtener_publicaciones(clase_id: str):
    cursor = db.publicaciones.find({"clase_id": clase_id})
    res = await cursor.to_list(length=100); return [{**p, "_id": str(p["_id"])} for p in res]

@app.post("/comentar")
async def comentar(com: Comentario):
    await db.comentarios.insert_one(com.dict()); return {"msg": "ok"}

@app.get("/comentarios/{publicacion_id}")
async def obtener_comentarios(publicacion_id: str):
    cursor = db.comentarios.find({"publicacion_id": publicacion_id})
    res = await cursor.to_list(length=100); return [{**c, "_id": str(c["_id"])} for c in res]

@app.post("/enviar_mensaje")
async def enviar_mensaje(msg: Mensaje):
    await db.chats.insert_one(msg.dict()); return {"msg": "ok"}

@app.get("/obtener_chat/{clase_id}")
async def obtener_chat(clase_id: str):
    cursor = db.chats.find({"clase_id": clase_id})
    res = await cursor.to_list(length=50); return [{**m, "_id": str(m["_id"])} for m in res]

@app.post("/crear_grupo")
async def crear_grupo(g: GrupoPrivado):
    g.codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    g.miembros = [g.creador]
    await db.grupos_privados.insert_one(g.dict()); return {"codigo": g.codigo}

@app.post("/unirse_grupo")
async def unirse_grupo(data: dict):
    await db.grupos_privados.update_one({"codigo": data['codigo'].upper()}, {"$addToSet": {"miembros": data['usuario']}})
    return {"msg": "ok"}

@app.get("/mis_grupos/{usuario}")
async def mis_grupos(usuario: str):
    cursor = db.grupos_privados.find({"miembros": usuario})
    res = await cursor.to_list(length=100); return [{**g, "_id": str(g["_id"])} for g in res]

@app.post("/subir_archivo_grupo")
async def subir_archivo_grupo(arc: ArchivoGrupo):
    await db.archivos_grupos.insert_one(arc.dict()); return {"msg": "ok"}

@app.get("/archivos_grupo/{grupo_id}")
async def obtener_archivos_grupo(grupo_id: str):
    cursor = db.archivos_grupos.find({"grupo_id": grupo_id})
    res = await cursor.to_list(length=100); return [{**a, "_id": str(a["_id"])} for a in res]

@app.post("/enviar_mensaje_grupo")
async def enviar_mensaje_grupo(msg: MensajeGrupo):
    await db.chats_grupos.insert_one(msg.dict()); return {"msg": "ok"}

@app.get("/obtener_chat_grupo/{grupo_id}")
async def obtener_chat_grupo(grupo_id: str):
    cursor = db.chats_grupos.find({"grupo_id": grupo_id})
    res = await cursor.to_list(length=50); return [{**m, "_id": str(m["_id"])} for m in res]

@app.post("/eventos")
async def guardar_evento(evento: Evento):
    await db.calendario.insert_one(evento.dict()); return {"msg": "ok"}

@app.get("/eventos/{usuario}")
async def obtener_eventos(usuario: str):
    cursor = db.calendario.find({"usuario": usuario}).sort("fecha", 1)
    res = await cursor.to_list(length=100); return [{**e, "_id": str(e["_id"])} for e in res]
if __name__ == "__main__":
    import uvicorn
    import os
    # Esto permite que Render elija el puerto automáticamente
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    # Cambia esto en main.py:
templates = Jinja2Templates(directory=".") # Antes decía "templates"
app.mount("/static", StaticFiles(directory="."), name="static") # Antes decía "static"
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates  # <--- ESTA ES LA QUE FALTABA
from database import db
import os
import uvicorn

app = FastAPI()

# Configuramos para archivos sueltos en la raíz
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- AQUÍ VAN TUS DEMÁS RUTAS (Login, Registro, etc.) ---
# Asegúrate de copiar el resto de tu código aquí abajo

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)