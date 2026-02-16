import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles      # <--- REVISA QUE ESTA LÍNEA ESTÉ
from fastapi.templating import Jinja2Templates  # <--- Y ESTA TAMBIÉN
from database import db

app = FastAPI()

# Configuración para archivos sueltos en la raíz
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- AQUÍ PEGA TU CÓDIGO DE LOGIN Y REGISTRO ---
# (Asegúrate de no dejar líneas repetidas de "app = FastAPI()")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
