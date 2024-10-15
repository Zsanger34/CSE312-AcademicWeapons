from flask import Flask
from .routes import main_routes
from .settings import settings_routes

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(settings_routes)

    return app
