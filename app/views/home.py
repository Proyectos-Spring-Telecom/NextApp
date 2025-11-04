import flet as ft
import asyncio
from app.services.vehicles import get_vehicles
from app.services.locations import get_all_vehicles_locations
from app.components.map import create_map_with_markers

def HomeView(page: ft.Page) -> ft.Control:
    """
    Vista principal con mapa de vehículos.
    Requiere acceso a page para obtener el token del client_storage.
    """
    # Contenedor para el mapa
    map_container = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center,
        expand=True,
    )
    
    # Título
    title = ft.Text("Vehículos en el Mapa", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    
    # Función para cargar los vehículos
    async def load_vehicles():
        try:
            # Obtener token del client_storage
            token = await asyncio.to_thread(page.client_storage.get, "token")
            
            if not token:
                map_container.content = ft.Text(
                    "No hay token de autenticación. Por favor, inicia sesión nuevamente.",
                    size=16,
                    color="#F44336"
                )
                map_container.update()
                return
            
            # Obtener vehículos de la API
            result = await asyncio.to_thread(get_vehicles, token)
            
            if result.get("ok"):
                vehicles = result.get("data", [])
                
                if vehicles:
                    # Intentar obtener ubicaciones de los vehículos
                    locations = await asyncio.to_thread(get_all_vehicles_locations, token, vehicles)
                    
                    # Agregar coordenadas a los vehículos si se encontraron
                    for vehicle in vehicles:
                        vehicle_id = vehicle.get("id")
                        if vehicle_id in locations:
                            location_data = locations[vehicle_id]
                            # Agregar coordenadas al vehículo
                            vehicle["latitud"] = location_data.get("latitud") or location_data.get("Latitud") or location_data.get("lat") or location_data.get("latitude")
                            vehicle["longitud"] = location_data.get("longitud") or location_data.get("Longitud") or location_data.get("lon") or location_data.get("lng") or location_data.get("longitude")
                    
                    # Crear mapa con markers
                    map_widget = create_map_with_markers(
                        vehicles,
                        width=int(page.width) if page.width else None,
                        height=int(page.height * 0.7) if page.height else 600
                    )
                    map_container.content = map_widget
                else:
                    map_container.content = ft.Text(
                        "No hay vehículos disponibles",
                        size=16,
                    )
            else:
                error_msg = result.get("error", "Error desconocido")
                map_container.content = ft.Text(
                    f"Error al cargar vehículos: {error_msg}",
                    size=16,
                    color="#F44336"
                )
        except Exception as ex:
            map_container.content = ft.Text(
                f"Error: {str(ex)}",
                size=16,
                color="#F44336"
            )
        
        map_container.update()
    
    # Cargar vehículos al inicializar
    page.run_task(load_vehicles)
    
    return ft.Column(
        [
            title,
            ft.Divider(),
            map_container,
        ],
        expand=True,
    )
