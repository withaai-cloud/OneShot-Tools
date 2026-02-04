# How to Upload OneShot Tools to GitHub

Follow these simple steps to get your project on GitHub and deployed to Vercel.

## Method 1: GitHub Desktop (Easiest - Recommended)

### Step 1: Install GitHub Desktop
1. Go to [desktop.github.com](https://desktop.github.com)
2. Download and install GitHub Desktop
3. Sign in with your GitHub account (create one if needed at [github.com](https://github.com))

### Step 2: Add Your Project
1. Open GitHub Desktop
2. Click **File → Add Local Repository**
3. Click **Choose...** and select your `oneshot-tools-vercel` folder
4. If it says "not a Git repository", click **Create a Repository**

### Step 3: Create the Repository
Fill in the form:
- **Name**: oneshot-tools
- **Description**: Productivity tools suite with bank statement converter and tax optimizer
- **Keep this code private**: Uncheck (or keep checked if you want it private)
- Click **Create Repository**

### Step 4: Publish to GitHub
1. Click **Publish repository** in the top bar
2. Confirm:
   - Name: oneshot-tools
   - Description: (already filled in)
   - Keep private: Your choice
3. Click **Publish Repository**
4. Wait a few seconds
5. ✅ Done! Your code is now on GitHub

### Step 5: View on GitHub
1. In GitHub Desktop, click **Repository → View on GitHub**
2. Your project is live at: `github.com/YOUR_USERNAME/oneshot-tools`

---

## Method 2: GitHub Web Interface (No Installation)

### Step 1: Create Repository on GitHub
1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name**: oneshot-tools
   - **Description**: Productivity tools suite
   - **Public** or **Private**: Your choice
   - ✅ Check "Add a README file"
4. Click **Create repository**

### Step 2: Upload Your Files
1. On your new repository page, click **Add file → Upload files**
2. Drag and drop ALL files from your `oneshot-tools-vercel` folder
   - Or click **choose your files** and select all
3. At the bottom, add commit message: "Initial commit"
4. Click **Commit changes**
5. Wait for upload to complete
6. ✅ Done! Your code is on GitHub

---

## Method 3: Git Command Line (For Developers)

### Step 1: Initialize Git
```bash
cd oneshot-tools-vercel
git init
git add .
git commit -m "Initial commit: OneShot Tools"
```

### Step 2: Create Repository on GitHub
1. Go to [github.com/new](https://github.com/new)
2. Name: `oneshot-tools`
3. Click **Create repository**

### Step 3: Push to GitHub
Copy the commands from GitHub (they look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/oneshot-tools.git
git branch -M main
git push -u origin main
```

Enter your GitHub credentials when prompted.

✅ Done!

---

## What Happens Next?

Once your code is on GitHub:

### Automatic Benefits
- ✅ Version control
- ✅ Backup of your code
- ✅ Easy collaboration
- ✅ Ready for Vercel deployment

### Next Step: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click **Add New... → Project**
4. Select your `oneshot-tools` repository
5. Click **Deploy**
6. Wait 2-3 minutes
7. 🎉 Your app is live!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

---

## Troubleshooting

### "Repository already exists"
- Choose a different name, or
- Delete the existing repository first

### "Authentication failed"
Using Git command line:
```bash
# Use personal access token instead of password
# Generate at: github.com/settings/tokens
```

Using GitHub Desktop:
- File → Options → Accounts → Sign out and sign in again

### Files too large
GitHub has a 100MB file limit. If you have large files:
- Add them to `.gitignore`
- Use Git LFS for large files
- Or upload them separately

### "Nothing to commit"
Make sure you're in the correct folder:
```bash
pwd  # Should show path to oneshot-tools-vercel
```

---

## Tips

✅ **Use GitHub Desktop** - It's the easiest method
✅ **Make repository public** - Required for free Vercel hosting
✅ **Add a good description** - Helps others understand your project
✅ **Check the files** - Make sure all files uploaded correctly

---

## Need Help?

- **GitHub Guide**: [docs.github.com/get-started](https://docs.github.com/get-started)
- **GitHub Desktop Help**: [docs.github.com/desktop](https://docs.github.com/desktop)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)

---

**Ready to deploy? Let's go!** 🚀
