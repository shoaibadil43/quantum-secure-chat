# Global Deployment Guide - Quantum Secure Chat

This guide will help you deploy your app to a global host so anyone in the world can access it.

## Overview

The app consists of two parts:
1. **Backend API** (FastAPI) - Runs the chat server and handles authentication
2. **Frontend Web App** (Flutter Web) - User interface accessible in any browser

## Deployment Strategy

We recommend using these free services:
- **Backend**: Railway.app or Render.com
- **Frontend**: Vercel or Netlify

---

## Option 1: Deploy Backend to Railway.app (Recommended)

Railway.app is the easiest option - no git required!

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click "Start Project"
3. Sign up with GitHub/Google/Email
4. Create a new project

### Step 2: Deploy Backend
Railway is paid now, but you can use **Render.com** instead (free tier with limitations):

**Alternative: Deploy Backend to Render.com**

1. Go to https://render.com
2. Sign up (free account)
3. Click "Create +" → "Web Service"
4. Connect your GitHub repository (you'll need to create one first)
5. Select the repository
6. Configure:
   - **Name**: `quantum-secure-chat-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Environment Variables**:
     - `DATABASE_URL`: (Can use SQLite for now)
7. Click "Create Web Service"
8. Once deployed, you'll get a URL like: `https://quantum-secure-chat-backend-xxxx.onrender.com`

**NOTE**: Copy this URL, you'll need it for the frontend!

---

## Option 2: Deploy Backend to Heroku (Legacy - May Cost Money Now)

Heroku is no longer free, so we don't recommend it.

---

## Deploy Frontend to Vercel (Recommended)

### Step 1: Prepare Git Repository
1. Open your project folder in VS Code
2. Open terminal and run:
```bash
cd c:\Users\shaik\OneDrive\Desktop\quantum-secure-chat
git init
git add .
git commit -m "Initial commit"
```

3. Create GitHub repository:
   - Go to https://github.com/new
   - Create a repository named `quantum-secure-chat`
   - Don't initialize with README
   - Copy the commands shown and run them in your terminal:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/quantum-secure-chat.git
   git push -u origin main
   ```

### Step 2: Update Backend URL in Frontend

Before deploying, update the API endpoint in your frontend:

**File**: `frontend/lib/services/api_service.dart`

Find this line:
```dart
const String BACKEND_URL = 'http://192.168.29.109:8000/api';
```

Replace it with your Render.com backend URL:
```dart
const String BACKEND_URL = 'https://quantum-secure-chat-backend-xxxx.onrender.com/api';
```

Also update WebSocket URL to:
```dart
static const String _baseUrl = 'wss://quantum-secure-chat-backend-xxxx.onrender.com/api/ws/chat';
```

Then commit and push:
```bash
git add -A
git commit -m "Update backend URL to global host"
git push
```

### Step 3: Deploy to Vercel

1. Go to https://vercel.com
2. Sign up (free account)
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Configure:
   - **Framework**: Select "Other"
   - **Build Command**: `cd frontend && flutter build web --release`
   - **Output Directory**: `frontend/build/web`
6. Click "Deploy"
7. Your frontend will be live at: `https://quantum-secure-chat-xxxx.vercel.app`

---

## Alternative: Deploy Frontend to Firebase Hosting

1. Go to https://console.firebase.google.com
2. Create a new project
3. Run:
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
```
4. Select the Firebase project
5. Deploy:
```bash
firebase deploy
```

---

## Alternative: Deploy Frontend to Netlify (No Git Required!)

1. Go to https://netlify.com
2. Sign up (free account)
3. Drag and drop your `frontend/build/web` folder to Netlify
4. Your frontend will be live immediately!

**This is the EASIEST option if you don't want to use Git!**

---

## Final Setup: Update API URLs

After deployment, you need to tell the app where the backend is running.

Update in: `frontend/lib/services/api_service.dart`

```dart
const String BACKEND_URL = 'https://quantum-secure-chat-backend-xxxx.onrender.com/api';
```

Then rebuild and redeploy the frontend.

---

## Quick Start Summary

For the absolute fastest global deployment:

1. **Backend**: Deploy code from `backend/` folder to Render.com
2. **Frontend**: Drag `frontend/build/web/` folder to Netlify
3. **Update API URL** in frontend code
4. **Rebuild and redeploy** frontend with the new URL

---

## Testing Your Global App

Once deployed:
1. Visit your Vercel/Netlify URL in browser
2. Create a new account (registration works with real database now)
3. Login with your account
4. You'll see a list of all registered users
5. Click on any user to start a secure chat conversation

**Note**: WebSocket messaging (real-time chat) will work when both users are online

---

## Troubleshooting

### Backend URL showing 404
- Make sure backend is deployed and running
- Check your Render/Railway dashboard for logs
- Verify the URL is correct in `api_service.dart`

### Can't register new users
- Database needs to be set up on backend
- Check the Render/Railway logs for database errors
- May need to configure PostgreSQL database on Render

### Frontend not showing users
- Verify backend is responding: Visit `https://your-backend-url/`
- Check browser console (F12) for error messages
- Verify API calls in Developer Tools Network tab

---

## Security Notes

⚠️ **IMPORTANT**: This is a development setup. For production:
- Use HTTPS everywhere (hosting services do this automatically)
- Set proper environment variables (API keys, database URLs)
- Enable CORS properly for your specific domain
- Use strong JWT secrets
- Implement rate limiting
- Add monitoring and logging

---

## Support

For detailed documentation, see:
- Backend: `docs/API_DOCUMENTATION.md`
- Architecture: `docs/ARCHITECTURE.md`
- Deployment: `docs/DEPLOYMENT.md`
