import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates # <--- ESTA LÍNEA DEBE ESTAR SÍ O SÍ
from database import db

# 1. Inicializar la aplicación
app = FastAPI()

# 2. Configurar archivos (punto "." porque están sueltos en tu GitHub)
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

# 3. Ruta principal
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 4. AQUÍ PEGA TUS RUTAS DE REGISTRO Y LOGIN (Las que ya tenías)
# No borres tus funciones de @app.post("/register") ni @app.post("/login")

# 5. Configuración para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
