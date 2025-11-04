# app/services/vehicles.py

import requests
from app.config import VEHICLES_URL, API_TIMEOUT_SECONDS, USE_HTTPS, DISABLE_SSL_VERIFY

# Desactivar advertencias SSL para Pyodide (web)
if DISABLE_SSL_VERIFY:
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except ImportError:
        pass  # urllib3 no disponible (no es Pyodide)

# Si HTTPS no está disponible, usar HTTP como fallback (solo desarrollo)
if not USE_HTTPS:
    VEHICLES_URL = VEHICLES_URL.replace("https://", "http://")

def get_vehicles(token: str):
    """
    GET Vehiculos con Bearer Token.
    Devuelve:
      { "ok": True, "data": <json> } en éxito
      { "ok": False, "error": "mensaje" } en error
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.get(
            VEHICLES_URL, 
            headers=headers, 
            timeout=API_TIMEOUT_SECONDS,
            verify=not DISABLE_SSL_VERIFY  # Desactivar verificación SSL en Pyodide
        )
    except requests.Timeout:
        return {"ok": False, "error": "Tiempo de espera agotado. El servidor tardó demasiado en responder."}
    except requests.RequestException as ex:
        return {"ok": False, "error": f"Sin conexión ({ex})"}

    # Éxito típico .NET: 200/201
    if resp.status_code in (200, 201):
        try:
            data = resp.json() if resp.content else []
            return {"ok": True, "data": data}
        except Exception as ex:
            return {"ok": False, "error": f"Error al procesar respuesta: {ex}"}

    # Error con cuerpo JSON
    try:
        err = resp.json()
        msg = (
            err.get("message")
            or err.get("Message")
            or err.get("error")
            or err.get("Error")
            or str(err)
        )
    except Exception:
        msg = f"HTTP {resp.status_code}"

    return {"ok": False, "error": msg}

