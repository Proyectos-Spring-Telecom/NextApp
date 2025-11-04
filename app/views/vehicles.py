import flet as ft

def VehiclesView() -> ft.Control:
    return ft.Column(
        [
            ft.Text("Vehiculos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Listado de vehiculos."),
        ],
        expand=True,
    )
