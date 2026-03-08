# 🚀 QUICK REFERENCE - CI/CD Deployment

## One-Time Setup (First Time Only) - 15 minutes

```bash
# 1. Create GitHub repo at github.com/new
#    (name it: quantum-secure-chat)

# 2. Connect local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/quantum-secure-chat.git
git branch -M main
git push -u origin main

# 3. Connect to Vercel (https://vercel.com/new)
#    - Import from GitHub
#    - Configure build: cd frontend && flutter build web --release
#    - Output: frontend/build/web
#    - Add environment variables (see below)
#    - Deploy!
```

### Environment Variables for Vercel:
| Key | Value |
|-----|-------|
| `BACKEND_API_URL` | `http://192.168.29.109:8000/api` |
| `BACKEND_WS_URL` | `ws://192.168.29.109:8000/api/ws/chat` |

> Later replace with your deployed backend URL

---

## Every Update (After Initial Setup) - 10 seconds

```bash
# 1. Make changes in VS Code

# 2. Three git commands
git add .
git commit -m "Describe what you changed"
git push

# That's it! ✅
# Vercel auto-deploys your changes
# URL: https://quantum-secure-chat-xxxxx.vercel.app
```

---

## Commit Message Examples

```bash
git commit -m "Feature: Add user profile page"
git commit -m "Fix: Correct login validation"
git commit -m "Update: Improve dark mode colors"
git commit -m "Refactor: Simplify API calls"
```

---

## Check Status/Logs

```bash
# See what's different
git status

# See your commits
git log --oneline

# Check GitHub
https://github.com/YOUR_USERNAME/quantum-secure-chat

# Check Vercel deployments
https://vercel.com/dashboard
```

---

## If Something Breaks

```bash
# Quick revert
git revert HEAD
git push

# See what went wrong
# GitHub: Actions tab
# Vercel: Deployments tab → Click failed deploy
```

---

## Key Files

| File | Purpose |
|------|---------|
| `frontend/lib/config/backend_config.dart` | API URLs (can update config without rebuilding) |
| `.github/workflows/frontend-build.yml` | Automatic tests for frontend |
| `.github/workflows/backend-test.yml` | Automatic tests for backend |
| `vercel.json` | Vercel deployment configuration |

---

## URLs After Deployment

| Service | URL |
|---------|-----|
| **Your Web App** | `https://quantum-secure-chat-xxxxx.vercel.app` |
| **GitHub Repo** | `https://github.com/YOUR_USERNAME/quantum-secure-chat` |
| **Vercel Dashboard** | `https://vercel.com/dashboard` |
| **GitHub Actions** | `https://github.com/.../actions` |

---

## First-Time Verification

After Vercel deployment:

```
1. ✅ App loads at Vercel URL
2. ✅ Can create account
3. ✅ Can login
4. ✅ Can see users list
5. ✅ Can send messages
```

If any fails:
- Check Vercel deployment logs
- Verify backend API URL is correct
- Check browser console (F12) for errors

---

## Updating Backend URL

When you deploy backend to Render/Railway:

```
1. Get backend URL: https://your-backend.onrender.com
2. Go to Vercel dashboard → Settings
3. Update BACKEND_API_URL
4. Push empty commit to redeploy:
   git commit --allow-empty -m "Trigger redeploy"
   git push
```

---

## Common Commands Cheat Sheet

```bash
git status              # See changed files
git add .              # Stage all changes
git commit -m "msg"    # Create commit
git push               # Push to GitHub (triggers deployment)
git log --oneline      # See commit history
git reset --soft HEAD~1 # Undo last commit (keep changes)
git revert HEAD        # Revert last commit (create new commit)
git pull               # Get latest from GitHub
```

---

## Support Resources

- Full guide: `CI_CD_DEPLOYMENT_GUIDE.md`
- Backend config: `frontend/lib/config/backend_config.dart`
- Deployment config: `vercel.json`

---

**Remember**: After setup, deployment is as simple as:
```
Edit → git add . → git commit → git push
```

That's it! 🚀
