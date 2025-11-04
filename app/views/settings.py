import flet as ft

def SettingsView(page: ft.Page) -> ft.Control:
    is_dark = page.theme_mode == ft.ThemeMode.DARK

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        )
        page.update()

    return ft.Column(
        [
            ft.Text("Ajustes", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Divider(),
            ft.Text("Preferencias generales"),
            ft.Row(
                [
                    ft.Switch(
                        label="Tema oscuro",
                        value=is_dark,
                        on_change=toggle_theme,
                    ),
                ]
            ),
        ],
        expand=True,
    )
