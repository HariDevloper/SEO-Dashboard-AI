# 🚀 Deployment Guide: SEO Dashboard AI

This guide will help you upload your project to GitHub and host it live.

## 1. Upload to GitHub

Open your terminal in the project folder (`c:\Users\harik\Desktop\SEO dashboard AI`) and run these commands:

```bash
# Initialize Git
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit of SEO Dashboard AI"

# Create a new repository on GitHub (you need 'gh' CLI installed, OR do this manually on github.com)
# Option A: Using GitHub CLI
gh repo create seodashboard-ai --public --source=. --remote=origin --push

# Option B: Manual
# 1. Go to https://github.com/new
# 2. Create a repo named "seodashboard-ai"
# 3. thorough the commands shown on screen:
#    git remote add origin https://github.com/YOUR_USERNAME/seodashboard-ai.git
#    git branch -M main
#    git push -u origin main
```

## 2. Host the Backend (Python/Flask)
We recommend **Render** or **Railway** for hosting the Python backend.

**Using Render (Free Tier):**
1. Sign up at [render.com](https://render.com).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository.
4. **Root Directory:** `backend`
5. **Runtime:** Python 3
6. **Build Command:** `pip install -r requirements.txt`
7. **Start Command:** `gunicorn app:app`
8. Click **Create Web Service**.
9. **Copy the URL** provided (e.g., `https://seo-backend.onrender.com`).

## 3. Host the Frontend (React)
We recommend **Vercel** for the frontend.

1. Sign up at [vercel.com](https://vercel.com).
2. Click **Add New** -> **Project**.
3. Import your GitHub repository.
4. **Framework Preset:** Create React App (should auto-detect).
5. **Root Directory:** Click "Edit" and select `frontend`.
6. **Environment Variables:**
   - Add a new variable named `REACT_APP_API_URL`
   - Value: The Backend URL from Step 2 (e.g., `https://seo-backend.onrender.com/api`)
     *(Note: You might need to add `/api` to the end depending on your backend routes, currently the backend serves at `/api/audit`)*.
7. Click **Deploy**.

## 4. Final Configuration
Once the frontend is live, you need to tell the backend to allow requests from it (CORS).

1. Go back to your Backend hosting (Render).
2. Add an Environment Variable: `CORS_ORIGIN` = `https://your-frontend-domain.vercel.app`
3. (Optional) In `backend/app.py`, ensure `CORS(app)` allows this origin. Our current setup `CORS(app)` defaults to allowing all, which is fine for testing but check settings for production.

---
**Done!** Your SEO Dashboard is now live.
