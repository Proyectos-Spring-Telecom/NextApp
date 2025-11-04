import flet as ft

def HomeView() -> ft.Control:
    return ft.Column(
        [
            ft.Text("Inicio", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Contenido de la pantalla de inicio."),
        ],
        expand=True,
    )
