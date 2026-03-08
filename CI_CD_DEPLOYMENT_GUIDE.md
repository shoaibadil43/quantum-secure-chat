# 🚀 CI/CD Deployment Guide - Quantum Secure Chat

## Complete Workflow: From GitHub to Live Deployment

This guide explains the automated CI/CD pipeline for your Quantum Secure Chat app.

---

## 📋 What is CI/CD?

**CI/CD** = **Continuous Integration / Continuous Deployment**

- **Continuous Integration (CI)**: Automatically test code when you push to GitHub
- **Continuous Deployment (CD)**: Automatically deploy the app when tests pass

**In simple terms**: Push code to GitHub → Automatic tests run → If tests pass → App auto-deploys to the web

---

## 🔧 Current Setup

Your project now includes:

### ✅ Git Configuration
- `.gitignore` - Prevents sensitive files from being uploaded
- GitHub repository ready for connection
- Initial commit with all code

### ✅ CI/CD Pipelines (GitHub Actions)
- `.github/workflows/frontend-build.yml` - Tests and builds Flutter web app
- `.github/workflows/backend-test.yml` - Tests backend API

### ✅ Deployment Configuration
- `vercel.json` - Configuration for Vercel deployment
- Environment variable setup for secure URLs
- Production-ready build settings

### ✅ Code Configuration
- `frontend/lib/config/backend_config.dart` - Centralized API URL configuration
- Can be updated without rebuilding code
- Supports development and production environments

---

## 🎯 STEP-BY-STEP: Complete CI/CD Setup

### **STEP 1: Create GitHub Repository** 
*(Takes 5 minutes)*

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name**: `quantum-secure-chat`
   - **Description**: `Real-Time Quantum Secure Chat App with BB84 Encryption`
   - **Visibility**: Public (or Private if you prefer)
   - **DO NOT initialize with README** (we already have code)
3. Click "Create repository"
4. You'll see instructions - **copy the commands**

### **STEP 2: Push Code to GitHub**
*(Takes 2 minutes)*

Run these commands in your terminal:

```bash
cd c:\Users\shaik\OneDrive\Desktop\quantum-secure-chat

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/quantum-secure-chat.git

# Rename branch to 'main' (GitHub default)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 250+, done.
Counting objects: 100% (250/250), done.
...
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

Now visit: `https://github.com/YOUR_USERNAME/quantum-secure-chat`
You should see all your code!

### **STEP 3: Set Up Vercel Account**
*(Takes 3 minutes)*

1. Go to https://vercel.com
2. Click "Sign Up" → Use GitHub account (recommended)
3. Authorize Vercel to access your GitHub
4. Click "Create Team" or "Continue" (skip if prompted)
5. You're ready for the next step!

### **STEP 4: Connect GitHub to Vercel (Automatic Deployment)**
*(Takes 5 minutes)*

1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select **"GitHub"** → Authorize if needed
4. Find and click on `quantum-secure-chat` repository
5. **Configure Project**:
   - Framework Preset: **Other** (Flutter Web)
   - Root Directory: `./` (keep default)
   - Build Command: `cd frontend && flutter build web --release`
   - Output Directory: `frontend/build/web`
6. **Environment Variables** - Add these:
   - Key: `BACKEND_API_URL` | Value: `http://192.168.29.109:8000/api`
   - Key: `BACKEND_WS_URL` | Value: `ws://192.168.29.109:8000/api/ws/chat`
   
   *(Later, change to your deployed backend URL)*

7. Click "Deploy"
8. **Wait 3-5 minutes** for build to complete
9. You'll get a deployment URL! 🎉

---

## 📱 YOUR APP IS NOW LIVE!

Once deployed, you'll have a URL like:
```
https://quantum-secure-chat-xxxxx.vercel.app
```

**Share this URL with anyone - they can use the app worldwide!**

---

## 🔄 The Automatic Deployment Process

Now that everything is connected, here's what happens automatically:

```
You make changes to code
              ↓
You commit: git commit -m "message"
              ↓
You push: git push
              ↓
GitHub receives your code
              ↓
GitHub Actions run tests automatically
  ├─ Frontend builds and tests
  ├─ Backend runs pytest
  └─ If all pass → Deploy signal sent to Vercel
              ↓
Vercel receives deploy signal
              ↓
Vercel automatically:
  ├─ Pulls latest code from GitHub
  ├─ Runs build command (flutter build web)
  ├─ Tests the build
  └─ Deploys to production
              ↓
Your app is updated automatically! ✅
              ↓
You can access new version at your Vercel URL
```

---

## 🔐 Environment Variables & Secrets

### What are they?
Environment variables let you change settings **without editing code**.

