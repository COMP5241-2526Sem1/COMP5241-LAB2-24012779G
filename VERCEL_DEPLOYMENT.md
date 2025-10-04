# Vercel Deployment Guide for NoteTaker

## 🚀 Quick Deployment Steps

### 1. **Connect Repository to Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your repository: `COMP5241-2526Sem1/COMP5241-LAB2-24012779G`

### 2. **Configure Environment Variables**
In Vercel Dashboard → Project Settings → Environment Variables, add:

```env
DATABASE_URL=postgresql://postgres.[your-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
GITHUB_TOKEN=your_github_token_here
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
```

### 3. **Deploy**
- Click "Deploy" - Vercel will automatically build and deploy
- Wait for deployment to complete (usually 1-2 minutes)

## 🔍 **Testing Your Deployment**

### Health Check Endpoints
After deployment, test these URLs:

1. **General Health**: `https://your-app.vercel.app/health`
   - Should return: `{"status": "healthy", "database_configured": true, ...}`

2. **API Status**: `https://your-app.vercel.app/api/status`
   - Should return: `{"api": "online", "database": "connected", ...}`

3. **Main App**: `https://your-app.vercel.app/`
   - Should load the NoteTaker interface

## ❌ **Common Issues & Solutions**

### Issue: "FUNCTION_INVOCATION_FAILED"
**Cause**: Missing environment variables or database connection issues
**Solution**: 
1. Check environment variables in Vercel dashboard
2. Test with `/health` endpoint
3. Verify Supabase database is active

### Issue: "Module not found" errors
**Cause**: Python import path issues
**Solution**: The new `api/index.py` should fix this

### Issue: Database connection timeout
**Cause**: Cold start delays
**Solution**: 
1. Vercel Pro has faster cold starts
2. Consider using connection pooling
3. Check Supabase connection limits

## 🔧 **Advanced Configuration**

### Vercel Settings
- **Runtime**: Python 3.9+ (automatic)
- **Function Timeout**: 30 seconds (configured in vercel.json)
- **Memory**: 1024MB (Vercel default)

### Performance Optimization
- **Static Files**: Served efficiently by Vercel CDN
- **Database**: Supabase provides connection pooling
- **Caching**: Consider adding Flask-Caching for API responses

## 📊 **Monitoring**

### Vercel Analytics
- Enable in Project Settings → Analytics
- Monitor function performance and errors

### Logs
- View real-time logs in Vercel Dashboard → Functions tab
- Use for debugging deployment issues

## 🛡️ **Security**

### Production Checklist
- ✅ Environment variables set in Vercel (not in code)
- ✅ Supabase database uses SSL (automatic)
- ✅ CORS properly configured for your domain
- ✅ Strong SECRET_KEY set
- ✅ GitHub token has minimal required permissions

## 🎯 **Next Steps**

1. **Custom Domain**: Add your own domain in Vercel settings
2. **Performance**: Enable Vercel Analytics
3. **Monitoring**: Set up alerts for function errors
4. **Backup**: Supabase provides automatic backups

---

**Need Help?** Check the Vercel logs for specific error messages!