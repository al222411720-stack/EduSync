import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. Iniciar App
app = FastAPI()

# 2. Configurar archivos (punto "." porque están sueltos en tu GitHub)
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="."), name="static")

# 3. Ruta de prueba
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 4. Configuración para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
