from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException, Query
import math
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

# --- Define the known points from the diagram ---
P1 = 0.05  # MPa
V1_LIQUID = 0.00105 # m^3/kg
V1_VAPOR = 30.00    # m^3/kg

P2 = 10.0   # MPa (Critical Pressure)
V2_LIQUID = 0.0035  # m^3/kg (Critical Volume)
V2_VAPOR = 0.0035   # m^3/kg (Critical Volume)

# --- Pre-calculate slopes and intercepts for the linear equations ---
delta_p = P2 - P1
if delta_p == 0:
     raise ValueError("P1 and P2 cannot be the same.")

# Liquid line: v = m_liquid * P + c_liquid
m_liquid = (V2_LIQUID - V1_LIQUID) / delta_p # Slope
c_liquid = V1_LIQUID - m_liquid * P1

# Vapor line: v = m_vapor * P + c_vapor
m_vapor = (V2_VAPOR - V1_VAPOR) / delta_p # Slope
# Note: The vapor line is not a straight line in reality, but for the sake of this
# calculation, we are using a linear approximation.
# This is a simplification for the purpose of this example.
# The intercept is calculated similarly to the liquid line.
c_vapor = V1_VAPOR - m_vapor * P1

@app.get("/phase-change-diagram")
async def get_phase_change_data(
    pressure: float = Query(..., gt=0, description="Pressure in mega pascals (MPa)")
):
    """
    Calculates the specific volume for saturated liquid and saturated vapor
    using linear equations derived from the P1(0.05 MPa) and P2(10 MPa) points.
    The calculation uses interpolation/extrapolation for ANY positive input pressure.
    """

    # --- Direct Calculation using linear equations ---
    # v = mP + c
    specific_volume_liquid = m_liquid * pressure + c_liquid
    specific_volume_vapor = m_vapor * pressure + c_vapor

    # Ensure non-negative volumes (safety check, especially for extrapolation)
    specific_volume_liquid = max(0, specific_volume_liquid)
    specific_volume_vapor = max(0, specific_volume_vapor)

    # --- Response ---
    return {
        "specific_volume_liquid": round(specific_volume_liquid, 6),
        "specific_volume_vapor": round(specific_volume_vapor, 6)
    }
