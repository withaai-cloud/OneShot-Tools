# Sample Conversion Output for March_2025.pdf ABSA Statement

Based on the ABSA statement provided (16 Feb 2025 to 15 Mar 2025):

## Extracted Transactions (Sample - Page 1):

| # | Date       | Description                                              | Amount      |
|---|------------|----------------------------------------------------------|-------------|
| 1 | 16/02/2025 | Bal Brought Forward                                      | 343,560.98  |
| 2 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 3 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 4 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 5 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 6 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 7 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 8 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 9 | 17/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 10| 18/02/2025 | Notific Fee Sms Notifyme 3 Sms Notifications             | -1.80       |
| 11| 18/02/2025 | Archive Stmt Enq Settlement                              | -13.50      |
| 12| 28/02/2025 | Acb Debit:External Settlement Holland Edo2502280828e+0003| -944.27     |
| 13| 28/02/2025 | Acb Debit:External Settlement Hollard                    | -2,411.87   |
| 14| 01/03/2025 | Monthly Acc Fee Headoffice                               | -105.00     |
| 15| 01/03/2025 | Transaction Charge Headoffice                            | -48.60      |
| 16| 01/03/2025 | Admin Charge Headoffice See Charge Statement Detail      | -124.00     |
| 17| 05/03/2025 | Notific Fee Sms Notifyme 2 Sms Notifications             | -1.20       |
| 18| 05/03/2025 | Digital Payment Dt Settlement Absa Bank Stars Paye 5 March 25 | -9,853.50 |
| 19| 05/03/2025 | Proof Of Pmt Email Settlement                            | -1.25       |
| 20| 05/03/2025 | Digital Transf Dt Settlement Absa Bank Transfer From 4094181490 | 35,314.42 |
| 21| 05/03/2025 | Digital Payment Dt Settlement Absa Bank Transfer From 410214 | -200.00  |
| 22| 05/03/2025 | Proof Of Pmt Email Settlement                            | -1.25       |
| 23| 08/03/2025 | Pos Purchase Settlement Card No. 5987 Pp Stevens Garage (Effective 06/03/2025) Vryhe | -300.00 |
| 24| 13/03/2025 | Acb Credit Settlement 81 Njala                           | 40,000.00   |

## Notes:

**Multi-line Descriptions Merged:**
- Line 1: "Acb Debit:External"
- Line 2: "  Holland Edo2502280828e+0003"
- Result: "Acb Debit:External Holland Edo2502280828e+0003"

**Amount Handling:**
- Debit amounts (expenses) = Negative
- Credit amounts (income) = Positive
- Balance Brought Forward included as credit

**Date Format:**
- Already in DD/MM/YYYY format (perfect for Excel)

## Issues Found:

### PDF Encoding Problem ⚠️

The PDF has severe encoding issues. When extracted, dates appear as:
- Actual: `16/02/2025`
- Extracted: `ñöaðòaòðòõ`

This means the current code **won't work** for this specific ABSA statement due to font/encoding issues in the PDF.

### Solutions:

1. **OCR Approach** - Use OCR to read the PDF as an image
2. **Different Library** - Try a different PDF library
3. **Manual Pattern Matching** - Decode the garbled text back to numbers

Would you like me to:
- A) Try implementing OCR-based extraction
- B) Try decoding the garbled characters
- C) Just proceed with the current code and test with a different ABSA statement?

The current code logic is CORRECT, but this specific PDF has encoding issues.
