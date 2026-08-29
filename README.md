<img width="1536" height="1024" alt="TrustBoost PII Sanitizer" src="https://github.com/user-attachments/assets/5ac2a5c4-9ad3-410d-abaa-788527bd4f73" />

# 🛡️ TrustBoost — Information Flow Control for Autonomous AI Agents

[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Version: 2.6.0](https://img.shields.io/badge/Version-2.6.0-green)]()
[![Languages: 8](https://img.shields.io/badge/Languages-8%20supported-orange)]()
[![Downloads](https://img.shields.io/badge/ClawHub-1100%2B%20downloads-brightgreen)](https://clawhub.ai/teodorofodocrispin-cmyk/trustboost-pii-sanitizer)
[![GitHub Stars](https://img.shields.io/github/stars/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer?style=social)](https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer)
[![Listed on Glama](https://img.shields.io/badge/MCP-Glama%20Listed-blue)](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/trustboost-api)
[![awesome-mcp-servers](https://img.shields.io/badge/awesome--mcp--servers-Security-red)](https://github.com/punkpeye/awesome-mcp-servers)

> **The inspection layer between your agents and your LLMs.**
> Every autonomous AI pipeline has a blind spot: raw PII flowing unsanitized to external APIs and language models. TrustBoost closes that gap — with verifiable proof on Solana.

---

## ⚡ Try it now — no wallet, no setup

```bash
curl -X POST https://api.trustboost.dev/sanitize/preview \
  -H "Content-Type: application/json" \
  -d '{"text": "My name is John Doe, email john@gmail.com, SSN 123-45-6789"}'
```

```json
{
  "sanitized_content": "My name is [REDACTED], email [REDACTED], SSN [REDACTED]",
  "safety_score": 0.6,
  "risk_category": "PRIVATE",
  "demo": true,
  "requests_remaining": 2
}
```

3 free previews per IP · no account · no wallet · no setup.

---

## 🚀 Quick Start (Trial — 50 free sanitizations)

```bash
curl -X POST https://api.trustboost.dev/sanitize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact Maria at maria@company.com, RFC: LOPC850312AB3",
    "tx_hash": "TRIAL",
    "wallet_address": "your-agent-id",
    "context": "general"
  }'
```

```json
{
  "status": "success",
  "data": {
    "sanitized_content": "Contact [REDACTED] at [REDACTED], RFC: [REDACTED]",
    "safety_score": 0.6,
    "risk_category": "PRIVATE",
    "entities_removed": true,
    "entities": [
      {"type": "full_name", "category": "PRIVATE", "redacted_text": "Maria"},
      {"type": "email", "category": "PRIVATE", "redacted_text": "maria@company.com"},
      {"type": "mx_rfc", "category": "PRIVATE", "redacted_text": "LOPC850312AB3"}
    ],
    "usage_metrics": {"quota_remaining": 49, "quota_limit": 50}
  }
}
```

---

## 🌍 Languages & PII Coverage

| Language | Country-Specific Identifiers |
|----------|------------------------------|
| 🇺🇸 English | SSN, API keys, credit cards, IBAN, passwords |
| 🇲🇽 Spanish LATAM | RFC, CUIT, CURP, DNI, Cédula, RUC, NIT, RUT |
| 🇧🇷 Portuguese BR | CPF, CNPJ, RG, CEP |
| 🇩🇪 German | Personalausweis, Steuernummer, Sozialversicherungsnummer |
| 🇯🇵 Japanese | マイナンバー, 運転免許証, パスポート番号 |
| 🇫🇷 French | NIR, SIRET, SIREN, Carte Vitale |
| 🇮🇹 Italian | Codice Fiscale, Partita IVA, Tessera Sanitaria |
| 🇰🇷 Korean | 주민등록번호 (RRN), 사업자등록번호 |

---

## 🎯 Context Modes

| Mode | What it protects | Best for |
|------|-----------------|----------|
| `general` | All PII categories | Default agent pipelines |
| `financial` | IBANs, account numbers, wallet addresses | Payment workflows |
| `legal` | Maximum redaction | Contracts, court documents |
| `medical` | Patient identifiers, MRNs | Healthcare agents |
| `code` | API keys, credentials, PEM blocks | Dev pipelines, CI/CD |

---

## 🔐 Trust Model

| What TrustBoost does | What TrustBoost never does |
|---------------------|---------------------------|
| Sanitizes text before it reaches YOUR LLM | Store raw input text |
| Returns structured entity list | Log PII values |
| Anchors proof on Solana via Helius | Require personal accounts |
| Logs sanitized output only (90 days) | Retain your raw text after the request completes |

**Full disclosure on data transmission**: raw text is sent to Render (AWS) infrastructure and, for semantic detection, to OpenAI (GPT-4o-mini) — it is **not** processed locally. Neither TrustBoost nor OpenAI stores the raw text after the request completes; only the sanitized output and metadata are retained (see [PRIVACY.md](./PRIVACY.md)). **For strict no-transmission requirements** (e.g. on-premise HIPAA environments), this service is not suitable — use a local, regex/NER-based sanitizer instead.

Every paid sanitization generates an immutable **Proof of Sanitization** on Solana — verifiable by anyone at `/verify/{anchor_tx}`.

---

## 💰 Pricing

| Tier | Cost | Quota | How |
|------|------|-------|-----|
| **Preview** | Free | 3/IP/hour | `POST /sanitize/preview` |
| **Trial** | Free | 50/wallet | `tx_hash: "TRIAL"` |
| **Paid** | 149 USDC | 10,000 sanitizations | Send USDC on Solana → retry with `tx_hash` |

**Unit cost:** $0.0149 USDC per sanitization — paid as a single bundle of 149 USDC = 10,000 sanitizations. One payment, no subscriptions, no recurring charges. A rounding error compared to GDPR fines.

**Payment address (Solana mainnet):**
giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4

---

## 🤖 Protocol Support

| Protocol | Endpoint | Status |
|----------|----------|--------|
| **MCP** JSON-RPC 2.0 | `POST /mcp` | ✅ Live |
| **A2A** (Google) | `POST /message/send` | ✅ Conformant |
| **ANP** | `GET /.well-known/agent-description.json` | ✅ Live |
| **x402** | `GET /sanitize` → HTTP 402 | ✅ Live |

```bash
# Install as MCP server (Claude Code / Cursor / Windsurf)
npx clawhub install trustboost-pii-sanitizer
```

---

## 📊 Performance

| Metric | Score |
|--------|-------|
| Precision | 1.000 |
| Recall | 1.000 |
| F1 Score | 1.000 |
| False Positive Rate | 0.000 |
| Test cases | 34 labeled (8 languages) |
| Avg latency | ~200ms |

> Benchmark methodology and full test corpus available in [BENCHMARKS.md](./BENCHMARKS.md).

---

## 🏢 Enterprise & Compliance

TrustBoost provides a technical layer for compliance with:

**GDPR** · **LGPD** · **HIPAA** · **CCPA** · **APPI** · **EU AI Act** (August 2, 2026)

Every paid sanitization includes an on-chain audit trail verifiable at `/verify/{anchor_tx}` — suitable for compliance documentation under EU AI Act Articles 12, 13, and 26.

For enterprise inquiries: teodorofodocrispin@gmail.com

---

## 🛠️ API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sanitize` | POST | Main sanitization endpoint |
| `/sanitize/preview` | POST | Free preview, no wallet |
| `/score/{wallet}` | GET | TrustBoost Score & trust tier |
| `/verify/{anchor_tx}` | GET | Verify Proof of Sanitization on Solana |
| `/budget/{operator}` | GET | Privacy Budget status |
| `/health` | GET | Service health |
| `/preflight` | GET | Buyer-agent wallet authorization |
| `/policy` | GET | Policy hash for agent verification |
| `/.well-known/agent-card.json` | GET | A2A agent identity |
| `/.well-known/x402.json` | GET | x402 payment discovery |

Full OpenAPI spec: [api.trustboost.dev/openapi.json](https://api.trustboost.dev/openapi.json)

---

## 📦 Downloads & Distribution

[![Downloads](https://img.shields.io/badge/ClawHub-800%2B%20downloads-brightgreen)](https://clawhub.ai/teodorofodocrispin-cmyk/trustboost-pii-sanitizer)
[![Live Demo](https://img.shields.io/badge/🛡️%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/TrustBoost/pii-sanitizer)
[![Listed on x402-list.com](https://img.shields.io/badge/x402--list-Listed-orange)](https://x402-list.com/services/trustboost-pii-sanitizer)
[![Atelier Marketplace](https://img.shields.io/badge/Atelier-Live%20%24149-green)](https://atelierai.xyz/agents/trustboost)

---

## 🔗 Links

- **API:** [api.trustboost.dev](https://api.trustboost.dev)
- **Health:** [api.trustboost.dev/health](https://api.trustboost.dev/health)
- **Source:** [trustboost-api](https://github.com/teodorofodocrispin-cmyk/trustboost-api) (MIT)
- **Landing:** [trustboost.dev](https://teodorofodocrispin-cmyk.github.io/TrustBoost-PII-Sanitizer/)

---

*Built for the autonomous agent economy. MIT License.*
