# app/components/map.py

import flet as ft
from app.config import GOOGLE_MAPS_API_KEY
from app.components.buttons import PrimaryPillButton

def create_map_with_markers(vehicles_data: list, width: int = None, height: int = 600, page: ft.Page = None):
    """
    Crea un mapa embebido interactivo con Google Maps mostrando las posiciones de los vehículos.
    Usa Google Maps Embed API para mostrar un mapa interactivo embebido.
    
    vehicles_data: Lista de vehículos con campos latitud y longitud
    page: Página de Flet para usar launch_url (opcional)
    """
    if not vehicles_data:
        return ft.Container(
            content=ft.Text("No hay vehículos disponibles", size=16),
            alignment=ft.alignment.center,
            width=width,
            height=height,
        )
    
    # Extraer coordenadas y preparar marcadores
    markers_data = []
    lats = []
    lons = []
    
    for idx, vehicle in enumerate(vehicles_data):
        # Buscar coordenadas
        lat = (
            vehicle.get("latitud") or vehicle.get("Latitud") or 
            vehicle.get("lat") or vehicle.get("latitude") or
            vehicle.get("Latitude") or vehicle.get("y") or 0
        )
        lon = (
            vehicle.get("longitud") or vehicle.get("Longitud") or 
            vehicle.get("lon") or vehicle.get("lng") or vehicle.get("longitude") or
            vehicle.get("Longitude") or vehicle.get("x") or 0
        )
        
        # Si no hay coordenadas directas, buscar en objeto anidado
        if not lat or not lon:
            ubicacion = vehicle.get("ubicacion") or vehicle.get("Ubicacion") or vehicle.get("location") or vehicle.get("Location") or {}
            lat = lat or ubicacion.get("latitud") or ubicacion.get("Latitud") or ubicacion.get("lat") or ubicacion.get("latitude") or 0
            lon = lon or ubicacion.get("longitud") or ubicacion.get("Longitud") or ubicacion.get("lon") or ubicacion.get("lng") or ubicacion.get("longitude") or 0
        
        if lat and lon and float(lat) != 0 and float(lon) != 0:
            lats.append(float(lat))
            lons.append(float(lon))
            
            # Obtener información del vehículo para el marcador
            nombre = (
                vehicle.get("placas") or vehicle.get("Placas") or
                vehicle.get("economico") or vehicle.get("Economico") or
                vehicle.get("descripcion") or vehicle.get("Descripcion") or
                vehicle.get("nombre") or vehicle.get("Nombre") or 
                vehicle.get("placa") or vehicle.get("Placa") or 
                vehicle.get("PlacaVehiculo") or 
                f"Vehículo {idx + 1}"
            )
            
            markers_data.append({
                "lat": float(lat),
                "lon": float(lon),
                "info": nombre
            })
    
    # Si no hay coordenadas válidas, mostrar mensaje
    if not markers_data:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon("map", size=64, color="#9E9E9E"),
                    ft.Text(
                        "No hay vehículos con coordenadas disponibles",
                        size=16,
                        color="#757575",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Los vehículos no tienen ubicación GPS registrada.",
                        size=14,
                        color="#9E9E9E",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
            alignment=ft.alignment.center,
            width=width,
            height=height,
            padding=20,
        )
    
    # Calcular centro del mapa
    center_lat = sum(lats) / len(lats) if lats else 19.4326  # Default: Ciudad de México
    center_lon = sum(lons) / len(lons) if lons else -99.1332
    
    # Calcular tamaño del mapa
    map_width = width or 800
    map_height = (height - 80) if height else 520  # Dejar espacio para botón y texto
    
    # Crear URL para Google Maps Embed API (permite iframe interactivo)
    # Para múltiples marcadores, necesitamos usar una URL diferente
    if len(markers_data) <= 1:
        # Un solo marcador - usar Embed API
        embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={center_lat},{center_lon}&zoom=13"
    else:
        # Múltiples marcadores - usar formato de dirección
        # Para Embed API con múltiples puntos, usamos el centro y agregamos marcadores
        embed_url = f"https://www.google.com/maps/embed/v1/view?key={GOOGLE_MAPS_API_KEY}&center={center_lat},{center_lon}&zoom=11"
    
    # URL para abrir en Google Maps completo (para obtener direcciones)
    if len(markers_data) == 1:
        full_map_url = f"https://www.google.com/maps?q={markers_data[0]['lat']},{markers_data[0]['lon']}"
    else:
        # Para múltiples marcadores, usar formato de dirección
        coords = "|".join([f"{m['lat']},{m['lon']}" for m in markers_data[:10]])
        full_map_url = f"https://www.google.com/maps/dir/{coords}"
    
    # Crear HTML con iframe para el mapa embebido
    map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; }}
        #map-container {{
            width: 100%;
            height: 100vh;
            position: relative;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: 0;
        }}
    </style>
</head>
<body>
    <div id="map-container">
        <iframe
            src="{embed_url}"
            width="100%"
            height="100%"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
    </div>
