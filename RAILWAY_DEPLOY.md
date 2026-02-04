# 🚂 Deploy to Railway (Recommended Alternative to Vercel)

Railway is actually **better than Vercel for Flask apps**. Here's why and how to deploy:

## Why Railway?

✅ **Better for Python** - Native Flask support  
✅ **No file size limits** - Upload large bank statements  
✅ **Simpler deployment** - Just works, no config needed  
✅ **Free tier** - $5 credit/month (free)  
✅ **Better debugging** - See logs easily  

## Deployment Steps (5 minutes)

### Step 1: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### Step 2: Deploy Your Project

1. Click "New Project"
2. Click "Deploy from GitHub repo"
3. Select your `oneshot-tools` repository
4. Railway auto-detects it's a Flask app
5. Click "Deploy Now"
6. Wait 2-3 minutes ⏳

### Step 3: Get Your URL

1. Click on your deployment
2. Go to "Settings" tab
3. Scroll to "Domains"
4. Click "Generate Domain"
5. Copy your URL: `your-app.up.railway.app`

🎉 **Done!** Your app is live!

## Configuration (Optional)

Railway auto-detects Flask but you can customize:

### Add Environment Variables
1. Go to "Variables" tab
2. Add any needed variables
3. Click "Save"

### Custom Domain
1. Go to "Settings" → "Domains"
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records
5. SSL certificate auto-generated

### View Logs
Click "Deployments" → Latest deployment → "View Logs"

Perfect for debugging!

## Using Railway Instead of Vercel

No code changes needed! Your existing `oneshot-tools` repo works perfectly:

**Files Railway uses:**
- `requirements.txt` - Auto-installs dependencies
- `app.py` - Auto-detects Flask app
- No special configuration needed!

**What Railway does automatically:**
1. Detects Python project
2. Creates virtual environment
3. Installs from `requirements.txt`
4. Finds and runs `app.py`
5. Exposes on PORT environment variable
6. Generates HTTPS domain

## Pricing

**Free Tier:**
- $5 credit per month
- Enough for personal/small business use
- No credit card required initially

**Usage:**
- ~$0.01 per hour while running
- ~$7.20/month if always on
- Free tier covers this!

**Sleep Mode:**
- App sleeps after 30min inactive (free tier)
- Wakes up instantly on first request
- Or upgrade to keep always active

## Comparison: Railway vs Vercel

| Feature | Railway | Vercel |
|---------|---------|--------|
| Flask Support | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Okay |
| File Upload Limit | ✅ None | ⚠️ 4.5 MB |
| Configuration | ✅ None needed | ⚠️ Complex |
| Debugging | ✅ Easy logs | ⚠️ Harder |
| Cold starts | ✅ Fast | ✅ Fast |
| Free tier | ✅ $5/month | ✅ Good |
| Custom domains | ✅ Easy | ✅ Easy |

**Winner:** Railway for Flask apps!

## Updating Your App

Push to GitHub and Railway auto-deploys:

```bash
# Make changes to your code
git add .
git commit -m "Updated features"
git push
```

Railway automatically:
1. Detects the push
2. Rebuilds the app
3. Deploys new version
4. Zero downtime!

## Troubleshooting

### Build Failed
Check logs in Railway dashboard:
- Usually missing dependencies
- Add to `requirements.txt`

### App Not Starting
Check these:
1. `app.py` exists at root
2. Flask app named `app`
3. No syntax errors (test locally first)

### Port Issues
Railway sets PORT automatically.  
Your app already uses `0.0.0.0:5000` which works!

## Alternative: Use Railway CLI

For advanced users:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd your-project
railway up

# View logs
railway logs

# Open in browser
railway open
```

## Still Want to Use Vercel?

See `VERCEL_FIX.md` for the latest Vercel fixes.

But honestly, **Railway is easier** for Flask! 🚂

## Migration from Vercel to Railway

Already on Vercel? Easy switch:

1. Keep your GitHub repo unchanged
2. Connect Railway to same repo
3. Deploy on Railway
4. Test the Railway URL
5. Update DNS to point to Railway
6. Delete Vercel project (optional)

Takes 5 minutes!

## Need Help?

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Very responsive community
- **Railway Support**: help@railway.app

---

**Ready to deploy?** Go to [railway.app](https://railway.app) and deploy in 5 minutes! 🚀

Much easier than fighting with Vercel configuration! 😊
