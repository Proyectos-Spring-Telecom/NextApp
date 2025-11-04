# app/layout/drawer.py

import flet as ft

def make_drawer(on_drawer_change):
    return ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                label="Inicio", icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME
            ),
            ft.NavigationDrawerDestination(
                label="Vehiculos", icon=ft.Icons.REPORT_GMAILERRORRED_OUTLINED, selected_icon=ft.Icons.REPORT
            ),
            ft.NavigationDrawerDestination(
                label="Dashboard", icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD
            ),
            ft.Divider(),
            ft.NavigationDrawerDestination(
                label="Ajustes", icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS
            ),
            ft.NavigationDrawerDestination(
                label="Cerrar sesión", icon=ft.Icons.LOGOUT
            ),
        ],
        on_change=on_drawer_change,
    )
