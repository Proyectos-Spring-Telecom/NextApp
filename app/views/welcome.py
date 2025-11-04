# app/views/welcome.py

import flet as ft
from app.components.buttons import PrimaryPillButton

def WelcomeView(on_continue):
    """
    Bienvenida estable: fondo translúcido, logo, textos y botón.
    Sin tema dinámico en el botón; siempre azul.
    """

    # Fondo translúcido (car.png)
    background = ft.Image(
        src="welcome/home.png",
        fit=ft.ImageFit.CONTAIN,
        opacity=0.80,
        repeat=ft.ImageRepeat.NO_REPEAT,
    )

    # Logo (450x161 px real, escalado proporcionalmente)
    logo = ft.Image(src="logoHorizontal1.png", width=250, height=90, fit=ft.ImageFit.CONTAIN)

    # Textos
    title = ft.Text("Bienvenido a Next App", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#FFFFFF") 
    subtitle = ft.Text("Tu entorno unificado para gestión y análisis.", text_align=ft.TextAlign.CENTER, color="#FFFFFF")

    # Botón consistente (sin theme_mode ni width)
    button = PrimaryPillButton("Continuar", on_click=on_continue)

    # Contenido centrado
    content = ft.Column(
        [logo, ft.Container(height=2), title, subtitle, ft.Container(height=10), button],
        alignment=ft.MainAxisAlignment.END,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # Stack: fondo + contenido (ambos centrados)
    view = ft.Stack(
        [
            ft.Container(content=background, alignment=ft.alignment.center, expand=True),
            ft.Container(
                content=content,
                alignment=ft.alignment.bottom_center,
                expand=True,
                padding=ft.padding.only(bottom=40),
            ),
            #ft.Container(content=content, alignment=ft.alignment.center, expand=True),
        ],
        expand=True,
    )

    # Fondo base según tema del sistema (solo color de page)
    def on_mount(e: ft.ControlEvent):
        page = e.page
        page.bgcolor = (
            "#E7E0EC"  # SURFACE_CONTAINER_HIGHEST
            if page.theme_mode == ft.ThemeMode.LIGHT
            else "#FFFFFF"  # BACKGROUND
        )

    view.on_mount = on_mount
    return view
