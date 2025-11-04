# app/components/alerts.py

import flet as ft
import asyncio

def show_success_alert(page: ft.Page, title: str, message: str, on_ok=None):
    """
    Muestra una alerta de éxito estilo "sweet alert"
    """
    def close_dialog(e):
        dialog.open = False
        page.update()
        # Ejecutar callback después de actualizar, para asegurar que el diálogo se cierre
        if on_ok:
            # Pequeño delay para asegurar que el overlay se limpie
            async def delayed_callback():
                await asyncio.sleep(0.1)
                on_ok()
            page.run_task(delayed_callback)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon("check_circle", color="#4CAF50", size=40),
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color="#4CAF50"),
        ], spacing=10),
        content=ft.Container(
            content=ft.Text(message, size=16, text_align=ft.TextAlign.CENTER),
            padding=ft.padding.only(top=10, bottom=10),
            width=300,
        ),
        actions=[
            ft.ElevatedButton(
                "OK",
                on_click=close_dialog,
                bgcolor="#4CAF50",
                color="#FFFFFF",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=16),
    )
    
    # En Flet 0.28.3, los diálogos se agregan al overlay
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def show_error_alert(page: ft.Page, title: str, message: str, on_ok=None):
    """
    Muestra una alerta de error estilo "sweet alert"
    """
    def close_dialog(e):
        dialog.open = False
        page.update()
        if on_ok:
            on_ok()
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon("error", color="#B00020", size=40),
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color="#B00020"),
        ], spacing=10),
        content=ft.Container(
            content=ft.Text(message, size=16, text_align=ft.TextAlign.CENTER),
            padding=ft.padding.only(top=10, bottom=10),
            width=300,
        ),
        actions=[
            ft.ElevatedButton(
                "OK",
                on_click=close_dialog,
                bgcolor="#B00020",
                color="#FFFFFF",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=16),
    )
    
    # En Flet 0.28.3, los diálogos se agregan al overlay
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def show_info_alert(page: ft.Page, title: str, message: str, on_ok=None):
    """
    Muestra una alerta informativa estilo "sweet alert"
    """
    def close_dialog(e):
        dialog.open = False
        page.update()
        if on_ok:
            on_ok()
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon("info", color="#2196F3", size=40),
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color="#2196F3"),
        ], spacing=10),
        content=ft.Container(
            content=ft.Text(message, size=16, text_align=ft.TextAlign.CENTER),
            padding=ft.padding.only(top=10, bottom=10),
            width=300,
        ),
        actions=[
            ft.ElevatedButton(
                "OK",
                on_click=close_dialog,
                bgcolor="#2196F3",
                color="#FFFFFF",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=16),
    )
    
    # En Flet 0.28.3, los diálogos se agregan al overlay
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

