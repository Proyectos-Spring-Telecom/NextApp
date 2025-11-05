import flet as ft
import asyncio
from app.services.vehicles import get_vehicles
from app.services.locations import get_last_vehicles_positions
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
            
            # Obtener últimas posiciones de vehículos directamente desde el endpoint
            positions_result = await asyncio.to_thread(get_last_vehicles_positions, token)
            
            if positions_result.get("ok"):
                vehicles_with_positions = positions_result.get("data", [])
                
                if vehicles_with_positions:
                    # El endpoint devuelve vehículos con sus últimas posiciones
                    # Crear mapa con markers directamente
                    map_widget = create_map_with_markers(
                        vehicles_with_positions,
                        width=int(page.width) if page.width else None,
                        height=int(page.height * 0.7) if page.height else 600,
                        page=page
                    )
                    map_container.content = map_widget
                else:
                    # Si no hay vehículos con posiciones, intentar obtener lista de vehículos
                    vehicles_result = await asyncio.to_thread(get_vehicles, token)
                    if vehicles_result.get("ok"):
                        vehicles = vehicles_result.get("data", [])
                        if vehicles:
                            # Crear mapa aunque no tenga coordenadas (mostrará mensaje)
                            map_widget = create_map_with_markers(
                                vehicles,
                                width=int(page.width) if page.width else None,
                                height=int(page.height * 0.7) if page.height else 600,
                                page=page
                            )
                            map_container.content = map_widget
                        else:
                            map_container.content = ft.Text(
                                "No hay vehículos disponibles",
                                size=16,
                            )
                    else:
                        map_container.content = ft.Text(
                            "No hay vehículos con posiciones disponibles",
                            size=16,
                        )
            else:
                # Si falla el endpoint de posiciones, intentar con vehículos sin posiciones
                vehicles_result = await asyncio.to_thread(get_vehicles, token)
                if vehicles_result.get("ok"):
                    vehicles = vehicles_result.get("data", [])
                    if vehicles:
                        # Crear mapa aunque no tenga coordenadas (mostrará mensaje)
                        map_widget = create_map_with_markers(
                            vehicles,
                            width=int(page.width) if page.width else None,
                            height=int(page.height * 0.7) if page.height else 600
                        )
                        map_container.content = map_widget
                    else:
                        error_msg = positions_result.get("error", "Error desconocido")
                        map_container.content = ft.Text(
                            f"Error al cargar posiciones: {error_msg}",
                            size=16,
                            color="#F44336"
                        )
                else:
                    error_msg = positions_result.get("error", "Error desconocido")
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
