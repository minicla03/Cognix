from nicegui import ui
from presentation.layout import setup_layout
from presentation.pages import home

setup_layout()

with ui.sub_pages() as sub_pages:

    @ui.page('/')
    def home_page():
        """Homepage / Vetrina"""
        home.render()

# --- Avvio server ---
if __name__ == '__main__':
    ui.run(title='Studia+ | AI Studio', reload=True)
