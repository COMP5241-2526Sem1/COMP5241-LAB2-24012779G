# NoteTaker - AI Coding Guidelines

## Architecture Overview

This is a Flask-based note-taking web application with a SQLAlchemy backend and vanilla JavaScript frontend served as static files.

**Key Components:**
- `src/main.py` - Flask app entry point with static file serving and database initialization
- `src/models/` - SQLAlchemy models (Note, User) with shared `db` instance from `user.py`
- `src/routes/` - Flask blueprints registered with `/api` prefix
- `src/static/index.html` - Single-page application with embedded CSS/JS

## Critical Patterns

### Database Setup
- **Production**: Uses Supabase PostgreSQL via `DATABASE_URL` environment variable
- **Development**: Falls back to SQLite at `ROOT_DIR/database/app.db` if no `DATABASE_URL`
- `db` instance is imported from `src.models.user`, NOT instantiated in models
- All models must import: `from src.models.user import db`
- Environment variables loaded via `python-dotenv`

### Deployment Configuration
- **Vercel**: Configured via `vercel.json` with serverless Python runtime
- **Environment Variables**: `DATABASE_URL`, `SECRET_KEY` set in Vercel dashboard
- **Local Development**: Uses `.env` file (copy from `.env.example`)

### API Structure
- All routes use Flask blueprints with `/api` prefix
- Note routes follow RESTful patterns: `GET /api/notes`, `POST /api/notes`, `PUT /api/notes/<id>`
- Search endpoint: `GET /api/notes/search?q=<query>` using SQLAlchemy `.contains()`
- All models have `.to_dict()` method for JSON serialization

### Frontend Integration
- Single HTML file at `src/static/index.html` with embedded CSS and JavaScript
- API calls use relative URLs (e.g., `/api/notes`) 
- Auto-save functionality with debounced saves every 2 seconds
- Frontend uses vanilla JavaScript class `NoteTaker` for state management

### Error Handling
- Routes use try/catch with `db.session.rollback()` on errors
- Frontend shows user messages via `showMessage()` method
- All database operations wrapped in sessions with proper cleanup

## Development Workflow

**Local setup:**
```bash
cp .env.example .env  # Add your Supabase credentials
pip install -r requirements.txt
python src/main.py    # App runs on http://localhost:5001
```

**Deploy to Vercel:**
```bash
vercel  # Follow prompts, set DATABASE_URL and SECRET_KEY in dashboard
```

**Key files to modify:**
- Models: Add to `src/models/` and import db from `user.py`
- API endpoints: Add routes to existing blueprints in `src/routes/`
- Frontend: Modify the single `src/static/index.html` file

## Project Conventions

- Models use `updated_at` with `onupdate=datetime.utcnow` for automatic timestamps
- Route methods use descriptive docstrings
- Frontend uses grid layout with sidebar (notes list) and main editor
- Database queries ordered by `updated_at.desc()` for recent-first display
- No authentication system - single-user application