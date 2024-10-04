from flask import Flask
from .routes import main_routes
from .register_path import register_route

def create_app():
    app = Flask(__name__)
    
    # Register Blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(register_route)

    return app
