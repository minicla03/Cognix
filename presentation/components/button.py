from nicegui import ui

def render_primary_button(label, on_click=None):
    """Bottone primario riutilizzabile"""
    ui.button(label, on_click=on_click).classes(
        'bg-orange-400 text-white rounded-lg px-4 py-2 hover:bg-orange-500'
    )
