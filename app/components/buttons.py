# app/components/buttons.py

import flet as ft

def PrimaryPillButton(text: str, on_click=None, width: int = 320):
    """
    Botón pill estable y homogéneo.
    - Ancho fijo (por defecto 320 px) para igualar TextField.
    - Azul corporativo consistente en todos los estados.
    - Sin dependencias de tema.
    """
    safe_handler = on_click if callable(on_click) else (lambda e: None)

    blue         = "#0D2571"
    blue_hover   = "#12308F"
    blue_pressed = "#0B1E66"
    white        = "#FFFFFF"
    white70      = "#B3FFFFFF"  # white con 70% opacidad

    return ft.ElevatedButton(
        text,
        width=width,                 # ← mismo ancho que los TextField
        on_click=safe_handler,
        disabled=False,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT:  blue,
                ft.ControlState.HOVERED:  blue_hover,
                ft.ControlState.FOCUSED:  blue_hover,
                ft.ControlState.PRESSED:  blue_pressed,
                ft.ControlState.DISABLED: blue,
            },
            color={
                ft.ControlState.DEFAULT:  white,
                ft.ControlState.HOVERED:  white,
                ft.ControlState.FOCUSED:  white,
                ft.ControlState.PRESSED:  white,
                ft.ControlState.DISABLED: white70,
            },
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding(0, 16, 0, 16),   # alto cómodo sin “ensanchar” el botón
            overlay_color="#14FFFFFF",  # white con 8% opacidad
            elevation=2,
        ),
    )
