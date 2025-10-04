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
- Database path is `ROOT_DIR/database/app.db` (repository root, not src/)
- `db` instance is imported from `src.models.user`, NOT instantiated in models
- All models must import: `from src.models.user import db`

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

**Run locally:**
```bash
python src/main.py
# App runs on http://localhost:5001
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