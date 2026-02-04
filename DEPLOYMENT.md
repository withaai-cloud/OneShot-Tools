# Deploying OneShot Tools to Vercel

This guide will help you deploy OneShot Tools to Vercel for free hosting.

## Prerequisites

1. A GitHub account
2. A Vercel account (free - sign up at [vercel.com](https://vercel.com))

## Step 1: Push to GitHub

### Option A: Using GitHub Desktop (Easiest)

1. **Download GitHub Desktop** from [desktop.github.com](https://desktop.github.com)
2. **Sign in** to your GitHub account
3. Click **File → Add Local Repository**
4. Browse to your `oneshot-tools-vercel` folder
5. Click **Create a repository** (if prompted)
6. Fill in:
   - Name: `oneshot-tools`
   - Description: "Productivity tools suite with bank statement converter and tax optimizer"
   - Keep the repository **Public** (or Private if you prefer)
7. Click **Publish repository**
8. Done! Your code is now on GitHub

### Option B: Using Git Command Line

```bash
cd oneshot-tools-vercel

# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: OneShot Tools"

# Create repository on GitHub (go to github.com/new)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/oneshot-tools.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

### Method 1: Import from GitHub (Recommended)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **Add New... → Project**
3. Click **Import Git Repository**
4. Select your `oneshot-tools` repository
5. Vercel will auto-detect it's a Flask app
6. Click **Deploy**
7. Wait 2-3 minutes for deployment
8. 🎉 You're live! Vercel will give you a URL like `oneshot-tools.vercel.app`

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd oneshot-tools-vercel
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Choose your account
# - Link to existing project? No
# - What's your project's name? oneshot-tools
# - In which directory is your code located? ./
# - Want to override the settings? No

# Your app will be deployed!
```

## Step 3: Custom Domain (Optional)

1. In your Vercel dashboard, go to your project
2. Click **Settings → Domains**
3. Add your custom domain
4. Update your domain's DNS records as instructed
5. Vercel will automatically handle SSL certificates

## Important Notes

### File Uploads
- Vercel has a **4.5 MB limit** for serverless function payloads
- For larger bank statements, consider these alternatives:
  - Split large PDFs before uploading
  - Use Vercel Blob Storage (paid)
  - Deploy to a different platform (Railway, Render, Fly.io)

### Storage
- Files uploaded to Vercel are stored in `/tmp` (temporary)
- Files are deleted after each request completes
- This is perfect for conversion tasks (no data persistence needed)
- Downloaded files work fine (sent immediately to user)

### Environment Variables
If you need any API keys or secrets:
1. Go to Project Settings → Environment Variables
2. Add your variables
3. Redeploy

## Alternative Hosting Options

If Vercel's limitations don't work for you:

### Railway.app (Recommended for Flask)
- Better for Python apps
- Larger file uploads
- $5/month (free tier available)
- Guide: [railway.app/new](https://railway.app/new)

### Render.com
- Free tier available
- Good for Flask apps
- No file size limits
- Guide: [render.com/docs](https://render.com/docs)

### Fly.io
- Free tier: 3 VMs
- Full control
- Good for Python
- Guide: [fly.io/docs](https://fly.io/docs)

### PythonAnywhere
- Specifically for Python
- Free tier available
- Easy Flask deployment
- Guide: [pythonanywhere.com](https://www.pythonanywhere.com)

## Updating Your Deployment

Whenever you make changes:

**If using GitHub + Vercel:**
1. Push changes to GitHub (using GitHub Desktop or `git push`)
2. Vercel automatically redeploys (takes 1-2 minutes)

**If using Vercel CLI:**
```bash
vercel --prod
```

## Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- View build logs in Vercel dashboard
- Ensure Python version is compatible (3.9+)

### File Upload Errors
- Check file size (must be < 4.5 MB for Vercel)
- Consider alternative hosting for large files

### 404 Errors
- Ensure `vercel.json` is in the root directory
- Check that routes are configured correctly
- Redeploy the project

### Slow Performance
- First request may be slow (cold start)
- Consider upgrading to Pro plan
- Or use always-on hosting (Railway, Render)

## Cost

**Vercel Free Tier:**
- ✅ Unlimited deployments
- ✅ Automatic SSL
- ✅ Global CDN
- ✅ Custom domains
- ⚠️ 100GB bandwidth/month
- ⚠️ 6,000 build minutes/month

More than enough for personal/small business use!

## Security

- All connections use HTTPS automatically
- Files are processed server-side
- No persistent storage (files deleted immediately)
- Your code is private (even on public GitHub repos)

## Support

- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- Vercel Community: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)

---

Need help? Check the troubleshooting section or consult the Vercel documentation.

**Happy deploying! 🚀**
