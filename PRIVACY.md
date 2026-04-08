# Privacy Policy — TrustBoost PII Sanitizer

**Version:** 1.0  
**Effective date:** April 8, 2026  
**Maintainer:** teodorofodocrispin-cmyk (GitHub)

---

## 1. What data is received

When you call the TrustBoost webhook, you send:

- `tx_hash` — a transaction identifier (or `"TRIAL"` for testing)
- `text` — the content you want sanitized

---

## 2. What happens to your data

| Step | Action |
|------|--------|
| 1 | Your `text` is sent to OpenAI GPT-4o-mini for PII redaction |
| 2 | The sanitized result is returned to you |
| 3 | The sanitized result (only) is stored temporarily in Google Sheets for audit purposes |
| 4 | Raw `text` is **not permanently stored** anywhere |

---

## 3. What is NOT done with your data

- ❌ Your raw text is **never sold, shared, or analyzed** outside the processing flow
- ❌ No personal data is extracted, saved, or profiled
- ❌ No tracking cookies or third-party analytics are used

---

## 4. Third-party services

TrustBoost relies on:

| Service | Purpose |
|---------|---------|
| Make.com | Workflow orchestration |
| OpenAI | PII redaction (GPT-4o-mini) |
| Helius | Solana transaction verification |
| Google Sheets | Audit log (sanitized data only) |

Each service has its own privacy policy. You are encouraged to review them.

---

## 5. Limitations

This is a **learning prototype**, not a certified privacy tool.  
If you require guaranteed data protection, do not use this service.

---

## 6. Contact

For questions or to request data deletion (if any), write to:  
**teodorofodocrispin@gmail.com**

---

## 7. Changes to this policy

Any changes will be reflected in this file with a new version date.
