# 🎯 Quick Fix for "Error rendering homepage: index.html"

Great news! Your app is **running on Vercel** now - it just can't find the template files.

## The Problem

Vercel's Python builder doesn't automatically include the `templates/` and `static/` folders in the serverless function.

## The Solution

I've updated `vercel.json` to explicitly tell Vercel to include these folders.

## How to Apply This Fix

### Step 1: Download New Files

Get the updated `oneshot-tools-vercel.zip`

### Step 2: Update Just These 2 Files

You only need to replace:
1. `vercel.json` - Now includes `includeFiles` configuration
2. `.vercelignore` - NEW file that ensures templates aren't ignored

### Step 3: Push to GitHub

**Using GitHub Desktop:**
1. Replace `vercel.json` in your repo
2. Add the new `.vercelignore` file
3. Commit: "Fix template loading for Vercel"
4. Push

**Using Git:**
```bash
# Copy the two files
cp path/to/new/vercel.json .
cp path/to/new/.vercelignore .

# Commit and push
git add vercel.json .vercelignore
git commit -m "Fix template loading for Vercel"
git push
```

### Step 4: Wait for Redeploy

Vercel will auto-redeploy (2-3 minutes)

### Step 5: Test

Visit your Vercel URL - you should now see the OneShot Tools homepage! 🎉

## What Changed

**Before (broken):**
```json
{
  "builds": [
    {
      "src": "index.py",
      "use": "@vercel/python"
    }
  ]
}
```

**After (fixed):**
```json
{
  "builds": [
    {
      "src": "index.py",
      "use": "@vercel/python",
      "config": {
        "includeFiles": [
          "templates/**",
          "static/**"
        ]
      }
    }
  ]
}
```

The `includeFiles` config tells Vercel to bundle the template and static folders with your serverless function.

## If Still Having Issues

### Templates Still Not Loading

Check in Vercel Dashboard → Your Project → Settings → General:
- Output Directory: Leave blank
- Install Command: `pip install -r requirements.txt`
- Build Command: Leave blank

### Static Files Not Loading

If CSS isn't loading, check browser console:
- Look for 404 errors on `/static/` files
- Make sure `static/` folder is in your GitHub repo
- Clear browser cache

### 500 Error on Specific Pages

Test each tool individually:
- `/health` - Health check
- `/` - Homepage  
- `/tools/bank-statement-converter` - Bank tool
- `/tools/tax-optimizer` - Tax tool

If one works but another doesn't, check that specific template file exists.

## File Structure Check

Make sure your GitHub repo has:
```
oneshot-tools/
├── index.py                 ✅
├── app.py                   ✅
├── vercel.json             ✅ (updated)
├── .vercelignore           ✅ (new)
├── requirements.txt        ✅
├── templates/              ✅
│   ├── index.html
│   ├── bank_statement_converter.html
│   └── tax_optimizer.html
└── static/                 ✅
    ├── css/
    │   └── style.css
    └── js/
        └── converter.js
```

## Success Checklist

After deploying, verify:
- ✅ `/health` returns JSON
- ✅ `/` shows homepage
- ✅ CSS loads (page looks styled)
- ✅ Navigation works
- ✅ Both tools load

## Why This Happened

Vercel's Python runtime is optimized for API functions, not full web apps. It doesn't automatically include non-Python files unless you specify them with `includeFiles`.

This is why frameworks like Next.js work better on Vercel - they're designed for it!

But with this fix, Flask works too! 💪

---

**Update these 2 files and you're good to go!** 🚀

If this still doesn't work after pushing, let me know what error you see.
