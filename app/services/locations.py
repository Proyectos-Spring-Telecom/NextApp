# app/services/locations.py

import requests
from app.config import API_TIMEOUT_SECONDS, VEHICLES_LAST_POSITIONS_URL, USE_HTTPS, DISABLE_SSL_VERIFY

def get_vehicle_location(token: str, vehicle_id: int = None, imei: int = None):
    """
    Obtiene la ubicación actual de un vehículo.
    Puede buscar por vehicle_id o por imei.
    
    Devuelve:
      { "ok": True, "data": { "lat": float, "lon": float, ... } } en éxito
      { "ok": False, "error": "mensaje" } en error
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Intentar diferentes endpoints posibles
    # Usar HTTPS para evitar Mixed Content
    from app.config import USE_HTTPS, DISABLE_SSL_VERIFY
    
    # Desactivar advertencias SSL para Pyodide (web)
    if DISABLE_SSL_VERIFY:
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except ImportError:
            pass  # urllib3 no disponible (no es Pyodide)
    
    protocol = "https" if USE_HTTPS else "http"
    base_url = f"{protocol}://springtelecom.mx/dev/devsionapi/api"
    
    endpoints_to_try = []
    
    if vehicle_id:
        endpoints_to_try.extend([
            f"{base_url}/Vehiculos/{vehicle_id}/Ubicacion",
            f"{base_url}/Vehiculos/{vehicle_id}/Location",
            f"{base_url}/Ubicaciones/{vehicle_id}",
        ])
    
    if imei:
        endpoints_to_try.extend([
            f"{base_url}/Ubicaciones?imei={imei}",
            f"{base_url}/Ubicaciones?IMEI={imei}",
            f"{base_url}/Vehiculos/Ubicacion?imei={imei}",
        ])
    
    # Intentar cada endpoint
    for url in endpoints_to_try:
        try:
            resp = requests.get(
                url, 
                headers=headers, 
                timeout=API_TIMEOUT_SECONDS,
                verify=not DISABLE_SSL_VERIFY  # Desactivar verificación SSL en Pyodide
            )
            if resp.status_code in (200, 201):
                try:
                    data = resp.json() if resp.content else {}
                    return {"ok": True, "data": data, "endpoint": url}
                except Exception:
                    continue
        except requests.Timeout:
            continue  # Continuar con el siguiente endpoint si hay timeout
        except requests.RequestException:
            continue
    
    return {"ok": False, "error": "No se encontró endpoint de ubicaciones disponible"}

def get_last_vehicles_positions(token: str):
    """
    Obtiene las últimas posiciones de todos los vehículos usando el endpoint específico.
    Este endpoint es más eficiente que hacer llamadas individuales.
    
    Devuelve:
      { "ok": True, "data": <lista de vehículos con posiciones> } en éxito
      { "ok": False, "error": "mensaje" } en error
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Desactivar advertencias SSL para Pyodide (web)
    if DISABLE_SSL_VERIFY:
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except ImportError:
            pass  # urllib3 no disponible (no es Pyodide)
    
    # Si HTTPS no está disponible, usar HTTP como fallback (solo desarrollo)
    url = VEHICLES_LAST_POSITIONS_URL
    if not USE_HTTPS:
        url = url.replace("https://", "http://")
    
    try:
        resp = requests.get(
            url, 
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

def get_all_vehicles_locations(token: str, vehicles: list):
    """
    Obtiene las ubicaciones de todos los vehículos.
    Hace llamadas individuales para cada vehículo.
    NOTA: Esta función está deprecada en favor de get_last_vehicles_positions()
    que es más eficiente.
    """
    locations = {}
    
    for vehicle in vehicles:
        vehicle_id = vehicle.get("id")
        imei = vehicle.get("imei")
        
        if vehicle_id or imei:
            location_result = get_vehicle_location(token, vehicle_id=vehicle_id, imei=imei)
            if location_result.get("ok"):
                locations[vehicle.get("id", imei)] = location_result.get("data", {})
    
    return locations

