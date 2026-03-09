# 🚀 QUANTUM SECURE CHAT - COMPLETE DEPLOYMENT GUIDE

## Your Deployment Targets
- **Backend**: Heroku (FastAPI)
- **Frontend**: Vercel (Flutter Web)
- **Database**: PostgreSQL on Heroku
- **Cache**: Redis (free tier available)

---

## STEP 1: PREPARE GITHUB REPOSITORY

```bash
# 1. Clone your repo locally
git clone https://github.com/shoaibadil43/quantum-secure-chat.git
cd quantum-secure-chat

# 2. Ensure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

---

## STEP 2: DEPLOY BACKEND TO HEROKU

### 2.1 Create Heroku Account & Install CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# After installation, login:
heroku login
```

### 2.2 Create Heroku App
```bash
# Create app on Heroku
heroku create quantum-secure-chat-backend

# Or use existing app:
heroku apps:create --region us quantum-secure-chat-api
```

### 2.3 Add PostgreSQL Database
```bash
# Add PostgreSQL to your Heroku app
heroku addons:create heroku-postgresql:hobby-dev --app quantum-secure-chat-backend

# Check database URL
heroku config --app quantum-secure-chat-backend
```

### 2.4 Add Redis (Caching & Sessions)
```bash
# Add Redis using Heroku Redis
heroku addons:create heroku-redis:premium-0 --app quantum-secure-chat-backend

# Or use free external Redis:
# Sign up at https://redis.io/try-free/
```

### 2.5 Set Environment Variables on Heroku
```bash
heroku config:set \
  SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" \
  MASTER_KEY="$(python -c 'import secrets; print(secrets.token_hex(16))')" \
  DEBUG=False \
  --app quantum-secure-chat-backend
```

### 2.6 Deploy to Heroku
```bash
# Add Heroku remote
git remote add heroku https://git.heroku.com/quantum-secure-chat-backend.git

# Deploy code
git push heroku main

# View logs
heroku logs --tail --app quantum-secure-chat-backend
```

### 2.7 Migrate Database (if needed)
```bash
# If you added migrations
heroku run python -m alembic upgrade head --app quantum-secure-chat-backend
```

✅ **Your backend is now live at**: `https://quantum-secure-chat-backend.herokuapp.com`

---

## STEP 3: DEPLOY FRONTEND TO VERCEL

### 3.1 Build Flutter Web Version
```bash
cd frontend

# Get dependencies
flutter pub get

# Build web version
flutter build web --release
```

### 3.2 Create Vercel Configuration

In your `frontend/` directory, create `vercel.json`:
```json
{
  "buildCommand": "flutter build web --release",
  "outputDirectory": "build/web"
}
```

### 3.3 Deploy to Vercel
```bash
# Option A: Install Vercel CLI
npm i -g vercel

# Deploy
vercel --cwd frontend

# Option B: Use GitHub Integration
# 1. Go to https://vercel.com/new
# 2. Select your GitHub repo
# 3. Set build command: flutter build web --release
# 4. Set output dir: build/web
# 5. Click Deploy
```

✅ **Your frontend is now live at**: `https://your-app.vercel.app`

---

## STEP 4: CONNECT FRONTEND TO BACKEND

### 4.1 Update Frontend Configuration
Edit `frontend/lib/services/api_service.dart`:

```dart
class APIService {
  static const String _baseUrl = 'https://quantum-secure-chat-backend.herokuapp.com/api';
  // ... rest of code
}
```

### 4.2 Update Backend CORS
Edit `backend/app/config.py`:

```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-app.vercel.app",  # Your Vercel URL
]
```

### 4.3 Re-deploy Both
```bash
# Backend
git push heroku main

# Frontend  
git push
# Vercel auto-deploys on push
```

---

## STEP 5: SET UP ENVIRONMENT VARIABLES

### Heroku
```bash
heroku config:set \
  DATABASE_URL="postgres://..." \
  REDIS_URL="redis://..." \
  SECRET_KEY="your-key" \
  CORS_ORIGINS="https://your-app.vercel.app" \
  --app quantum-secure-chat-backend
```

### Vercel
```bash
# In Vercel dashboard:
# Settings > Environment Variables

BACKEND_API_URL=https://quantum-secure-chat-backend.herokuapp.com/api
BACKEND_WS_URL=wss://quantum-secure-chat-backend.herokuapp.com/api/ws/chat
```

---

## STEP 6: TEST THE DEPLOYMENT

### 6.1 Test Backend Health
```bash
curl https://quantum-secure-chat-backend.herokuapp.com/docs
```

### 6.2 Test Frontend
- Open `https://your-app.vercel.app` in browser
- Try Sign Up flow
- Check backend logs for requests

### 6.3 Check Logs
```bash
# Backend logs
heroku logs --tail --app quantum-secure-chat-backend

# Frontend logs (in Vercel dashboard)
```

---

## TROUBLESHOOTING

### Backend Issues
```bash
# Check app status
heroku ps --app quantum-secure-chat-backend

# Restart app
heroku restart --app quantum-secure-chat-backend

# View recent deploys
heroku releases --app quantum-secure-chat-backend
```

### Database Issues
```bash
# Check database connection
heroku pg:info --app quantum-secure-chat-backend

# Access database
heroku pg:psql --app quantum-secure-chat-backend
```

### CORS Errors
- Add your frontend URL to `CORS_ORIGINS` in backend config
- Re-deploy backend with `git push heroku main`

---

## QUICK REFERENCE COMMANDS

```bash
# Heroku
heroku login
heroku create app-name
heroku config:set KEY=VALUE
git push heroku main
heroku logs --tail

# Vercel
vercel --cwd frontend
vercel env add
vercel deploy

# Git
git add .
git commit -m "message"
git push origin main
```

---

## COSTS

| Service | Free Tier | Monthly Cost |
|---------|-----------|--------------|
| Heroku Backend | ❌ (eco dyno $5) | $5-50 |
| PostgreSQL | ✅ (20MB) | $9+ |
| Redis | ❌ | $15+ |
| Vercel Frontend | ✅ | $0 |
| **TOTAL** | | **$30+/month** |

---

## SUPPORT

If you encounter issues:
1. Check Heroku logs: `heroku logs --tail`
2. Check Vercel logs: Vercel dashboard
3. Check GitHub Actions: `.github/workflows/`

---

**Your app will be live and accessible worldwide! 🌍**

