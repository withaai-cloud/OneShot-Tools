# 🔧 Fix for Invert Amounts Option

## The Problem

The "Invert amounts" checkbox wasn't working - amounts weren't being inverted when the option was selected.

## The Solution

Fixed two issues:
1. **Backend reading the checkbox value** - FormData sends booleans as strings ("true"/"false")
2. **Amount formatting after inversion** - Now properly formats with commas and 2 decimals

## What Changed

### `app.py` - Two fixes:

**Fix 1: Reading the checkbox correctly**
```python
# Before - only checked for 'true', ignored 'false'
invert_amounts = request.form.get('invert_amounts') == 'true'

# After - properly handles both 'true' and 'false' strings
invert_amounts_str = request.form.get('invert_amounts', 'false')
invert_amounts = invert_amounts_str.lower() == 'true'
```

**Fix 2: Proper formatting after inversion**
```python
# Before - lost comma formatting
amount_clean = str(amount_val)

# After - maintains proper formatting
if amount_val >= 0:
    amount_clean = f"{amount_val:,.2f}"
else:
    amount_clean = f"-{abs(amount_val):,.2f}"
```

## How to Update

### Using GitHub Desktop:

1. **Extract** new `oneshot-tools-vercel.zip`
2. **Replace** just `app.py` in your repo
3. **Commit** in GitHub Desktop: "Fix invert amounts option"
4. **Push**
5. **Wait 2-3 minutes** for Vercel to deploy
6. **Test!**

## Testing

After deploying:

1. Go to Bank Statement Converter
2. Upload a PDF
3. ✅ **Check** "Invert amounts (flip positive ↔ negative)"
4. Click "Convert to Excel"
5. Download and open the Excel file
6. **Verify** amounts are inverted:
   - Credits (positive) should now be negative
   - Debits (negative) should now be positive

## How Inversion Works

**Normal (not inverted):**
- Credits = Positive (e.g., 1,000.00)
- Debits = Negative (e.g., -500.00)

**Inverted:**
- Credits = Negative (e.g., -1,000.00)
- Debits = Positive (e.g., 500.00)

This is useful when you want to switch accounting conventions!

## Debug Mode

The update includes a debug print statement. If you're still having issues, check the Vercel function logs to see:
- What value the checkbox is sending
- Whether inversion is being applied

To view logs:
1. Vercel Dashboard → Your Project
2. Functions tab
3. Click on latest function execution
4. Look for "DEBUG: invert_amounts_str = ..."

---

**Just replace app.py and it will work!** 🎯
