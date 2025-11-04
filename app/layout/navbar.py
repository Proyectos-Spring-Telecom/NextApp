import flet as ft

def make_navbar(on_nav_change, selected_index=0):
    return ft.NavigationBar(
        bgcolor="#E7E0EC",
        indicator_color=ft.Colors.BLUE_200,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.LIST_ALT_OUTLINED, selected_icon=ft.Icons.LIST_ALT, label="Vehiculos"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.INSIGHTS_OUTLINED, selected_icon=ft.Icons.INSIGHTS, label="Dashboard"
            ),
        ],
        on_change=on_nav_change,
        selected_index=selected_index,
    )
