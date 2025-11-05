# app/components/vehicle_card.py

import flet as ft
from app.components.map import create_vehicle_map_modal

def create_vehicle_card(vehicle: dict, on_click=None, page: ft.Page = None):
    """
    Crea una tarjeta personalizada para mostrar información de un vehículo.
    
    Args:
        vehicle: Diccionario con datos del vehículo
        on_click: Función callback cuando se hace clic en la tarjeta
        page: Página de Flet para mostrar el mapa modal (opcional)
    """
    # Extraer información del vehículo
    placas = vehicle.get("placas") or vehicle.get("Placas") or "N/A"
    economico = vehicle.get("economico") or vehicle.get("Economico") or ""
    marca = vehicle.get("marca") or vehicle.get("Marca") or ""
    modelo = vehicle.get("modelo") or vehicle.get("Modelo") or ""
    anio = vehicle.get("anio") or vehicle.get("Anio") or ""
    color = vehicle.get("color") or vehicle.get("Color") or ""
    imagen = vehicle.get("imagen") or vehicle.get("Imagen") or ""
    cliente = vehicle.get("cliente") or vehicle.get("Cliente") or ""
    km = vehicle.get("km") or vehicle.get("Km") or 0
    imei = vehicle.get("imei") or vehicle.get("IMEI") or ""
    
    # Construir información de la tarjeta
    title = f"{placas}"
    if economico:
        title += f" - {economico}"
    
    subtitle = f"{marca} {modelo}".strip()
    if anio:
        subtitle += f" ({anio})"
    
    # Imagen del vehículo
    image_content = None
    if imagen:
        try:
            image_content = ft.Image(
                src=imagen,
                fit=ft.ImageFit.COVER,
                width=200,
                height=150,
                border_radius=8,
            )
        except:
            image_content = None
    
    if not image_content:
        # Placeholder si no hay imagen
        image_content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon("directions_car", size=48, color="#9E9E9E"),
                    ft.Text("Sin imagen", size=12, color="#9E9E9E"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=200,
            height=150,
            bgcolor="#F5F5F5",
            border_radius=8,
            alignment=ft.alignment.center,
        )
    
    # Información adicional
    info_items = []
    
    if color:
        info_items.append(
            ft.Row(
                [
                    ft.Icon("palette", size=16, color="#757575"),
                    ft.Text(f"Color: {color}", size=12, color="#616161"),
                ],
                spacing=4,
            )
        )
    
    if cliente:
        info_items.append(
            ft.Row(
                [
                    ft.Icon("person", size=16, color="#757575"),
                    ft.Text(f"Cliente: {cliente[:30]}...", size=12, color="#616161"),
                ],
                spacing=4,
            )
        )
    
    if km:
        info_items.append(
            ft.Row(
                [
                    ft.Icon("speed", size=16, color="#757575"),
                    ft.Text(f"KM: {km:,.0f}", size=12, color="#616161"),
                ],
                spacing=4,
            )
        )
    
    if imei:
        info_items.append(
            ft.Row(
                [
                    ft.Icon("gps_fixed", size=16, color="#757575"),
                    ft.Text(f"IMEI: {imei}", size=12, color="#616161"),
                ],
                spacing=4,
            )
        )
    
    # Contenido principal de la tarjeta
    card_content = ft.Container(
        content=ft.Row(
            [
                # Imagen
                image_content,
                
                # Información
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                title,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#212121",
                            ),
                            ft.Text(
                                subtitle,
                                size=14,
                                color="#757575",
                            ),
                            ft.Divider(height=10, color="transparent"),
                            ft.Column(
                                info_items,
                                spacing=6,
                                tight=True,
                            ),
                            # Botón para ver mapa del vehículo
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Ver en mapa",
                                        icon="map",
                                        on_click=lambda e, v=vehicle: _show_vehicle_map(v, page),
                                        style=ft.ButtonStyle(
                                            color="#FFFFFF",
                                            bgcolor="#0D2571",
                                        ),
                                        height=36,
                                    ),
                                ],
                                spacing=8,
                            ) if page else ft.Container(),
                        ],
                        spacing=8,
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    expand=True,
                    padding=ft.padding.only(left=16),
                ),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        padding=16,
        bgcolor="#FFFFFF",
        border_radius=12,
        border=ft.border.all(1, "#E0E0E0"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color="#00000015",
            offset=ft.Offset(0, 2),
        ),
    )
    
    # Si hay un callback, hacer la tarjeta clickeable
    if on_click:
        card_content.on_click = lambda e: on_click(vehicle)
        # Nota: ft.Cursor no está disponible en Flet 0.28.3
    
    return card_content


def _show_vehicle_map(vehicle: dict, page: ft.Page):
    """Muestra el mapa modal del vehículo"""
    if not page:
        return
    
    # Buscar coordenadas del vehículo
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
        # Obtener nombre del vehículo
        nombre = (
            vehicle.get("placas") or vehicle.get("Placas") or
            vehicle.get("economico") or vehicle.get("Economico") or
            vehicle.get("descripcion") or vehicle.get("Descripcion") or
            vehicle.get("nombre") or vehicle.get("Nombre") or 
            vehicle.get("placa") or vehicle.get("Placa") or 
            vehicle.get("PlacaVehiculo") or 
            "Vehículo"
        )
        
        # Crear y mostrar el modal del mapa
        map_dialog = create_vehicle_map_modal(page, vehicle, float(lat), float(lon), nombre)
        page.dialog = map_dialog
        map_dialog.open = True
        page.update()
    else:
        # Mostrar error si no hay coordenadas
        from app.components.alerts import show_error_alert
        show_error_alert(
            page,
            "Ubicación no disponible",
            "Este vehículo no tiene coordenadas GPS registradas."
        )

