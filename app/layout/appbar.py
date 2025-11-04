import flet as ft

def make_appbar(open_drawer):
    return ft.AppBar(
        leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer),
        title=ft.Text("Next App"),
        center_title=False,
        bgcolor="#FAFAFA",  # SURFACE
        actions=[
            ft.IconButton(ft.Icons.SEARCH),
            ft.IconButton(ft.Icons.NOTIFICATIONS_NONE),
            ft.PopupMenuButton(
                items=[ft.PopupMenuItem(text="Perfil"), ft.PopupMenuItem(text="Cerrar sesión")]
            ),
        ],
    )
