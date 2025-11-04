import flet as ft

def DashboardView() -> ft.Control:
    return ft.Column(
        [
            ft.Text("Dashboard", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Gráficas y métricas clave."),
        ],
        expand=True,
    )
