from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__,instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),  # Sử dụng os.getenv() để lấy biến môi trường
            SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DB_URI"),
            JWT_SECRET_KEY =os.getenv("JWT_SECRET_KEY")
            )
    else: 
        app.config.from_mapping(
            test_config
        )
    
    db.app =app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    return app