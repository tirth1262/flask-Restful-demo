from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from office_management.config import Config
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from office_management.main.routes import main
        from office_management.users.routes import users

        app.register_blueprint(main)
        app.register_blueprint(users)

        return app
