# app/config.py

# URLs de la API - Usar HTTPS para evitar Mixed Content en producción
# Si el servidor no soporta HTTPS, el navegador bloqueará las peticiones desde HTTPS
AUTH_URL = "https://springtelecom.mx/dev/devsionapi/api/Authentication/TokenApp"
VEHICLES_URL = "https://springtelecom.mx/dev/devsionapi/api/Vehiculos"
VEHICLES_LAST_POSITIONS_URL = "https://springtelecom.mx/dev/devsionapi/api/Vehiculo/ultimaVehiculos"
API_TIMEOUT_SECONDS = 15  # Aumentado para evitar timeouts con headers grandes

# Fallback a HTTP si HTTPS no está disponible (solo para desarrollo local)
# En producción, el servidor debe soportar HTTPS
USE_HTTPS = True

# Desactivar verificación SSL para Pyodide (web)
# Pyodide no puede validar certificados como Python normal
# En producción, el servidor debe tener certificados válidos
DISABLE_SSL_VERIFY = True  # Cambiar a False en desarrollo local si es necesario

# Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyDuJ3IBZIs2mRbR4alTg7OZIsk0sXEJHhg"
