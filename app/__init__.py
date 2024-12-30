from flask import Flask
from config import Config
from mongoengine import connect
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize MongoDB connection
    connect(host=app.config['MONGODB_URI'])
    
    # Register blueprints
    from app.routes import main
    from app.api import api
    
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    
    return app 