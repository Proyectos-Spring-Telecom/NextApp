import flet as ft

def SplashView() -> ft.Control:
    return ft.Column(
        [
            ft.Image(src="splash.png", width=225, height=81, fit=ft.ImageFit.CONTAIN),
            ft.Text("Next App", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Inicializando...", size=14, color="#9E9E9E"),  # GREY
            ft.ProgressBar(width=240),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
