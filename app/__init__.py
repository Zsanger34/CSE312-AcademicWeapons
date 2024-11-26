from flask import Flask
from .routes import main_routes
from .register_path import register_route
from .login_path import login_route
from app.posts_path import posts_bp
from app.get_posts import get_post_api
from .logout_path import logout_routes
from .create_routine import add_week_route

def create_app():
    app = Flask(__name__)
    
    #blueprint routes
    app.register_blueprint(main_routes)
    app.register_blueprint(register_route)
    app.register_blueprint(login_route)
    app.register_blueprint(posts_bp)
    app.register_blueprint(get_post_api)
    app.register_blueprint(logout_routes)
    app.register_blueprint(add_week_route)

    return app
