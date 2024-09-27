from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from src.extension import mail
import os
from dotenv import load_dotenv
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db
from flasgger import Swagger


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY="dev",  # Gán cứng giá trị SECRET_KEY
            SQLALCHEMY_DATABASE_URI="sqlite:///bookmarks.db",  # Gán cứng giá trị URI
            JWT_SECRET_KEY="JWT_KEY",  # Gán cứng giá trị JWT_SECRET_KEY
            MAIL_SERVER="sandbox.smtp.mailtrap.io",  # Gán cứng giá trị MAIL_SERVER
            MAIL_PORT=2525,  # Gán cứng giá trị MAIL_PORT
            MAIL_USERNAME="3854a770817c8c",  # Gán cứng giá trị MAIL_USERNAME
            MAIL_PASSWORD="31f48ad412de14",  # Gán cứng giá trị MAIL_PASSWORD
            MAIL_USE_TLS=True,  # Gán cứng giá trị MAIL_USE_TLS
            MAIL_USE_SSL=False,  # Gán cứng giá trị MAIL_USE_SSL
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    JWTManager(app)
    mail.init_app(app)
    swagger = Swagger(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    # Looking to send emails in production? Check out our Email API/SMTP product!
    return app
