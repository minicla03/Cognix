from nicegui import ui

def setup_layout():
    """Configura tema e colori globali"""
    ui.colors(primary='#ffb347', secondary='#2c6bed')

def render_navbar():
    """Navbar riutilizzabile"""
    with ui.header().classes('justify-between bg-white text-black shadow-sm p-3'):
        ui.label('🧠 STUDIA+').classes('text-lg font-bold')
        with ui.row().classes('gap-4'):
            ui.link('Home', '/')
            ui.link('Notebook', '/notebooks')
            ui.link('Chat AI', '/chat')

def render_footer():
    """Footer riutilizzabile"""
    with ui.footer().classes('justify-center text-gray-500 p-2'):
        ui.label('© 2025 Studia+ — Potenziato da AI Studio')