### Where to set them?
1. **Development (Local)**:
   - Create `frontend/.env.local` (in .gitignore)
   - Add your local backend URL

2. **Production (Vercel)**:
   - Settings → Project Settings → Environment Variables
   - Add variables there
   - They're injected during build

### Key Variables:
- `BACKEND_API_URL` - REST API endpoint
- `BACKEND_WS_URL` - WebSocket endpoint
- `ENVIRONMENT` - 'development' or 'production'

### Updating Backend URL:
When you deploy your backend to Render/Railway:

1. Get your backend URL: `https://your-backend.onrender.com`
2. Go to Vercel dashboard
3. Select your project → Settings → Environment Variables
4. Update `BACKEND_API_URL` to your new backend URL
5. **Redeploy** by pushing an empty commit:
   ```bash
   git commit --allow-empty -m "Trigger redeploy with new backend URL"
   git push
   ```

---

## 📝 Simple Update Workflow

**This is what you'll do every time you update the app:**

```bash
# 1. Make changes to your code (edit files in VS Code)

# 2. Stage the changes
git add .

# 3. Create a commit
git commit -m "Add new feature: [describe what you changed]"

# 4. Push to GitHub
git push

# That's it! The rest is automatic:
# - GitHub tests the code
# - If tests pass, Vercel deploys
# - Your app updates automatically
```

### Example commits:
```bash
git commit -m "Fix: Login validation error"
git commit -m "Feature: Add user search functionality"
git commit -m "Update: Improve message UI styling"
git commit -m "Bugfix: WebSocket connection timeout"
```

---

## 🛠️ Troubleshooting

### Build failing in GitHub Actions?
1. Go to your GitHub repo
2. Click "Actions" tab
3. See which workflow failed (Frontend or Backend)
4. Click on it to see error details
5. Fix the error in VS Code
6. Push again: `git add . && git commit -m "Fix" && git push`

### Deployment failed in Vercel?
1. Go to https://vercel.com/dashboard
2. Select your project
3. Click "Deployments"
4. Find the failed deployment
5. Click it to see error logs
6. Common fixes:
   - Backend URL is wrong or unreachable
   - Build command uses wrong path
   - Output directory doesn't exist

### App not loading?
1. Check browser console (F12)
2. Look for API errors
3. Verify backend URL in environment variables
4. Ensure backend is running

---

## 🚨 When Something Goes Wrong

**If your deployed app breaks:**

1. **Quick fix**:
   ```bash
   # Revert to previous version
   git revert HEAD
   git push
   # This undoes the last change and redeploys
   ```

2. **Check what broke**:
   - GitHub Actions: See which test failed
   - Vercel: Check deployment logs
   - Browser Console: See JavaScript errors (F12)

3. **Deploy immediately**:
   - No need to wait - just push code and Vercel auto-deploys
   - Takes 3-5 minutes usually
   - Check deployment status on Vercel dashboard

---

## 📊 Your CI/CD Dashboard

### GitHub (github.com/YOUR_USERNAME/quantum-secure-chat)
- **Commits** tab: See all your pushes
- **Actions** tab: See automated tests
- **Settings** tab: Manage repository

### Vercel (vercel.com/dashboard)
- See all deployments
- Check deployment logs
- View custom domains
- Manage environment variables

### GitHub Actions
- **Automatic testing** on every push
- **Build logs** show any errors
- **Test results** displayed in Actions tab

---

## 🎯 Commands You'll Use Regularly

```bash
# See status of your changes
git status

# Stage all changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub (triggers CI/CD)
git push

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## ✅ Success Checklist

- [x] Git repository initialized locally
- [x] GitHub repository created
- [x] Code pushed to GitHub
- [x] GitHub Actions workflows set up
- [x] Vercel account created
- [ ] GitHub connected to Vercel
- [ ] First deploy to Vercel completed
- [ ] App is live and accessible
- [ ] Environment variables set in Vercel

---

## 🎉 You're All Set!

Your app is now ready for:
- ✅ Automatic testing on every push
- ✅ Automatic deployment on every commit
- ✅ Easy rollback if something breaks
- ✅ Team collaboration via GitHub
- ✅ Instant global updates

## 📱 What Users Can Do

**Your Vercel URL** can be shared with anyone:
- Open in browser
- Works on mobile, tablet, desktop
- Create account
- Start chatting securely
- All in real-time!

---

## 🚀 Next Steps

1. Follow STEP 1-4 above to complete setup
2. Make a test change to verify auto-deployment works
3. Share your Vercel URL with friends
4. Use simple `git push` workflow for all future updates

**Questions?** Refer to individual section headings above!
