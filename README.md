# NoteTaker - AI-Powered Personal Note Management Application

⭐ **Star this repository if you find it useful!**

A modern, responsive web application for managing personal notes with **AI translation capabilities** and cloud database integration.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **🤖 AI Translation**: Translate English notes to Chinese using GitHub Models API
- **☁️ Cloud Database**: Powered by Supabase PostgreSQL for scalability
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates
- **🚀 Vercel Ready**: Pre-configured for serverless deployment

## 🤖 AI Translation Feature

The app includes an intelligent translation system powered by **GitHub Models API**:

### How It Works
1. **Write in English**: Create notes in English as usual
2. **One-Click Translation**: Click the "🤖 Translate" button
3. **AI Processing**: GitHub's GPT-4o-mini model translates your content
4. **Instant Results**: Chinese translation appears alongside English
5. **Persistent Storage**: Both versions saved to Supabase database

### Translation Capabilities
- **Service**: GitHub Models API (GPT-4o-mini)
- **Languages**: English → Chinese (Simplified)
- **Content**: Translates both title and note content
- **Accuracy**: AI-powered for natural, contextual translations
- **Storage**: Translations stored in `title_zh` and `content_zh` fields

### Example Translation
```
English: "Welcome to NoteTaker"
Chinese: "欢迎使用记事本"

English: "This is a test note for the translation feature."
Chinese: "这是翻译功能的测试笔记。"
```

## 🌟 **This Project is Open Source!**

Feel free to:
- ⭐ **Star this repository** if you find it useful
- 🐛 **Report issues** if you find bugs
- 🔄 **Submit pull requests** for improvements
- 📧 **Contact me** for collaboration opportunities

## 👨‍💻 **About This Project**

This NoteTaker application demonstrates:
- **🎯 Full-stack web development** with Flask and PostgreSQL
- **🤖 AI integration** using GitHub Models API for translation
- **☁️ Cloud deployment** with Vercel and Supabase
- **⚡ Modern web technologies** and best practices
- **🔄 Database migration** from SQLite to cloud PostgreSQL
- **🎨 Responsive UI design** with modern CSS and JavaScript

## ⚡ Quick Start Guide

### 🚀 **New to the project?** Start here:

1. **📋 Prerequisites**: Python 3.11+, Supabase account, GitHub token
2. **⚙️ Windows Users**: Run `setup.cmd` then `start.cmd` 
3. **🐧 Linux/Mac Users**: Follow the detailed setup steps below
4. **🌐 Try Online**: Deploy to Vercel for instant cloud hosting
5. **🧪 Test Features**: Create notes, search, and try AI translation

### 🎯 **First-time Setup Checklist:**
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with Supabase and GitHub credentials
- [ ] Database tables created using `supabase_setup.sql`
- [ ] App running on `http://localhost:5001`
- [ ] Translation feature tested with sample note

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support
- **🤖 GitHub Models API**: AI-powered translation service

### Database
- **☁️ Supabase PostgreSQL**: Cloud-hosted, scalable database with real-time capabilities
- **🔄 Migration Ready**: Easily switch between local SQLite and cloud PostgreSQL

### Deployment
- **⚡ Vercel**: Serverless deployment platform with automatic scaling
- **🌍 Global CDN**: Fast content delivery worldwide

## 📁 Project Structure

```
note-taking-app/
├── src/
│   ├── models/
│   │   ├── user.py          # Database configuration and user model
│   │   └── note.py          # Note model with translation support
│   ├── routes/
│   │   ├── user.py          # User API routes
│   │   └── note.py          # Note API endpoints + translation
│   ├── services/
│   │   └── translation.py   # GitHub Models API translation service
│   ├── static/
│   │   ├── index.html       # Frontend application with translation UI
│   │   └── favicon.ico      # Application icon
│   └── main.py              # Flask application entry point
├── .venv/                   # Python virtual environment
├── .env                     # Environment variables (Supabase, GitHub token)
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment configuration
├── start.cmd                # Windows startup script
├── setup.cmd                # Windows setup script
├── supabase_setup.sql       # Database schema for Supabase
└── README.md               # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
- **GitHub Account**: For GitHub Models API access

### Installation Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd note-taking-app
   ```

2. **Set up environment** (Windows users can use `setup.cmd`)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   
   **Linux/Mac:**
   ```bash
   source .venv/bin/activate
   ```
   
   **Windows:**
   ```cmd
   .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file and add:
   ```properties
   # Supabase PostgreSQL Database
   DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
   
   # GitHub Models API Token
   GITHUB_TOKEN=your_github_token_here
   
   # Flask Configuration
   SECRET_KEY=your-secret-key
   FLASK_ENV=development
   ```

6. **Set up Supabase database**
   - Go to your Supabase dashboard
   - Open SQL Editor
   - Run the SQL from `supabase_setup.sql`

7. **Run the application**
   
   **Option 1: Using the batch file (Windows - Recommended)**
   ```cmd
   start.cmd
   ```
   
   **Option 2: Manual command**
   ```bash
   python src/main.py
   ```

8. **Access the application**
   - Open your browser and go to `http://localhost:5001`

### 🧪 Testing Your Setup

**Test Database Connection:**
```bash
python test_supabase.py
```

**Test Translation Feature:**
1. Create a new note with English content
2. Click the "🤖 Translate" button
3. Watch as AI generates Chinese translation
4. Both versions are saved automatically

**Verify All Features:**
- ✅ Create, edit, delete notes
- ✅ Search functionality
- ✅ Auto-save capability  
- ✅ AI translation (English → Chinese)
- ✅ Responsive design on mobile

## 🖥️ Windows Batch Files

