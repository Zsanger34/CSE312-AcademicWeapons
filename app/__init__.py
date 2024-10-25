from flask import Flask
from .routes import main_routes
from .register_path import register_route
from .login_path import login_route
from .workout import workout_route
from .workout_routine import workoutroutine_route

def create_app():
    app = Flask(__name__)
    
    #blueprint routes
    app.register_blueprint(main_routes)
    app.register_blueprint(register_route)
    app.register_blueprint(login_route)
    app.register_blueprint(workout_route)
    app.register_blueprint(workoutroutine_route)

    return app
