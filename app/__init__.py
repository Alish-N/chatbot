from flask import Flask
from config import Config
from mongoengine import connect

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize MongoDB connection
    connect(host=app.config['MONGODB_URI'])
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app 