For Windows users, convenient batch files are provided:

### `start.cmd` - Main startup script
- Comprehensive startup with error checking
- Automatically activates virtual environment
- Checks and installs dependencies
- Provides helpful status messages
- **Usage**: Double-click `start.cmd` or run from command line

### `start-simple.cmd` - Quick start
- Minimal startup script for advanced users
- **Usage**: `start-simple.cmd`

### `setup.cmd` - Initial setup
- Sets up virtual environment
- Installs all dependencies
- Run this once before using `start.cmd`
- **Usage**: `setup.cmd`

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes
- **🤖 `POST /api/notes/<id>/translate`** - Translate note to Chinese using AI

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "title_zh": "我的笔记标题",
  "content_zh": "这里是笔记内容...",
  "created_at": "2025-10-04T11:26:38.123456",
  "updated_at": "2025-10-04T11:27:30.654321"
}
```

### Translation API Response
```json
{
  "success": true,
  "message": "Note translated successfully",
  "translations": {
    "title_zh": "我的笔记标题",
    "content_zh": "这里是笔记内容..."
  }
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **🤖 Translate Button**: AI-powered English to Chinese translation
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Translation Display**: View Chinese translations alongside English content
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### Notes Table (Supabase PostgreSQL)
```sql
CREATE TABLE note (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    title_zh VARCHAR(200),           -- Chinese translation of title
    content_zh TEXT,                 -- Chinese translation of content
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Automatic timestamp updates
CREATE TRIGGER update_note_updated_at
    BEFORE UPDATE ON note
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Performance indexes
CREATE INDEX idx_note_updated_at ON note(updated_at DESC);
CREATE INDEX idx_note_search ON note USING gin(to_tsvector('english', title || ' ' || content));
```

## 🚀 Deployment

### Vercel Deployment (Recommended)

The application is pre-configured for Vercel deployment:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel
   ```

3. **Set Environment Variables** in Vercel Dashboard:
   - `DATABASE_URL`: Your Supabase PostgreSQL connection string
   - `GITHUB_TOKEN`: Your GitHub Models API token
   - `SECRET_KEY`: Flask secret key for sessions

4. **Automatic Deployments**: Connected GitHub repository will auto-deploy on push

### Manual Server Deployment

For traditional server deployment:
- CORS enabled for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration
- Supabase PostgreSQL for scalable data persistence

### Configuration Files
- `vercel.json`: Vercel serverless configuration
- `requirements.txt`: Python dependencies for deployment
- `.env`: Environment variables (not committed to git)

## 🔧 Configuration

### Environment Variables (.env)
```properties
# Supabase PostgreSQL Database (Required)
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

# GitHub Models API Token (Required for translation)
GITHUB_TOKEN=your_github_token_here

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Database Configuration
- **Production**: Supabase PostgreSQL (cloud-hosted, scalable)
- **Development**: Same as production (no local SQLite fallback)
- **Automatic Migration**: Run `supabase_setup.sql` in Supabase dashboard
- **SQLAlchemy ORM**: For database operations and relationships

### AI Translation Configuration
- **Service**: GitHub Models API (gpt-4o-mini)
- **Languages**: English → Chinese (Simplified)
- **Rate Limits**: Managed by GitHub Models service
- **Error Handling**: Graceful fallback with user-friendly messages

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support & Troubleshooting

### Common Issues

**Database Connection Problems:**
1. Verify your Supabase DATABASE_URL in `.env`
2. Check if your Supabase project is active
3. Run `python test_supabase.py` to test connection
4. Ensure tables are created using `supabase_setup.sql`

**Translation Not Working:**
1. Verify GITHUB_TOKEN in `.env` file
2. Check GitHub Models API quota/limits
3. Ensure internet connection for API calls

**App Won't Start:**
1. Check if virtual environment is activated
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check console for error messages
4. Use `start.cmd` for automated startup (Windows)

### Getting Help
- Check browser console for error messages
- Verify the Flask server is running on port 5001
- Review server logs for database/API errors
- Test individual components using provided test scripts

### Log Files & Debugging
- Flask debug mode shows detailed error traces
- Database connection status printed on startup
- Translation API responses logged for debugging

## 🎯 Future Enhancements

Potential improvements for future versions:

### Core Features
- **Multi-language Support**: Extend translation beyond Chinese (Japanese, Korean, etc.)
- **User Authentication**: Multi-user support with secure login
- **Note Categories**: Organize notes with tags and folders
- **Rich Text Editor**: Bold, italic, lists, images, and formatting
- **File Attachments**: Upload and embed files, images, PDFs

### AI & Smart Features
- **AI Summarization**: Generate note summaries using LLMs
- **Smart Search**: Semantic search powered by vector embeddings
- **Auto-tagging**: AI-powered automatic categorization
- **Voice Notes**: Speech-to-text transcription
- **Smart Suggestions**: AI-powered writing assistance

### UI/UX Improvements
- **Dark/Light Theme**: Toggle between color schemes
- **Offline Support**: Service workers for offline functionality
- **Mobile App**: React Native or PWA mobile application
- **Collaborative Editing**: Real-time multi-user editing
- **Export Options**: PDF, Markdown, DOCX export

### Technical Enhancements
- **Real-time Sync**: WebSocket-based live updates
- **Advanced Search**: Full-text search with filters
- **API Authentication**: JWT-based secure API access
- **Backup & Restore**: Automated data backup systems
- **Performance**: Caching, pagination, lazy loading

---

**Built with ❤️ using Flask, Supabase, GitHub Models API, and modern web technologies**

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## ⭐ Show Your Support

If this project helped you, please consider giving it a ⭐ star on GitHub!

