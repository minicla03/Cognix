from nicegui import ui
from presentation.layout import render_navbar, render_footer

def render():
    """Renderizza la pagina dei notebook"""
    render_navbar()
    ui.label('📘 I tuoi notebook').classes('text-2xl font-bold mb-4')
    ui.button('➕ Crea nuovo notebook').classes('bg-orange-400 text-white rounded-lg mb-4')

    with ui.row().classes('flex-wrap gap-4'):
        for i in range(3):
            idx = i  # cattura corretta
            with ui.card().classes('p-4 w-1/4 shadow-md'):
                ui.label(f'Notebook {idx+1}')
                ui.button('Apri', on_click=lambda idx=idx: ui.navigate.to('/chat')).classes('mt-2')

    render_footer()
