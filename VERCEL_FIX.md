# 🔧 Vercel Deployment Fix - Updated

If you're seeing "The server encountered an internal error", follow these steps:

## Quick Fix Steps

### Step 1: Download Updated Files

Download the new `oneshot-tools-vercel.zip` which includes these critical fixes:

**What changed:**
- `index.py` - Simple Vercel entry point at root level
- `app.py` - Added error handling and `/health` endpoint
- `vercel.json` - Simplified configuration

### Step 2: Test Health Endpoint

After deploying, visit: `https://your-app.vercel.app/health`

You should see:
```json
{
  "status": "ok",
  "message": "OneShot Tools is running",
  "python_version": "3.12.x"
}
```

If you see this, the app is working! Try the homepage.

### Step 3: Update Your GitHub Repository

**Using GitHub Desktop:**
1. Open GitHub Desktop
2. Go to your `oneshot-tools` repository folder
3. **Delete ALL files** in the folder
4. Extract new `oneshot-tools-vercel.zip`
5. Copy ALL files to your repository folder
6. In GitHub Desktop, you'll see changes
7. Commit: "Fix Vercel deployment - simplified structure"
8. Push to GitHub
9. Vercel auto-redeploys

**Using Git Command Line:**
```bash
cd your-repository-folder

# Remove old files (but keep .git)
find . -not -path './.git/*' -not -name '.git' -delete

# Copy new files
cp -r path/to/oneshot-tools-vercel/* .

# Commit
git add .
git commit -m "Fix Vercel deployment"
git push
```

### Step 4: Check Vercel Logs

If still getting errors:
1. Go to Vercel Dashboard
2. Click your project
3. Go to "Deployments"
4. Click latest deployment  
5. Click "Functions" tab
6. Look for error messages

## Common Issues & Solutions

### Error: "Build Failed"
Check the build logs in Vercel dashboard:
- Make sure all files were uploaded
- Check that `requirements.txt` is present
- Verify Python version (should auto-detect 3.12)

### Error: "404 Not Found"
- Clear browser cache
- Wait 5 minutes for DNS to propagate
- Check Vercel dashboard for deployment status

### Error: "500 Internal Server Error"
Check Vercel function logs:
1. Go to your project in Vercel
2. Click "Functions" tab
3. Look for error messages

Common causes:
- Missing dependencies in `requirements.txt`
- File path issues (check `/tmp` is being used)
- Large file uploads (> 4.5 MB limit)

## Alternative: Deploy to Railway

If Vercel continues giving issues, Railway is more Flask-friendly:

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select your repository
5. Click "Deploy"
6. No configuration needed!

Railway auto-detects Flask and handles everything.

**Railway Benefits:**
- Better for Python/Flask
- Larger file uploads
- Simpler configuration
- Free tier available

## Testing Locally

Before deploying, always test locally:

```bash
cd oneshot-tools-vercel
python app.py
```

Visit `http://localhost:5000` - if it works locally, it should work deployed.

## Need More Help?

- Check Vercel logs: Dashboard → Your Project → Functions → Logs
- Vercel Discord: [vercel.com/discord](https://vercel.com/discord)
- Try Railway instead: [railway.app](https://railway.app)

---

**The fix is ready!** Just update your GitHub repo with the new files and Vercel will redeploy automatically. 🚀
