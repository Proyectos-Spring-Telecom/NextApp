# app/components/map.py

import flet as ft

def create_map_with_markers(vehicles_data: list, width: int = None, height: int = 600):
    """
    Crea un mapa con markers basado en los datos de vehículos.
    Usa OpenStreetMap con Leaflet.js a través de Html control.
    
    vehicles_data: Lista de vehículos con campos latitud y longitud
    """
    if not vehicles_data:
        return ft.Container(
            content=ft.Text("No hay vehículos disponibles", size=16),
            alignment=ft.alignment.center,
            width=width,
            height=height,
        )
    
    # Generar código JavaScript para el mapa
    # Preparar markers
    markers_js = []
    for idx, vehicle in enumerate(vehicles_data):
        # Buscar coordenadas en diferentes campos posibles
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
            # Obtener información del vehículo para el popup
            nombre = (
                vehicle.get("placas") or vehicle.get("Placas") or
                vehicle.get("economico") or vehicle.get("Economico") or
                vehicle.get("descripcion") or vehicle.get("Descripcion") or
                vehicle.get("nombre") or vehicle.get("Nombre") or 
                vehicle.get("placa") or vehicle.get("Placa") or 
                vehicle.get("PlacaVehiculo") or 
                f"Vehículo {idx + 1}"
            )
            # Información adicional para el popup
            marca = vehicle.get("marca") or vehicle.get("Marca") or ""
            modelo = vehicle.get("modelo") or vehicle.get("Modelo") or ""
            popup_text = f"{nombre}"
            if marca or modelo:
                popup_text += f"<br>{marca} {modelo}".strip()
            
            # Escapar comillas para JavaScript
            popup_escaped = str(popup_text).replace('"', '\\"').replace("'", "\\'").replace("\n", " ")
            markers_js.append(f"""
                L.marker([{lat}, {lon}]).addTo(map)
                    .bindPopup("{popup_escaped}");
            """)
    
    # Si no hay markers válidos, mostrar información de los vehículos
    if not markers_js:
        # Crear lista de vehículos disponibles
        vehicles_list = []
        for idx, vehicle in enumerate(vehicles_data[:10]):  # Mostrar máximo 10
            placas = vehicle.get("placas") or vehicle.get("Placas") or "N/A"
            economico = vehicle.get("economico") or vehicle.get("Economico") or ""
            marca = vehicle.get("marca") or vehicle.get("Marca") or ""
            modelo = vehicle.get("modelo") or vehicle.get("Modelo") or ""
            imei = vehicle.get("imei") or ""
            
            vehicle_info = f"• {placas}"
            if economico:
                vehicle_info += f" ({economico})"
            if marca or modelo:
                vehicle_info += f" - {marca} {modelo}".strip()
            if imei:
                vehicle_info += f" [IMEI: {imei}]"
            
            vehicles_list.append(ft.Text(vehicle_info, size=14))
        
        more_text = ""
        if len(vehicles_data) > 10:
            more_text = f"\n... y {len(vehicles_data) - 10} vehículos más"
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Los vehículos no tienen coordenadas disponibles",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"Se encontraron {len(vehicles_data)} vehículo(s) sin ubicación GPS:",
                        size=14,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=20),
                    ft.Column(vehicles_list, spacing=8, scroll=ft.ScrollMode.AUTO),
                    ft.Text(more_text, size=12) if more_text else ft.Container(),
                    ft.Divider(height=20),
                    ft.Text(
                        "Nota: Se requiere un endpoint adicional para obtener las coordenadas de los vehículos.",
                        size=12,
                        color="#757575",
                        text_align=ft.TextAlign.CENTER,
                        italic=True,
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            alignment=ft.alignment.center,
            width=width,
            height=height,
            padding=20,
        )
    
    # Calcular centro del mapa (promedio de todas las coordenadas)
    lats = []
    lons = []
    for vehicle in vehicles_data:
        lat = vehicle.get("latitud") or vehicle.get("Latitud") or vehicle.get("lat")
        lon = vehicle.get("longitud") or vehicle.get("Longitud") or vehicle.get("lon") or vehicle.get("lng")
        if lat and lon:
            lats.append(float(lat))
            lons.append(float(lon))
    
    center_lat = sum(lats) / len(lats) if lats else 19.4326  # Default: Ciudad de México
    center_lon = sum(lons) / len(lons) if lons else -99.1332
    
    # HTML completo con Leaflet
    map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([{center_lat}, {center_lon}], 13);
        
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);
        
        // Agregar markers
        {''.join(markers_js)}
    </script>
</body>
</html>
    """
    
    # Usar Html control de Flet
    # Nota: En Flet 0.28.3, puede ser que Html use 'value' en lugar de 'content'
    try:
        return ft.Html(
            value=map_html,
            width=width,
            height=height,
        )
    except TypeError:
        # Si 'value' no funciona, intentar con otros parámetros
        try:
            return ft.Html(
                content=map_html,
                width=width,
                height=height,
            )
        except:
            # Si Html no está disponible, usar un contenedor con texto
            return ft.Container(
                content=ft.Text(
                    f"Mapa con {len([m for m in markers_js if m])} vehículos\n"
                    f"Centro: {center_lat}, {center_lon}\n"
                    "(El componente Html no está disponible en esta versión de Flet)",
                    size=14,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                width=width,
                height=height,
                bgcolor="#E3F2FD",
                border_radius=8,
                padding=20,
            )

