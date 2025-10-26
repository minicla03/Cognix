from nicegui import ui

def render_feature_cards(features):
    """Mostra feature cards in riga"""
    with ui.row().classes('justify-around w-full mt-8'):
        for icon, title, desc in features:
            with ui.card().classes('w-1/4 p-4 shadow-md hover:shadow-lg transition'):
                ui.label(icon).classes('text-3xl mb-2')
                ui.label(title).classes('font-semibold text-lg')
                ui.label(desc).classes('text-gray-600 text-sm')
