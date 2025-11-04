# main.py
# Flet 0.28.3
# Splash → Welcome → Login → Home (AppShell con AppBar, Drawer, NavBar)

import flet as ft
import asyncio

from app.views import (
    SplashView,
    WelcomeView,
    LoginView,
    HomeView,
    VehiclesView,
    DashboardView,
    SettingsView,
)
from app.services.auth import login as auth_login
from app.components.alerts import show_success_alert, show_error_alert


def main(page: ft.Page):
    # --- Configuración base ---
    page.theme = ft.Theme(color_scheme_seed="#2196F3", use_material3=True)  # Blue
    page.title = "Next App (0.28.3)"
    page.theme_mode = page.platform_brightness
    page.padding = 0
    page.bgcolor = "#FAFAFA"  # SURFACE
    page.window_min_width = 420
    page.window_min_height = 720
    
    # NOTA: No configurar vertical_alignment ni horizontal_alignment a nivel de página
    # porque pueden ocultar el AppBar y otros componentes del shell

    # ---------------------------------------------------------
    # Navegación por ruta
    # ---------------------------------------------------------
    def on_route_change(e: ft.RouteChangeEvent):
        # Limpiar vistas PRIMERO
        page.views.clear()
        
        # Limpiar componentes del shell SOLO si NO vamos a /home
        if e.route != "/home":
            page.appbar = None
            page.drawer = None
            page.navigation_bar = None
            page.on_resize = None
            page.update()

        if page.route == "/":
            # Sin shell fuera de /home
            page.appbar = None
            page.drawer = None
            page.navigation_bar = None

            splash_view = ft.View(
                "/",
                controls=[SplashView()],
                padding=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )
            page.views.append(splash_view)
            page.update()

            # Navegar a welcome después de 1 segundo
            # Asegurar que funcione en web y desktop
            async def go_next():
                await asyncio.sleep(1)
                # Verificar que todavía estamos en la ruta splash
                if page.route == "/":
                    page.go("/welcome")
            
            # Ejecutar la tarea asíncrona
            page.run_task(go_next)
            return

        if page.route == "/welcome":
            page.appbar = None
            page.drawer = None
            page.navigation_bar = None

            page.views.append(
                ft.View(
                    "/welcome",
                    controls=[WelcomeView(lambda *_: page.go("/login"))],
                    padding=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            page.update()
            return

        if page.route == "/login":
            page.appbar = None
            page.drawer = None
            page.navigation_bar = None

            def on_login_ok(user_name: str, password: str):
                # Ejecutar el login de forma asíncrona para no bloquear la UI
                async def do_login_async():
                    try:
                        # Llamada al backend (ejecutar en thread separado para no bloquear UI)
                        res = await asyncio.to_thread(auth_login, user_name, password)
                        
                        if res.get("ok"):
                            # Guardamos credenciales temporalmente (hasta definir refresh token)
                            # Ejecutar en thread para no bloquear
                            await asyncio.to_thread(page.client_storage.set, "userName", user_name)
                            await asyncio.to_thread(page.client_storage.set, "password", password)

                            token = res.get("token") or ""
                            if token:
                                await asyncio.to_thread(page.client_storage.set, "token", token)

                            # Restaurar UI del botón ANTES de mostrar la alerta
                            restore_login_ui(preserve_values=False)
                            
                            # Mostrar alerta de éxito y navegar después
                            def navigate_to_home():
                                # Navegar directamente después de que el diálogo se cierre
                                # El on_ok del diálogo ya maneja el timing correcto
                                page.go("/home")
                            
                            show_success_alert(
                                page,
                                "¡Bienvenido!",
                                f"Sesión iniciada correctamente.\nBienvenido, {user_name}!",
                                on_ok=navigate_to_home
                            )
                        else:
                            # Error de API o credenciales: quedarse en /login
                            # Restaurar UI del botón pero mantener los valores de los campos
                            restore_login_ui(preserve_values=True)
                            
                            msg = res.get("error") or "No fue posible iniciar sesión. Verifica tus datos."
                            
                            # Mostrar alerta de error
                            show_error_alert(
                                page,
                                "Error de autenticación",
                                msg
                            )
                    except Exception as ex:
                        # Error inesperado - restaurar UI
                        restore_login_ui(preserve_values=True)
                        show_error_alert(
                            page,
                            "Error de conexión",
                            f"Error al conectar con el servidor:\n{str(ex)}"
                        )
                
                # Ejecutar en un task asíncrono
                page.run_task(do_login_async)

            login_view, restore_login_ui = LoginView(
                on_login_ok=on_login_ok,
                on_go_back=lambda: page.go("/welcome"),
            )
            
            page.views.append(
                ft.View(
                    "/login",
                    controls=[login_view],
                    padding=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            page.update()
            return

        if page.route == "/home":
            # Limpiar overlay si hay diálogos bloqueando
            if page.overlay:
                for item in list(page.overlay):
                    if isinstance(item, ft.AlertDialog):
                        item.open = False
                        page.overlay.remove(item)
            
            # Inicializar contenido - pasar page a HomeView
            content = ft.Container(
                content=HomeView(page),
                padding=20,
                expand=True
            )
            selected_index = 0

            def set_index(i: int):
                nonlocal selected_index
                selected_index = i
                navbar.selected_index = i
                # Pasar page a HomeView y VehiclesView cuando se selecciona
                views = [HomeView(page), VehiclesView(page), DashboardView()]
                content.content = views[i]
                page.update()

            def on_nav_change(e: ft.ControlEvent):
                set_index(e.control.selected_index)

            def open_drawer(_=None):
                if page.drawer is not None:
                    page.drawer.open = True
                    page.update()

            def on_drawer_select(e: ft.ControlEvent):
                idx = e.control.selected_index
                if idx in (0, 1, 2):
                    set_index(idx)
                elif idx == 3:
                    content.content = SettingsView()
                # Cerrar drawer después de un pequeño delay para evitar parpadeo
                async def close_drawer():
                    await asyncio.sleep(0.1)
                    if page.drawer is not None:
                        page.drawer.open = False
                        page.update()
                page.run_task(close_drawer)

            # Crear NavigationBar con iconos simples
            navbar = ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon="home", label="Inicio"),
                    ft.NavigationBarDestination(icon="directions_car", label="Vehículos"),
                    ft.NavigationBarDestination(icon="insights", label="Tablero"),
                ],
                selected_index=0,
                on_change=on_nav_change,
            )

            # Configurar componentes del shell ANTES de agregar la vista
            # 1. Drawer
            page.drawer = ft.NavigationDrawer(
                controls=[
                    ft.NavigationDrawerDestination(icon="home", label="Inicio"),
                    ft.NavigationDrawerDestination(icon="directions_car", label="Vehículos"),
                    ft.NavigationDrawerDestination(icon="insights", label="Tablero"),
                    ft.Divider(),
                    ft.NavigationDrawerDestination(icon="settings", label="Ajustes"),
                ],
                on_change=on_drawer_select,
            )

            # 2. AppBar
            appbar = ft.AppBar(
                leading=ft.IconButton(icon="menu", on_click=open_drawer, tooltip="Menú"),
                title=ft.Text("Next App"),
                center_title=False,
                bgcolor="#FAFAFA",
            )
            page.appbar = appbar

            # 3. NavigationBar según ancho
            def adapt_layout():
                if page.width is None or page.width < 900:
                    page.navigation_bar = navbar
                else:
                    page.navigation_bar = None

            # Configurar adaptación inicial
            adapt_layout()
            page.on_resize = lambda _: adapt_layout()
            
            # Agregar vista con AppBar también en la View (puede ser necesario en Flet 0.28.3)
            home_view = ft.View(
                route="/home",
                appbar=appbar,  # Configurar AppBar también en la View
                controls=[ft.Column([content], expand=True)],
                padding=0,
            )
            page.views.append(home_view)
            
            # Actualizar página para renderizar los componentes
            page.update()
            
            # Verificación adicional para web - asegurar que los componentes estén visibles
            async def verify_components():
                await asyncio.sleep(0.2)
                # Forzar actualización si los componentes no están visibles
                if page.appbar is None or page.drawer is None:
                    page.appbar = appbar
                    page.drawer = ft.NavigationDrawer(
                        controls=[
                            ft.NavigationDrawerDestination(icon="home", label="Inicio"),
                            ft.NavigationDrawerDestination(icon="directions_car", label="Vehículos"),
                            ft.NavigationDrawerDestination(icon="insights", label="Tablero"),
                            ft.Divider(),
                            ft.NavigationDrawerDestination(icon="settings", label="Ajustes"),
                        ],
                        on_change=on_drawer_select,
                    )
                    adapt_layout()
                    page.update()
            
            page.run_task(verify_components)
            return

        # Fallback
        page.go("/welcome")

    page.on_route_change = on_route_change

    # ---------------------------------------------------------
    # Control global del botón "Atrás"
    # ---------------------------------------------------------
    def handle_back(e: ft.ViewPopEvent):
        if page.route in ("/", "/welcome", "/login"):
            e.prevent_default = True
            return
        if len(page.views) > 1:
            page.views.pop()
            page.update()
        else:
            page.window_close()

    page.on_view_pop = handle_back

    # Primera navegación - usar un pequeño delay para asegurar que funcione en web
    async def initial_navigation():
        await asyncio.sleep(0.1)  # Pequeño delay para que la página esté lista
        page.go("/")
    
    page.run_task(initial_navigation)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
