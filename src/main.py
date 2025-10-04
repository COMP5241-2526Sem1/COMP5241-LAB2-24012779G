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
    print("❌ ERROR: DATABASE_URL environment variable is required!")
    print("Please set your Supabase PostgreSQL connection string in .env file")
    print("Format: postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres")
    print("📖 Check SUPABASE_SETUP_GUIDE.md for detailed instructions")
    sys.exit(1)

# Validate Supabase URL format
if "supabase.co" in DATABASE_URL and "pooler.supabase.com" not in DATABASE_URL:
    print("⚠️  WARNING: Your DATABASE_URL appears to use the old Supabase format!")
    print("Old format: db.xxxxx.supabase.co")
    print("New format: aws-0-[region].pooler.supabase.com")
    print("Please update your DATABASE_URL in .env file")
    print("📖 Check SUPABASE_SETUP_GUIDE.md for help")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
print(f"🔗 Using Supabase PostgreSQL: {DATABASE_URL[:50]}...")  # Only show first 50 chars for security

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database tables
with app.app_context():
    try:
        # Test database connection first
        from sqlalchemy import text
        result = db.session.execute(text('SELECT 1'))
        db.session.commit()
        print("✅ Database connection successful!")
        
        # Note: Tables should be created manually in Supabase SQL Editor
        # using the supabase_setup.sql file provided
        print("📝 Make sure you've run the SQL setup in Supabase dashboard")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your DATABASE_URL in .env file")
        print("Make sure your Supabase project is active and URL is correct")
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

# Export app for Vercel
app = app
