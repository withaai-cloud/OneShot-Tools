# 🏦 ABSA Bank Support Added!

## What's New

Your Bank Statement Converter now supports **both FNB and ABSA** bank statements!

### Features

✅ **Auto-detection** - Automatically detects if statement is FNB or ABSA
✅ **Multi-line descriptions** - ABSA descriptions spanning two lines are merged
✅ **Proper amounts** - Debits (expenses) are negative, Credits (income) are positive
✅ **Same Excel format** - Both banks output to same 3-column format

## What Changed

### Files Updated:
1. **`app.py`** - Added ABSA extraction logic
2. **`api/templates/index.html`** - Updated homepage to show ABSA support
3. **`api/templates/bank_statement_converter.html`** - Updated supported formats list

### ABSA Format Handling

**Input (ABSA PDF):**
```
Date              Description                    Charge  Debit    Credit   Balance
17/02/2025        Archive Stmt Enq              13.50 A                     343,560.98
28/02/2025        Acb Debit:External            15.00 T  944.27             340,616.71
                  Holland  Edo2502280828e+0003
```

**Output (Excel):**
```
Date          Description                                    Amount
17/02/2025    Archive Stmt Enq                              -13.50
28/02/2025    Acb Debit:External Holland Edo2502280828e+0003 -944.27
```

### How It Works

1. **Date extraction** - Reads DD/MM/YYYY format from ABSA statements
2. **Description merging** - If next line starts with spaces, it's added to description
3. **Amount detection** - Finds Debit (column 4) and Credit (column 5) amounts
4. **Conversion** - Debits become negative, Credits stay positive

## How to Update

### Using GitHub Desktop:

1. **Extract** new `oneshot-tools-vercel.zip`
2. **Replace these files** in your repo:
   - `app.py`
   - `api/templates/index.html`
   - `api/templates/bank_statement_converter.html`
3. **Commit**: "Add ABSA bank statement support"
4. **Push**
5. **Wait 2-3 minutes** for Vercel to deploy
6. **Test with ABSA statement!** ✅

## Testing

### Test with FNB Statement:
1. Upload FNB PDF
2. Convert - should work as before ✅

### Test with ABSA Statement:
1. Upload ABSA PDF (like March_2025.pdf)
2. Convert
3. Download Excel
4. Verify:
   - ✅ Dates in DD/MM/YYYY format
   - ✅ Multi-line descriptions merged
   - ✅ Debits are negative
   - ✅ Credits are positive

## Excel Output Format

**Same 3 columns for both banks:**
- **Date** - Transaction date
- **Description** - Transaction description (multi-line merged)
- **Amount** - Negative for expenses, Positive for income

## Supported Banks

- ✅ **FNB** - First National Bank
- ✅ **ABSA** - Absa Bank
- 🔜 Standard Bank (coming soon)
- 🔜 Nedbank (coming soon)
- 🔜 Capitec (coming soon)

## Format Auto-Detection

The tool automatically detects which bank the statement is from by looking for:
- "ABSA" or "Absa Bank" → ABSA format
- "FNB" or "First National Bank" → FNB format
- Default → FNB format

No need to select - it just works! 🎯

## Invert Amounts

The invert amounts option works for both FNB and ABSA:
- ✅ Check "Invert amounts" to flip positive ↔ negative
- Works the same for both bank formats

---

**Upload any FNB or ABSA statement and it will convert automatically!** 🚀
