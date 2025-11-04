# app/views/login.py

import flet as ft
from app.components.buttons import PrimaryPillButton

def LoginView(on_login_ok, on_go_back):
    # --- Header: logo + título alineados a 320px ---
    header = ft.Column(
        [
            ft.Container(
                content=ft.Image(src="assets/logoHorizontal1.png", width=200, height=120, opacity=0.95),
                alignment=ft.alignment.center_left,
                width=320,
                padding=ft.padding.only(bottom=100),
            ),
            ft.Container(
                content=ft.Text("Iniciar sesión", size=22, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center_left,
                width=320,
            ),
        ],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # Campos + validación visual
    user_error = ft.Text("", size=12, color=ft.Colors.ERROR, visible=False)
    pwd_error = ft.Text("", size=12, color=ft.Colors.ERROR, visible=False)

    user = ft.TextField(label="Correo Electronico", width=320)
    pwd = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=320)

    def do_login(_):
        # Trim
        u = (user.value or "").strip()
        p = (pwd.value or "").strip()

        # Reset errores
        user_error.value = ""
        user_error.visible = False
        pwd_error.value = ""
        pwd_error.visible = False

        if not u:
            user_error.value = "Escribe tu usuario."
            user_error.visible = True
            user.focus()
            user.update()
            user_error.update()
            return

        if not p:
            pwd_error.value = "Escribe tu contraseña."
            pwd_error.visible = True
            pwd.focus()
            pwd.update()
            pwd_error.update()
            return

        # OK: delega a on_login_ok (ya hace la llamada real en main)
        on_login_ok(u, p)

    # Acciones
    actions = ft.Column(
        [
            PrimaryPillButton("Entrar", on_click=do_login),
            ft.TextButton("Volver", on_click=lambda _: on_go_back()),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Form centrado
    form = ft.Column(
        [
            header,
            user,
            user_error,
            pwd,
            pwd_error,
            ft.Container(height=10),
            actions,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    # Pie (máx 320 px de ancho)
    footer_text = ft.Text(
        "Al iniciar aceptas nuestros Términos y Condiciones, así como nuestra Política de Privacidad.",
        size=14,
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.ON_SURFACE_VARIANT,
        no_wrap=False,
    )
    footer = ft.Container(
        content=ft.Container(
            content=footer_text,
            width=320,
            padding=ft.padding.symmetric(horizontal=16, vertical=8),
            alignment=ft.alignment.center,
        ),
        alignment=ft.alignment.center,
    )

    return ft.Column(
        [
            ft.Container(expand=True),
            form,
            ft.Container(expand=True),
            footer,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )
