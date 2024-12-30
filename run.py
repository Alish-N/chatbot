from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Get host from environment variable or default to '0.0.0.0'
    host = os.getenv('HOST', '0.0.0.0')
    
    # Get debug mode from environment variable or default to True
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    ) 