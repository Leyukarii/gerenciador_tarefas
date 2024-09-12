from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from app.models import User, Task

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
