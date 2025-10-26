from nicegui import ui

def render_hero(title, subtitle, button_label, button_link):
    """Sezione hero con titolo, sottotitolo, bottone e immagine"""
    with ui.row().classes(
        'items-center justify-between w-full p-10 bg-gradient-to-r from-orange-100 to-white rounded-xl shadow-sm'
    ):
        with ui.column().classes('w-1/2'):
            ui.label(title).classes('text-4xl font-bold mb-2')
            ui.label(subtitle).classes('text-gray-600 mb-4')
            ui.button(
                button_label,
                on_click=lambda: ui.navigate.to(button_link)
            ).classes('bg-orange-400 text-white rounded-lg px-4 py-2 hover:bg-orange-500')
        ui.image(
            'https://cdn.dribbble.com/users/185798/screenshots/10843206/media/97864cb3d2c2dd9b8a02c3c21f25e70a.png'
        ).classes('w-1/3 rounded-xl')
