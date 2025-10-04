# Deployment Guide: Supabase + Vercel

## 🗄️ Step 1: Set up Supabase Database

1. **Create a Supabase account** at https://supabase.com
2. **Create a new project**
3. **Get your database URL:**
   - Go to Project Settings → Database
   - Copy the "Connection string" under "Connection pooling"
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@[PROJECT-REF].supabase.co:5432/postgres`

## 🚀 Step 2: Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy from your project directory:**
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel:**
   - Go to your Vercel dashboard
   - Select your project → Settings → Environment Variables
   - Add these variables:
     ```
     DATABASE_URL=your-supabase-connection-string
     SECRET_KEY=your-secure-secret-key
     GITHUB_TOKEN=your-github-token
     ```

4. **Redeploy** to apply environment variables:
   ```bash
   vercel --prod
   ```

## 🧪 Step 3: Test Local Development

1. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. **Add your credentials** to `.env`:
   ```
   DATABASE_URL=your-supabase-connection-string
   SECRET_KEY=your-secure-secret-key
   GITHUB_TOKEN=your-github-token
   ```

3. **Install new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally:**
   ```bash
   python src/main.py
   ```

## 📋 What Changed

- ✅ Added PostgreSQL support with `psycopg2-binary`
- ✅ Environment variable support with `python-dotenv`
- ✅ Vercel deployment configuration in `vercel.json`
- ✅ Fallback to SQLite for local development
- ✅ Better error handling for database initialization
- ✅ AI-powered translation feature with GitHub Models API (using requests)
- ✅ Chinese translation display in note list
- ✅ Translation API endpoint and frontend integration

## 🔧 Troubleshooting

**Translation errors:**
- Verify your GitHub token has access to GitHub Models
- Check if the GitHub Models API is available in your region
- Ensure GITHUB_TOKEN environment variable is set correctly
- Test the translation service with the test script

**Database connection errors:**
- Verify your Supabase connection string
- Check if your Supabase project is active
- Ensure environment variables are set correctly in Vercel

**Vercel deployment issues:**
- Check the build logs in Vercel dashboard
- Verify `vercel.json` configuration
- Ensure all dependencies are in `requirements.txt`