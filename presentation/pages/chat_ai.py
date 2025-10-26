from nicegui import ui
from presentation.layout import render_navbar, render_footer

def render():
    """Renderizza la pagina Chat AI"""
    render_navbar()
    ui.label('💬 Chat AI').classes('text-2xl font-bold mb-4')

    ui.chat_message('Ciao! Come posso aiutarti oggi? 🤖')

    user_input = ui.input('Scrivi una domanda...').classes('w-2/3')
    ui.button(
        'Invia',
        on_click=lambda: ui.chat_message(f'Tu: {user_input.value}')
    ).classes('bg-orange-400 text-white ml-2')

    render_footer()