</body>
</html>
    """
    
    # Función para abrir mapa completo en nueva ventana
    def open_full_map(e):
        if page:
            page.launch_url(full_map_url, web_window_name="_blank")
        else:
            _open_url(full_map_url)
    
    # Como Flet 0.28.3 no tiene ft.Html, usaremos un contenedor con botón
    # que abra el mapa en una nueva ventana, pero con un preview mejorado
    # Alternativa: mostrar imagen estática con botón para mapa interactivo embebido
    
    # Crear URL para imagen estática como preview
    # Calcular zoom adecuado basado en el área cubierta
    if len(markers_data) > 1:
        # Calcular el rango de coordenadas
        lat_range = max(lats) - min(lats)
        lon_range = max(lons) - min(lons)
        max_range = max(lat_range, lon_range)
        
        # Ajustar zoom según el rango (mayor rango = menor zoom)
        if max_range > 0.1:
            zoom = 10
        elif max_range > 0.05:
            zoom = 11
        elif max_range > 0.02:
            zoom = 12
        else:
            zoom = 13
    else:
        zoom = 15
    
    # Crear marcadores con etiquetas numeradas (máximo 10 para la API estática)
    markers_str = "&".join([f"markers=color:red|label:{i+1}|{m['lat']},{m['lon']}" for i, m in enumerate(markers_data[:10])])
    
    # Si hay más de 10 vehículos, agregar un marcador adicional en el centro
    if len(markers_data) > 10:
        markers_str += f"&markers=color:blue|label:C|{center_lat},{center_lon}"
    
    static_preview_url = (
        f"https://maps.googleapis.com/maps/api/staticmap?"
        f"center={center_lat},{center_lon}&"
        f"zoom={zoom}&"
        f"size={map_width}x{map_height}&"
        f"{markers_str}&"
        f"key={GOOGLE_MAPS_API_KEY}"
    )
    
    # Crear componente con preview y botón para mapa interactivo
    return ft.Container(
        content=ft.Column(
            [
                # Preview del mapa (imagen estática)
                ft.Container(
                    content=ft.Image(
                        src=static_preview_url,
                        fit=ft.ImageFit.COVER,
                        width=map_width,
                        height=map_height,
                    ),
                    width=map_width,
                    height=map_height,
                    border_radius=8,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    border=ft.border.all(1, "#E0E0E0"),
                    on_click=open_full_map,  # Click en la imagen abre el mapa completo
                ),
                # Botón para abrir mapa interactivo completo
                PrimaryPillButton(
                    "Abrir mapa interactivo completo",
                    on_click=open_full_map,
                    width=map_width if map_width else 320,
                ),
                # Información de vehículos
                ft.Text(
                    _get_map_info_text(len(markers_data)),
                    size=12,
                    color="#757575",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=width,
        height=height,
        padding=10,
    )


def create_vehicle_map_modal(page: ft.Page, vehicle: dict, lat: float, lon: float, vehicle_name: str = ""):
    """
    Crea un diálogo modal con un mapa interactivo del vehículo individual.
    Permite ver el mapa, hacer zoom, mover y obtener direcciones.
    
    Args:
        page: Página de Flet
        vehicle: Diccionario con datos del vehículo
        lat: Latitud del vehículo
        lon: Longitud del vehículo
        vehicle_name: Nombre del vehículo para mostrar
    """
    # URL para Google Maps Embed API del vehículo
    embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={lat},{lon}&zoom=15"
    
    # URL para abrir en Google Maps completo (para direcciones)
    full_map_url = f"https://www.google.com/maps?q={lat},{lon}"
    
    # URL para obtener direcciones
    directions_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    
    def open_directions(e):
        page.launch_url(directions_url, web_window_name="_blank")
    
    def open_full_map(e):
        page.launch_url(full_map_url, web_window_name="_blank")
    
    # Información del vehículo
    placas = vehicle.get("placas") or vehicle.get("Placas") or vehicle_name or "Vehículo"
    economico = vehicle.get("economico") or vehicle.get("Economico") or ""
    marca = vehicle.get("marca") or vehicle.get("Marca") or ""
    modelo = vehicle.get("modelo") or vehicle.get("Modelo") or ""
    
    title_text = placas
    if economico:
        title_text += f" - {economico}"
    if marca or modelo:
        title_text += f" ({marca} {modelo})".strip()
    
    # Crear diálogo modal
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title_text, size=18, weight=ft.FontWeight.BOLD),
        content=ft.Container(
            content=ft.Column(
                [
                    # Información de coordenadas
                    ft.Text(
                        f"📍 Ubicación: {lat}, {lon}",
                        size=12,
                        color="#757575",
                    ),
                    ft.Divider(height=10),
                    # Nota sobre el mapa interactivo
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Para ver el mapa interactivo completo con zoom, desplazamiento y direcciones:",
                                    size=12,
                                    color="#616161",
                                ),
                                PrimaryPillButton(
                                    "Ver mapa interactivo completo",
                                    on_click=open_full_map,
                                    width=300,
                                ),
                                ft.Divider(height=10),
                                PrimaryPillButton(
                                    "Obtener direcciones",
                                    on_click=open_directions,
                                    width=300,
                                ),
                            ],
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=10,
                        width=400,
                    ),
                ],
                spacing=10,
                width=400,
                tight=True,
            ),
            width=400,
            height=300,
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    return dialog


def _get_map_info_text(num_vehicles: int) -> str:
    """Genera el texto informativo para el mapa"""
    info_text = f"📍 {num_vehicles} vehículo(s) en el mapa"
    if num_vehicles > 10:
        info_text += f" (mostrando primeros 10 marcadores)"
    info_text += " - Haz clic en el mapa o usa el botón para verlo interactivo con zoom y desplazamiento"
    return info_text

def _open_url(url: str):
    """Función auxiliar para abrir URLs en el navegador (fallback cuando no hay page)"""
    import webbrowser
    try:
        webbrowser.open(url)
    except Exception:
        # Si webbrowser no funciona, intentar con el sistema
        import subprocess
        import platform
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["start", url], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", url])
            else:
                subprocess.Popen(["xdg-open", url])
        except Exception:
            pass
