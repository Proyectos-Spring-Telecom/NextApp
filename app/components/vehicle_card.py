# app/components/vehicle_card.py

import flet as ft

def create_vehicle_card(vehicle: dict, on_click=None):
    """
    Crea una tarjeta personalizada para mostrar información de un vehículo.
    
    Args:
        vehicle: Diccionario con datos del vehículo
        on_click: Función callback cuando se hace clic en la tarjeta
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
        card_content.cursor = ft.Cursor.CLICK
    
    return card_content

