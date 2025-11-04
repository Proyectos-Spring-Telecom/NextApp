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


def main(page: ft.Page):
    # --- Configuración base ---
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE, use_material3=True)
    page.title = "Next App (0.28.3)"
    page.theme_mode = page.platform_brightness
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.SURFACE
    page.window_min_width = 420
    page.window_min_height = 720

    # ---------------------------------------------------------
    # AppShell para /home (AppBar + Drawer + NavigationBar)
    # ---------------------------------------------------------
    def build_app_shell():
        content = ft.Container(padding=20, expand=True)
        selected_index = 0

        def set_index(i: int):
            nonlocal selected_index
            selected_index = i
            navbar.selected_index = i
            content.content = [HomeView(), VehiclesView(), DashboardView()][i]
            page.update()

        def on_nav_change(e: ft.ControlEvent):
            set_index(e.control.selected_index)

        def open_drawer(_=None):
            page.drawer.open = True
            page.update()

        def on_drawer_select(e: ft.ControlEvent):
            idx = e.control.selected_index
            if idx in (0, 1, 2):  # Home, Vehículos, Tablero
                set_index(idx)
            elif idx == 3:        # Ajustes
                content.content = SettingsView()
            page.drawer.open = False
            page.update()

        # AppBar simple con botón de menú
        page.appbar = ft.AppBar(
            leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer),
            title=ft.Text("Next App"),
            center_title=False,
            bgcolor=ft.Colors.SURFACE,
        )

        # Drawer propio
        page.drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicio"),
                ft.NavigationDrawerDestination(icon=ft.Icons.DIRECTIONS_CAR_OUTLINED, label="Vehículos"),
                ft.NavigationDrawerDestination(icon=ft.Icons.INSIGHTS_OUTLINED, label="Tablero"),
                ft.Divider(),
                ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS_OUTLINED, label="Ajustes"),
            ],
            on_change=on_drawer_select,
        )

        # Bottom NavigationBar
        nonlocal_nav_index = 0  # solo para estado inicial
        navbar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.Icons.HOME_OUTLINED, label="Inicio"),
                ft.NavigationDestination(icon=ft.Icons.DIRECTIONS_CAR_OUTLINED, label="Vehículos"),
                ft.NavigationDestination(icon=ft.Icons.INSIGHTS_OUTLINED, label="Tablero"),
            ],
            selected_index=nonlocal_nav_index,
            on_change=on_nav_change,
        )

        # Adaptación por ancho
        def adapt_layout():
            wide = (page.width or 0) >= 900
            page.navigation_bar = None if wide else navbar
            page.update()

        page.on_resize = lambda _: adapt_layout()

        # Estado inicial
        set_index(0)
        adapt_layout()  # <- importante para que se vea el navbar al entrar

        # Vista con contenido centrado
        return ft.View(
            route="/home",
            controls=[ft.Column([content], expand=True)],
            padding=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )

    # ---------------------------------------------------------
    # Navegación por ruta
    # ---------------------------------------------------------
    def on_route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        if page.route == "/":
            # Sin shell fuera de /home
            page.appbar = None
            page.drawer = None
            page.navigation_bar = None

            page.views.append(
                ft.View(
                    "/",
                    controls=[SplashView()],
                    padding=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            page.update()

            async def go_next():
                await asyncio.sleep(1)
                page.go("/welcome")

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
                # Llamada al backend (sin navegar si falla)
                res = auth_login(user_name, password)

                if res.get("ok"):
                    # Guardamos credenciales temporalmente (hasta definir refresh token)
                    page.client_storage.set("userName", user_name)
                    page.client_storage.set("password", password)

                    token = res.get("token") or ""
                    if token:
                        page.client_storage.set("token", token)

                    page.snack_bar = ft.SnackBar(ft.Text("Sesión iniciada"))
                    page.snack_bar.open = True
                    page.update()

                    page.go("/home")
                else:
                    # Error de API o credenciales: quedarse en /login
                    msg = res.get("error") or "No fue posible iniciar sesión. Verifica tus datos."
                    page.dialog = ft.AlertDialog(
                        title=ft.Text("Error de autenticación"),
                        content=ft.Text(msg),
                        actions=[ft.TextButton("Entendido", on_click=lambda _: setattr(page.dialog, "open", False))],
                        actions_alignment=ft.MainAxisAlignment.END,
                        open=True,
                    )
                    page.update()

            page.views.append(
                ft.View(
                    "/login",
                    controls=[
                        LoginView(
                            on_login_ok=on_login_ok,
                            on_go_back=lambda: page.go("/welcome"),
                        )
                    ],
                    padding=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            page.update()
            return

        if page.route == "/home":
            # Aquí sí montamos TODO el shell
            shell_view = build_app_shell()
            page.views.append(shell_view)
            page.update()
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

    # Primera navegación
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
