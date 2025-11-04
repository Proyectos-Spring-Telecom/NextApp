# app/views/login.py

import flet as ft
from app.components.buttons import PrimaryPillButton

def LoginView(on_login_ok, on_go_back):
    # Esta función retornará una tupla: (view, restore_ui_function)
    # --- Header: logo + título alineados a 320px ---
    header = ft.Column(
        [
            ft.Container(
                content=ft.Image(src="logoHorizontal1.png", width=250, height=90, opacity=0.95),
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
    user_error = ft.Text("", size=12, color="#B00020", visible=False)  # ERROR
    pwd_error = ft.Text("", size=12, color="#B00020", visible=False)  # ERROR

    user = ft.TextField(label="Correo Electronico", width=320)
    pwd = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=320)
    
    # Indicador de carga
    loading_indicator = ft.ProgressRing(width=20, height=20, visible=False)
    login_button = PrimaryPillButton("Entrar", on_click=None)  # Se asignará después

    def do_login(e):
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
            # Actualizar controles
            user.update()
            user_error.update()
            login_button.update()
            return

        if not p:
            pwd_error.value = "Escribe tu contraseña."
            pwd_error.visible = True
            pwd.focus()
            # Actualizar controles
            pwd.update()
            pwd_error.update()
            login_button.update()
            return

        # Mostrar indicador de carga y deshabilitar botón
        loading_indicator.visible = True
        login_button.disabled = True
        login_button.text = "Iniciando sesión..."
        user.disabled = True
        pwd.disabled = True
        
        # Actualizar UI
        loading_indicator.update()
        login_button.update()
        user.update()
        pwd.update()
        
        # OK: delega a on_login_ok (ya hace la llamada real en main)
        # on_login_ok ahora es asíncrono y maneja los errores internamente
        on_login_ok(u, p)
    
    # Asignar el handler al botón
    login_button.on_click = do_login

    # Función para restaurar el estado del botón (será llamada desde main después del login)
    # preserve_values: si es True, mantiene los valores de los campos
    def restore_ui(preserve_values=False):
        loading_indicator.visible = False
        login_button.disabled = False
        login_button.text = "Entrar"
        user.disabled = False
        pwd.disabled = False
        if not preserve_values:
            # Limpiar campos solo si no se preservan
            user.value = ""
            pwd.value = ""
        loading_indicator.update()
        login_button.update()
        user.update()
        pwd.update()

    # Acciones
    actions = ft.Column(
        [
            ft.Row(
                [
                    login_button,
                    loading_indicator,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
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
        color="#605D62",  # ON_SURFACE_VARIANT
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

    view = ft.Column(
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
    
    # Retornar la vista y la función de restauración
    return view, restore_ui
