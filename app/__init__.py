from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    with app.app_context():
        from .models import User, Task
        db.create_all()

    from .routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
