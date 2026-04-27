# Privacy Policy — TrustBoost PII Sanitizer
**Version:** 3.0  
**Effective date:** April 27, 2026  
**Maintainer:** teodorofodocrispin-cmyk (GitHub)

---

## 1. What data is received
When you call the TrustBoost API, you send:
- `tx_hash` — a transaction identifier (or `"TRIAL"` for testing)
- `text` — the content you want sanitized
- `wallet_address` — your Solana wallet address (optional, used for per-wallet TRIAL quota tracking)

---

## 2. What happens to your data

| Step | Action |
|------|--------|
| 1 | Your `text` is sent to OpenAI GPT-4o-mini for PII redaction |
| 2 | The sanitized result is returned to you |
| 3 | The sanitized result (only) is stored in Supabase PostgreSQL for audit purposes |
| 4 | Raw `text` is **not stored** anywhere |
| 5 | Your `wallet_address` is stored to track per-wallet TRIAL quota |

---

## 3. What is NOT done with your data
- ❌ Your raw text is **never sold, shared, or analyzed** outside the processing flow
- ❌ No personal data is extracted, saved, or profiled
- ❌ No tracking cookies or third-party analytics are used

---

## 4. Third-party services
TrustBoost v2.0 relies on:

| Service | Purpose | Privacy Policy |
|---------|---------|----------------|
| Render (AWS) | API hosting and infrastructure | https://render.com/privacy |
| Supabase | Audit log database (sanitized data only) | https://supabase.com/privacy |
| OpenAI | PII redaction (GPT-4o-mini) | https://openai.com/privacy |
| Helius | Solana transaction verification | https://helius.dev/privacy |

Each service has its own privacy policy. You are encouraged to review them.

---

## 5. Data retention
- **Audit log entries** (sanitized output + metadata): retained indefinitely for compliance traceability
- **Raw input text**: never stored at any point
- **wallet_address**: stored only for TRIAL quota tracking

---

## 6. Limitations
This is a **learning prototype**, not a certified privacy tool.  
If you require guaranteed data protection (e.g. formal HIPAA compliance with a signed BAA), do not use this service without contacting the maintainer first.

---

## 7. Contact
For questions or to request data deletion, write to:  
**teodorofodocrispin@gmail.com**

---

## 8. Changes to this policy
Any changes will be reflected in this file with a new version date.

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | April 8, 2026 | Initial release |
| 2.0 | April 8, 2026 | Added third-party services table |
| 3.0 | April 27, 2026 | Updated for v2.0 — Render + Supabase infrastructure, per-wallet tracking |
