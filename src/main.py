import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.models.note import Note
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Enable CORS for all routes
CORS(app)

# register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')

# Database configuration - Supabase PostgreSQL ONLY
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    # For Vercel deployment, this should be set in environment variables
    # Don't exit in serverless environment, just log the error
    import logging
    logging.error("❌ ERROR: DATABASE_URL environment variable is required!")
    # Use a default that will cause a clear error later
    DATABASE_URL = "postgresql://missing:missing@missing:5432/missing"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database connection
db.init_app(app)

# Health check endpoint for Vercel debugging
@app.route('/health')
def health_check():
    """Health check endpoint to verify deployment"""
    return {
        'status': 'healthy',
        'database_configured': bool(os.environ.get('DATABASE_URL')),
        'github_token_configured': bool(os.environ.get('GITHUB_TOKEN')),
        'environment': os.environ.get('VERCEL_ENV', 'local')
    }

# API status endpoint
@app.route('/api/status')
def api_status():
    """API status endpoint"""
    try:
        # Test database connection if configured
        db_status = 'not_configured'
        if os.environ.get('DATABASE_URL'):
            try:
                from sqlalchemy import text
                with app.app_context():
                    db.session.execute(text('SELECT 1'))
                    db.session.commit()
                db_status = 'connected'
            except Exception as e:
                db_status = f'error: {str(e)[:100]}'
        
        return {
            'api': 'online',
            'database': db_status,
            'translation': 'configured' if os.environ.get('GITHUB_TOKEN') else 'not_configured'
        }
    except Exception as e:
        return {'error': str(e)}, 500

# Database connection test - only for local development
# In Vercel, this will be tested on first request, not at startup
def test_database_connection():
    """Test database connection - called lazily on first request"""
    try:
        from sqlalchemy import text
        with app.app_context():
            result = db.session.execute(text('SELECT 1'))
            db.session.commit()
            return True
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return False

# Only test connection in local development, not in Vercel
if __name__ == '__main__':
    with app.app_context():
        if test_database_connection():
            print("✅ Database connection successful!")
        else:
            print("❌ Database connection failed - check your .env file")
            sys.exit(1)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

# Export app for Vercel - this is the key for serverless deployment
# Remove the duplicate assignment
