from nicegui import ui
from presentation.layout import setup_layout
from presentation.pages import home
from flask import Flask
from backend.routes.user_routes import auth_bp
from redis_db.RedisDBMS import RedisConnectionManager


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp, url_prefix='/api')
    # other api....
    return app

def frontend_setup():
    setup_layout()

    with ui.sub_pages() as sub_pages:

        @ui.page('/')
        def home_page():
            """Homepage / Vetrina"""
            home.render()

if __name__ == '__main__':
    qa = create_app()
    RedisConnectionManager.instance()
    frontend_setup()
    ui.bind_flask(qa)
    ui.run(title='Studia+ | AI Studio', reload=True)
