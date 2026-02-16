import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates # <--- ESTA ES LA LÍNEA CLAVE
from database import db

app = FastAPI()

# Configuramos para buscar archivos en la raíz del proyecto
# Esto es porque en tu GitHub están todos los archivos sueltos
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- AQUÍ ABAJO SIGUE TU CÓDIGO DE LOGIN Y REGISTRO ---
# Asegúrate de no borrar tus rutas de @app.post("/register"), etc.

if __name__ == "__main__":
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)