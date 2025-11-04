# app/services/locations.py

import requests
from app.config import API_TIMEOUT_SECONDS

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

def get_all_vehicles_locations(token: str, vehicles: list):
    """
    Obtiene las ubicaciones de todos los vehículos.
    Hace llamadas individuales para cada vehículo.
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

