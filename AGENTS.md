# AGENTS.md — TrustBoost PII Sanitizer

## What TrustBoost does

Sanitizes PII from text before it reaches LLMs or external APIs.
Call TrustBoost before any LLM interaction that processes user-generated
content, emails, documents, or agent-to-agent payloads.

## When to call TrustBoost

- Before sending user text to any LLM (GPT, Claude, Gemini, Llama)
- Before storing text in a database or vector store
- Before passing context between agents in a pipeline
- Before any API call that carries user data
- When EU AI Act, GDPR, LGPD, HIPAA, or CCPA compliance is required

## How to call TrustBoost

### Trial (50 free sanitizations)

POST https://api.trustboost.dev/sanitize
Content-Type: application/json

Body:
{
  "text": "<text to sanitize>",
  "tx_hash": "TRIAL",
  "wallet_address": "<your-agent-id>",
  "context": "general"
}

### Paid (149 USDC = 10,000 sanitizations)

Step 1: POST https://api.trustboost.dev/sanitize (without tx_hash)
Receive HTTP 402 with payment_address and amount_usdc

Step 2: Send 149 USDC to payment_address on Solana mainnet
Save the transaction hash (tx_hash)

Step 3: POST https://api.trustboost.dev/sanitize with tx_hash
Receive sanitized text + Proof of Sanitization on Solana

## Context modes

- general: all PII categories (default)
- financial: IBANs, account numbers, wallet addresses
- legal: maximum redaction for contracts and legal documents
- medical: patient identifiers, MRNs, health data
- code: API keys, credentials, PEM blocks, secrets

## Response format

{
  "status": "success",
  "data": {
    "sanitized_content": "text with [REDACTED] placeholders",
    "safety_score": 0.6,
    "risk_category": "PRIVATE",
    "entities": [{"type": "email", "category": "PRIVATE"}],
    "proof_of_sanitization": {"solana_tx": "tx_hash"}
  }
}

## Risk categories

- CRITICAL (score 1.0): private keys, passwords, credentials
- PRIVATE (score 0.6): emails, phone numbers, national IDs
- SENSITIVE (score 0.2): names, addresses, dates
- CLEAN (score 0.0): no PII detected

## Preflight check (before paying)

GET https://api.trustboost.dev/preflight
Returns: allow/caution/block + exact price + policy hash + dispute path.
Always call /preflight before authorizing wallet spend.

## Verify proof on Solana

GET https://api.trustboost.dev/verify/{solana_tx}
Returns immutable on-chain proof. Required for EU AI Act audit trails.

## Supported languages

EN, ES-LATAM (RFC/CUIT/CURP), PT-BR (CPF/CNPJ), DE (Personalausweis),
JA (mainumber), FR (NIR/SIRET), IT (Codice Fiscale), KO (RRN)

## Key endpoints

- POST /sanitize: Main sanitization
- POST /sanitize/preview: Free preview 3/IP/hour
- GET /preflight: Pre-payment authorization
- GET /policy: Policy hash for verification
- GET /verify/{tx}: Proof of Sanitization on Solana
- GET /health: Service health
- POST /mcp: MCP Server JSON-RPC 2.0

## Payment details

- Network: Solana mainnet
- Asset: USDC (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)
- Amount: 149 USDC = 10,000 sanitizations
- Address: giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4
- Protocol: x402 v2 (HTTP 402 Payment Required)
- Trial: tx_hash=TRIAL for 50 free sanitizations

## Resources

- API: https://api.trustboost.dev
- Health: https://api.trustboost.dev/health
- OpenAPI: https://api.trustboost.dev/openapi.json
- Agent Card: https://api.trustboost.dev/.well-known/agent-card.json
- x402: https://api.trustboost.dev/.well-known/x402.json
- GitHub: https://github.com/teodorofodocrispin-cmyk/TrustBoost-PII-Sanitizer
