import flet as ft
import asyncio
from app.services.vehicles import get_vehicles
from app.components.vehicle_card import create_vehicle_card

def VehiclesView(page: ft.Page) -> ft.Control:
    """
    Vista de lista de vehículos con tarjetas personalizadas.
    Requiere acceso a page para obtener el token del client_storage.
    """
    # Contenedor para la lista de vehículos
    vehicles_container = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center,
        expand=True,
    )
    
    # Título
    title = ft.Text("Vehículos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
    
    # Contador de vehículos
    counter_text = ft.Text("Cargando...", size=14, color="#757575")
    
    # Función para cargar los vehículos
    async def load_vehicles():
        try:
            # Obtener token del client_storage
            token = await asyncio.to_thread(page.client_storage.get, "token")
            
            if not token:
                vehicles_container.content = ft.Text(
                    "No hay token de autenticación. Por favor, inicia sesión nuevamente.",
                    size=16,
                    color="#F44336"
                )
                counter_text.value = "Sin autenticación"
                vehicles_container.update()
                counter_text.update()
                return
            
            # Obtener vehículos de la API
            result = await asyncio.to_thread(get_vehicles, token)
            
            if result.get("ok"):
                vehicles = result.get("data", [])
                
                counter_text.value = f"{len(vehicles)} vehículo(s) encontrado(s)"
                
                if vehicles:
                    # Crear tarjetas para cada vehículo
                    cards = []
                    for vehicle in vehicles:
                        # Crear una función específica para cada vehículo
                        def make_click_handler(v):
                            return lambda e: on_vehicle_click(v)
                        
                        card = create_vehicle_card(
                            vehicle,
                            on_click=make_click_handler(vehicle),
                            page=page
                        )
                        cards.append(card)
                    
                    # Crear lista scrollable
                    vehicles_list = ft.Column(
                        cards,
                        spacing=16,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    )
                    
                    vehicles_container.content = vehicles_list
                else:
                    vehicles_container.content = ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon("directions_car", size=64, color="#9E9E9E"),
                                ft.Text(
                                    "No hay vehículos disponibles",
                                    size=16,
                                    color="#757575",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=16,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
            else:
                error_msg = result.get("error", "Error desconocido")
                vehicles_container.content = ft.Text(
                    f"Error al cargar vehículos: {error_msg}",
                    size=16,
                    color="#F44336"
                )
                counter_text.value = "Error"
        except Exception as ex:
            vehicles_container.content = ft.Text(
                f"Error: {str(ex)}",
                size=16,
                color="#F44336"
            )
            counter_text.value = "Error"
        
        vehicles_container.update()
        counter_text.update()
    
    # Función callback cuando se hace clic en un vehículo
    def on_vehicle_click(vehicle):
        # Aquí puedes agregar funcionalidad cuando se hace clic en un vehículo
        # Por ejemplo, mostrar detalles, navegar a otra vista, etc.
        # Nota: No usar print() en web, puede causar errores en Pyodide
        # En su lugar, puedes usar un diálogo o navegación
        pass
    
    # Cargar vehículos al inicializar
    page.run_task(load_vehicles)
    
    return ft.Column(
        [
            ft.Row(
                [
                    title,
                    ft.Container(expand=True),
                    counter_text,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Divider(),
            vehicles_container,
        ],
        expand=True,
        spacing=0,
    )
