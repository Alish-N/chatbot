from app import create_app
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = create_app()

# Configure CORS for the entire application
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://localhost:3000",  # If you have a separate frontend
            os.getenv('FRONTEND_URL', '*')  # Allow configurable frontend URL
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Get host from environment variable or default to '0.0.0.0'
    host = os.getenv('HOST', '0.0.0.0')
    
    # Get debug mode from environment variable or default to True
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Add logging for debugging
    if debug:
        import logging
        logging.getLogger('flask_cors').level = logging.DEBUG
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    ) 