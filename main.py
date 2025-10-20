# main.py
# Flet 0.28.3 (sin UserControl)
# AppBar + NavigationDrawer lateral + NavigationBar inferior

import flet as ft

# --- "Pantallas" (activities) simples para demo ---
def HomeView() -> ft.Control:
    return ft.Column(
        [
            ft.Text("Inicio", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Contenido de la pantalla de inicio."),
        ],
        expand=True,
    )

def IncidentsView() -> ft.Control:
    return ft.Column(
        [
            ft.Text("Incidencias", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Listado / acciones de incidencias."),
        ],
        expand=True,
    )

def DashboardView() -> ft.Control:
    return ft.Column(
        [
            ft.Text("Dashboard", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Gráficas y métricas clave."),
        ],
        expand=True,
    )

# --- Punto de entrada ---
def main(page: ft.Page):
    page.title = "Flet Skeleton — Drawer + BottomNav (0.28.3)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = ft.Colors.SURFACE
    page.window_min_width = 420
    page.window_min_height = 720

    selected_index = 0  # 0: Home, 1: Incidents, 2: Dashboard
    content = ft.Container(padding=20, expand=True)

    # --- Callbacks ---
    def set_index(i: int):
        nonlocal selected_index
        selected_index = i
        navbar.selected_index = i
        content.content = [HomeView(), IncidentsView(), DashboardView()][i]
        page.update()

    def on_nav_change(e: ft.ControlEvent):
        set_index(e.control.selected_index)

    def on_drawer_change(e: ft.ControlEvent):
        idx = e.control.selected_index
        if idx in (0, 1, 2):
            set_index(idx)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ir a Ajustes (no implementado)"))
            page.snack_bar.open = True
        # Cerrar drawer en móviles
        page.drawer.open = False
        page.update()

    def open_drawer(_):
        page.drawer.open = True
        page.update()

    def adapt_layout():
        wide = page.width and page.width >= 900
        page.navigation_bar = None if wide else navbar
        page.update()

    def on_resize(_):
        adapt_layout()

    # Drawer lateral
    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                label="Inicio", icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME
            ),
            ft.NavigationDrawerDestination(
                label="Incidencias", icon=ft.Icons.REPORT_GMAILERRORRED_OUTLINED, selected_icon=ft.Icons.REPORT
            ),
            ft.NavigationDrawerDestination(
                label="Dashboard", icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD
            ),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                label="Ajustes", icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS
            ),
        ],
        on_change=on_drawer_change,
    )

    # AppBar con botón de menú para abrir el Drawer
    appbar = ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer),
        title=ft.Text("Flet Skeleton"),
        center_title=False,
        bgcolor=ft.Colors.SURFACE,
        actions=[
            ft.IconButton(ft.Icons.SEARCH),
            ft.IconButton(ft.Icons.NOTIFICATIONS_NONE),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Perfil"),
                    ft.PopupMenuItem(text="Cerrar sesión"),
                ]
            ),
        ],
    )

    # NavigationBar inferior (en 0.28.3 usa NavigationBarDestination)
    navbar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.LIST_ALT_OUTLINED, selected_icon=ft.Icons.LIST_ALT, label="Incidencias"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INSIGHTS_OUTLINED, selected_icon=ft.Icons.INSIGHTS, label="Dashboard"
            ),
        ],
        on_change=on_nav_change,
        selected_index=selected_index,
    )

    # Montaje de la "shell"
    page.appbar = appbar
    page.drawer = drawer
    page.navigation_bar = navbar
    page.on_resize = on_resize

    set_index(0)  # pantalla inicial
    page.add(ft.Column([content], expand=True))
    adapt_layout()

if __name__ == "__main__":
    ft.app(target=main)
