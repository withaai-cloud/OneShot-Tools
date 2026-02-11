# ✅ GitHub Upload Verification Checklist

## CRITICAL: Make sure you upload the `api/` FOLDER, not just its contents!

Your GitHub repository should look like this:

```
one-shot-tools/                    ← Your repo
├── api/                           ← THIS FOLDER MUST EXIST!
│   ├── index.py                   ← Must be inside api/
│   ├── templates/                 ← Must be inside api/
│   │   ├── index.html
│   │   ├── bank_statement_converter.html
│   │   └── tax_optimizer.html
│   └── static/                    ← Must be inside api/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── converter.js
├── app.py                         ← At root level
├── vercel.json                    ← At root level
├── requirements.txt               ← At root level
└── ... (other files)
```

## How to Check in GitHub

1. Go to your repository: `github.com/YOUR_USERNAME/one-shot-tools`
2. You should see an **`api`** folder in the file list
3. Click on the `api` folder
4. Inside you should see:
   - `index.py`
   - `templates/` folder
   - `static/` folder

## If `api/` Folder is Missing

### Using GitHub Desktop:

1. **Locate your local repo folder**
   - GitHub Desktop → Repository → Show in Explorer/Finder
2. **Check if `api/` folder exists**
   - You should see a folder literally named `api`
   - Inside it should be `index.py`, `templates/`, and `static/`
3. **If `api/` folder is missing:**
   - Extract `oneshot-tools-vercel.zip`
   - Make sure you copy the **entire `api` folder**, not just what's inside it
   - The folder structure should match exactly as shown above
4. **In GitHub Desktop:**
   - You should see `api/index.py`, `api/templates/index.html`, etc.
   - NOT just `index.py`, `templates/index.html`
5. **Commit and Push**

### Using GitHub Web Interface:

1. Go to your repository
2. If no `api/` folder exists, create it:
   - Click "Add file" → "Create new file"
   - Type: `api/index.py` (this creates the folder and file)
   - Copy content from your local `api/index.py`
   - Commit
3. Upload `templates/` and `static/` into the `api/` folder:
   - Click on `api` folder
   - Click "Add file" → "Upload files"
   - Drag the `templates/` and `static/` folders
   - Commit

## Visual Check

When you look at your GitHub repository, the file tree should show:

```
📁 api
   📄 index.py
   📁 static
      📁 css
         📄 style.css
      📁 js
         📄 converter.js
   📁 templates
      📄 index.html
      📄 bank_statement_converter.html
      📄 tax_optimizer.html
📄 app.py
📄 vercel.json
📄 requirements.txt
```

## Common Mistakes

❌ **WRONG:** Uploading only the contents of folders
```
index.py              ← NO! This should be in api/
templates/            ← NO! This should be in api/templates/
static/               ← NO! This should be in api/static/
```

✅ **RIGHT:** Uploading folders with their structure
```
api/                  ← YES! The api folder exists
  index.py            ← YES! Inside api/
  templates/          ← YES! Inside api/
  static/             ← YES! Inside api/
```

## Test After Fixing

Once you've confirmed the `api/` folder structure is correct:

1. Push to GitHub
2. Wait for Vercel to deploy (2-3 min)
3. Check the error page again
4. Look for `api` in the "Files in dir" list
5. It should now work! 🎉

## Still Not Working?

If the `api/` folder is correctly in GitHub but still not deploying:

1. In Vercel Dashboard → Your Project
2. Settings → Git
3. Click "Disconnect" then "Reconnect"
4. Redeploy

This forces Vercel to re-read the repository structure.

---

**The key issue:** The `api/` folder must exist in your GitHub repository!
