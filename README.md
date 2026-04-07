<img width="1024" height="665" alt="image" src="https://github.com/user-attachments/assets/914a7d71-65ce-4086-9195-4be2302745be" />

🛡️ TrustBoost: Privacy Layer for AI
Stop sending sensitive user data to LLMs. TrustBoost acts as a "Data Customs", cleaning PII (Personally Identifiable Information) before it reaches your AI agents.

⚡ Quick Start (Trial Mode)
You don't need a license to start. Use the TRIAL token to test the API immediately:

import requests

# 🛡️ TrustBoost Privacy Layer - Integration in 30 seconds
def clean_pii(text):
    url = "(https://hook.us2.make.com/h4xqu3de1qlzn9mbrf7npe8rkelpft36)" 
    payload = {
        "text": text,
        "tx_hash": "TRIAL" # Free trial: first 50 requests included
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json().get("cleaned_text")
    except:
        return text # 

This repository implements an automated cybersecurity infrastructure that validates Solana transactions and uses AI to redact Personally Identifiable Information (PII).

### 🛠️ Technical Specifications
| Component | Technology |
| :--- | :--- |
| **Blockchain** | Solana Mainnet |
| **Verification Oracle** | Helius Digital Asset API (Threshold: 149 USDC) |
| **Privacy Engine** | OpenAI GPT-4o-mini |
| **Orchestration** | Make.com (No-Code/Low-Code Architecture) |
| **Database** | Google Sheets API |

### 🔍 System Logic (Verification Module)
The workflow functions as an intelligent "Data Customs" gate:
1. **Validation:** The system receives a `transaction_hash`.
2. **Payment Filter:** Helius is queried. If the transaction is < 148 USDC, the process terminates immediately.
3. **Sanitization:** Upon verified payment, the AI processes the text, redacting emails, private keys, passwords, and addresses.
4. **Logging:** The sanitized output is securely stored in Google Sheets for auditing purposes.

### 📑 Data Interface (JSON Payload)
```json
{
  "transaction_hash": "string (Solana Tx Hash)",
  "wallet_address": "string (Public Key)",
  "text_to_clean": "string (Sensitive Data)"
}

**TrustBoost** is a high-performance M2M (Machine-to-Machine) middleware designed to neutralize PII (Personally Identifiable Information) before it reaches LLM providers. Built for the Agent-to-Agent economy.
---

## 🛂 The Customs Protocol (Autonomous Access)
This system operates with a **Trustless Customs Gate**. Before any data is processed, the node verifies the Solana Ledger for a valid transaction signature.

### **How to Access:**
1. **Send Payment:** Exactly **149 USDC** (Solana Network) to:
   `giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4`
2. **Submit transaction_hash:** Include your **Transaction Signature (TX Hash)** in the body of your API call.
3. **Automatic Clearance:** Our Helius-powered node validates the payment in real-time. If the hash is valid, the "Gate" opens.

---

## 🛠️ API Implementation

### **Request with Payment Verification**
```bash
curl -X POST [https://hook.us2.make.com/h4xqu3de1qlzn9mbrf7npe8rkelpft36](https://hook.us2.make.com/h4xqu3de1qlzn9mbrf7npe8rkelpft36) \
-H "Content-Type: application/json" \
-d '{
  "transaction_hash": "PASTE_YOUR_SOLANA_TX_HASH_HERE",
  "wallet_address": "YOUR_WALLET_ADDRESS",
  "text_to_clean": "Contact me at john@doe.com or use key 5jK...9p"
}'

{
  "status": "success",
  "cleaned_text": "Contact me at [REDACTED] or use key [REDACTED]",
  "safety_score": "0.9",
  "risk_category": "CRITICAL"
}
```markdown
## 🤖 For AI Agents (MoltBook Compatible)

TrustBoost is designed to be consumed by autonomous agents. The following parameters are available beyond the basic API:

| Parameter | Type | Description |
|-----------|------|-------------|
| `confidence_threshold` | float (0.0-1.0) | Minimum confidence required to redact. Lower = more aggressive (default: 0.7). |
| `audit_trail` | boolean | If true, returns Solana transaction hash for each sanitization for on-chain verification. |
| `mode` | string | `"conservative"` (redacts only high-confidence PII) or `"aggressive"` (redacts anything suspicious). |

**Example agent call:**
```json
{
  "text_to_clean": "Contact me at john@doe.com",
  "transaction_hash": "TRIAL",
  "wallet_address": "YOUR_WALLET",
  "confidence_threshold": 0.85,
  "mode": "conservative",
  "audit_trail": true
}
{
  "status": "success",
  "cleaned_text": "Contact me at [REDACTED]",
  "safety_score": "0.92",
  "risk_category": "SENSITIVE",
  "solana_tx_hash": "5z3...9kP",
  "confidence_used": 0.85
}
💰 Sovereign Pricing Model
One-Time Integration: $149 USDC
Quota: 10,000 High-Velocity Sanitizations.
Audit Ledger: Every transaction is logged in a private, structured Security Ledger for real-time risk assessment.

📊 Security Dashboard
All processed data is categorized using our proprietary Risk Assessment logic:
Sanitized Output: Clean text ready for LLM processing.
Safety Score: Quantitative risk analysis (0.0 to 1.0).
Risk Category: Qualitative classification (PRIVATE, SENSITIVE, CRITICAL).
Developed for the next generation of privacy-first AI infrastructure.

## ⚙️ Infrastructure & Reliability

TrustBoost currently runs on **Make.com** webhooks with the following guarantees:

| Aspect | Detail |
|--------|--------|
| Uptime target | 99.9% (standard Make.com SLA) |
| Average latency | ~800ms per request |
| Rate limits | 30 requests per second |
| Fallback | None currently (roadmap: multi-provider) |

**For mission-critical deployments:** [Contact our technical team](mailto:teodorofodocrispin@gmail.com) for dedicated instance options.
