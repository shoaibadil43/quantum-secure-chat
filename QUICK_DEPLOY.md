# ⚡ QUICK DEPLOYMENT CHECKLIST

## Before You Start
- [ ] Have GitHub account with repo access
- [ ] Have credit card (for Heroku paid services)
- [ ] Have 30 minutes available
- [ ] All code is pushed to GitHub `main` branch

---

## PHASE 1: HEROKU SETUP (10 mins)

- [ ] Sign up at https://www.heroku.com
- [ ] Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- [ ] Run: `heroku login`
- [ ] Run: `heroku create quantum-secure-chat-api`
- [ ] Run: `heroku addons:create heroku-postgresql:hobby-dev`
- [ ] Get DATABASE_URL from: `heroku config`

---

## PHASE 2: SET BACKEND SECRETS (5 mins)

```bash
# Generate secure keys
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
MASTER_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')

# Set on Heroku
heroku config:set SECRET_KEY=$SECRET_KEY MASTER_KEY=$MASTER_KEY
```

---

## PHASE 3: DEPLOY BACKEND (5 mins)

```bash
cd quantum-secure-chat

# Connect to Heroku
git remote add heroku https://git.heroku.com/quantum-secure-chat-api.git

# Deploy
git push heroku main

# Watch logs
heroku logs --tail
```

✅ When you see "Application running on 0.0.0.0:8000" → Success!

---

## PHASE 4: VERCEL FRONTEND (10 mins)

- [ ] Go to https://vercel.com
- [ ] Click "New Project"
- [ ] Select your GitHub repo
- [ ] Set these:
  - **Build Command**: `cd frontend && flutter build web --release`
  - **Output Directory**: `frontend/build/web`
- [ ] Add Environment Variable:
  - `BACKEND_API_URL` = `https://your-heroku-app.herokuapp.com/api`
- [ ] Click Deploy

✅ When deployment is green → Success!

---

## PHASE 5: CONNECT THEM (5 mins)

In `frontend/lib/services/api_service.dart`:
```dart
static const String _baseUrl = 'https://your-heroku-app.herokuapp.com/api';
```

Push to GitHub:
```bash
git add .
git commit -m "Update backend URL"
git push origin main
```

---

## PHASE 6: TEST (5 mins)

- [ ] Open your Vercel app in browser
- [ ] Try Sign Up
- [ ] Check Heroku logs: `heroku logs --tail`
- [ ] If error, see TROUBLESHOOTING section

---

## DONE! 🎉

Your app is now **live worldwide** at:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-app.herokuapp.com`
- API Docs: `https://your-app.herokuapp.com/docs`

Everyone can now access your app!

---

## If Something Goes Wrong

**Backend won't start?**
```bash
heroku logs --tail
# Check for database connection errors
```

**CORS errors?**
```bash
# Update backend/app/config.py with your Vercel URL
# Then: git push heroku main
```

**Frontend blank page?**
```bash
# Check browser console (F12)
# Check Vercel Deployments tab
```

**Database issues?**
```bash
heroku pg:info
heroku pg:psql  # Access database directly
```

---

**Questions? Check DEPLOYMENT_GUIDE.md for full details**

