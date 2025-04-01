from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Primera llamada: GET /status
@app.get("/status")
async def get_status():
    # Simula un sistema dañado aleatorio
    
    return {"damaged_system": "engines"}

# Segunda llamada: GET /repair-bay
@app.get("/repair-bay", response_class=HTMLResponse)
async def get_repair_bay():

    html_content = f"""
    <div class="anchor-point">"ENG-04"</div>
    """
    
    return HTMLResponse(content=html_content)


# Tercera llamada: POST /teapot
@app.post("/teapot")
async def teapot():
    raise HTTPException(status_code=418, detail="I'm a teapot")

# Para correr el servidor, se ejecuta:
# uvicorn app:app --reload
