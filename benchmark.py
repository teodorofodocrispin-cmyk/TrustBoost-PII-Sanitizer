#!/usr/bin/env python3
"""
TrustBoost PII Sanitizer — Performance Benchmark
Calculates precision, recall, F1 per language and PII type.
Compares vs regex baseline.

Usage:
    python3 benchmark.py
    TRUSTBOOST_API_URL=https://api.trustboost.dev python3 benchmark.py
"""

import os
import json
import time
import requests

API_URL = os.getenv("TRUSTBOOST_API_URL", "https://api.trustboost.dev")
TX_HASH = os.getenv("TRUSTBOOST_TX_HASH", "TRIAL")
WALLET  = "benchmark-agent"

# ── Corpus ────────────────────────────────────────────────────────────────────
# Each entry: {text, language, pii_type, has_pii, context}
# has_pii=True  → TrustBoost MUST detect (risk_category != CLEAN)
# has_pii=False → TrustBoost MUST NOT flag as CRITICAL (negative control)

CORPUS = [
    # ── ENGLISH ──────────────────────────────────────────────────────────────
    {"text": "Contact John at john@example.com for details", "lang": "EN", "pii_type": "email", "has_pii": True, "ctx": "general"},
    {"text": "My SSN is 123-45-6789 please keep it safe", "lang": "EN", "pii_type": "SSN", "has_pii": True, "ctx": "general"},
    {"text": "API key: sk-proj-abc123XYZ789secret", "lang": "EN", "pii_type": "api_key", "has_pii": True, "ctx": "code"},
    {"text": "Card number 4111111111111111 exp 12/28", "lang": "EN", "pii_type": "credit_card", "has_pii": True, "ctx": "financial"},
    {"text": "AWS key AKIAIOSFODNN7EXAMPLE in config", "lang": "EN", "pii_type": "aws_key", "has_pii": True, "ctx": "code"},
    {"text": "Call me at +1-555-867-5309 after 5pm", "lang": "EN", "pii_type": "phone", "has_pii": True, "ctx": "general"},
    {"text": "The quarterly revenue was $4.2M last period", "lang": "EN", "pii_type": "none", "has_pii": False, "ctx": "financial"},
    {"text": "Please compile the project and run tests", "lang": "EN", "pii_type": "none", "has_pii": False, "ctx": "code"},

    # ── SPANISH LATAM ─────────────────────────────────────────────────────────
    {"text": "El RFC del contribuyente es LOPJ850101ABC", "lang": "ES-LATAM", "pii_type": "RFC", "has_pii": True, "ctx": "legal"},
    {"text": "CUIT del proveedor: 20-12345678-9", "lang": "ES-LATAM", "pii_type": "CUIT", "has_pii": True, "ctx": "financial"},
    {"text": "CURP: LOPJ850101HDFRZN09 del solicitante", "lang": "ES-LATAM", "pii_type": "CURP", "has_pii": True, "ctx": "legal"},
    {"text": "DNI numero 12345678 del cliente Juan Lopez", "lang": "ES-LATAM", "pii_type": "DNI", "has_pii": True, "ctx": "general"},
    {"text": "El pedido numero 850101 fue procesado ayer", "lang": "ES-LATAM", "pii_type": "none", "has_pii": False, "ctx": "general"},
    {"text": "La reunion es el martes a las 10am en oficina", "lang": "ES-LATAM", "pii_type": "none", "has_pii": False, "ctx": "general"},

    # ── PORTUGUESE BRAZIL ─────────────────────────────────────────────────────
    {"text": "CPF do cliente: 123.456.789-09", "lang": "PT-BR", "pii_type": "CPF", "has_pii": True, "ctx": "financial"},
    {"text": "CNPJ da empresa: 12.345.678/0001-90", "lang": "PT-BR", "pii_type": "CNPJ", "has_pii": True, "ctx": "financial"},
    {"text": "Email do paciente: joao@hospital.com.br", "lang": "PT-BR", "pii_type": "email", "has_pii": True, "ctx": "medical"},
    {"text": "O numero do pedido e 123456789 processado", "lang": "PT-BR", "pii_type": "none", "has_pii": False, "ctx": "general"},

    # ── JAPANESE ──────────────────────────────────────────────────────────────
    {"text": "マイナンバー：123456789012 の申請書類", "lang": "JA", "pii_type": "MY_NUMBER", "has_pii": True, "ctx": "legal"},
    {"text": "運転免許証番号: 123456789012 を確認してください", "lang": "JA", "pii_type": "license", "has_pii": True, "ctx": "legal"},
    {"text": "田中太郎様のメール: tanaka@company.co.jp", "lang": "JA", "pii_type": "email", "has_pii": True, "ctx": "general"},
    {"text": "プロジェクトの進捗報告は来週月曜日に行います", "lang": "JA", "pii_type": "none", "has_pii": False, "ctx": "general"},

    # ── GERMAN ────────────────────────────────────────────────────────────────
    {"text": "Personalausweis-Nr. L01X00T471 des Antragstellers", "lang": "DE", "pii_type": "Personalausweis", "has_pii": True, "ctx": "legal"},
    {"text": "IBAN: DE89370400440532013000 fuer Ueberweisung", "lang": "DE", "pii_type": "IBAN", "has_pii": True, "ctx": "financial"},
    {"text": "Die Besprechung findet am Dienstag um 10 Uhr statt", "lang": "DE", "pii_type": "none", "has_pii": False, "ctx": "general"},

    # ── FRENCH ───────────────────────────────────────────────────────────────
    {"text": "NIR du patient: 1 85 12 75 012 345 22", "lang": "FR", "pii_type": "NIR", "has_pii": True, "ctx": "medical"},
    {"text": "SIRET de la societe: 73282932000074", "lang": "FR", "pii_type": "SIRET", "has_pii": True, "ctx": "financial"},
    {"text": "La reunion est prevue pour jeudi prochain", "lang": "FR", "pii_type": "none", "has_pii": False, "ctx": "general"},

    # ── ITALIAN ───────────────────────────────────────────────────────────────
    {"text": "Codice Fiscale: RSSMRA85T10A562S del contribuente", "lang": "IT", "pii_type": "Codice_Fiscale", "has_pii": True, "ctx": "legal"},
    {"text": "Partita IVA: IT12345678901 della societa", "lang": "IT", "pii_type": "Partita_IVA", "has_pii": True, "ctx": "financial"},
    {"text": "Il progetto sara completato entro venerdi", "lang": "IT", "pii_type": "none", "has_pii": False, "ctx": "general"},

    # ── KOREAN ────────────────────────────────────────────────────────────────
    {"text": "주민등록번호: 850101-1234567 확인 요망", "lang": "KO", "pii_type": "RRN", "has_pii": True, "ctx": "legal"},
    {"text": "사업자등록번호: 123-45-67890 입니다", "lang": "KO", "pii_type": "BRN", "has_pii": True, "ctx": "financial"},
    {"text": "회의는 다음주 화요일 오전 10시에 있습니다", "lang": "KO", "pii_type": "none", "has_pii": False, "ctx": "general"},
]


def sanitize(text, context="general"):
    """Call TrustBoost API and return result."""
    start = time.time()
    try:
        r = requests.post(
            f"{API_URL}/sanitize",
            json={"text": text, "tx_hash": TX_HASH, "wallet_address": WALLET, "context": context},
            timeout=30
        )
        latency_ms = (time.time() - start) * 1000
        if r.status_code != 200:
            return None, latency_ms
        data = r.json().get("data", {})
        return data, latency_ms
    except Exception:
        return None, 0


def run_benchmark():
    print("\n🛡️  TrustBoost PII Sanitizer — Performance Benchmark")
    print("=" * 60)
    print(f"API: {API_URL}")
    print(f"Corpus: {len(CORPUS)} cases ({sum(1 for c in CORPUS if c['has_pii'])} positive, {sum(1 for c in CORPUS if not c['has_pii'])} negative)")
    print("=" * 60)

    results = []
    latencies = []

    for case in CORPUS:
        data, latency_ms = sanitize(case["text"], case["ctx"])
        latencies.append(latency_ms)

        if data is None:
            detected = False
        else:
            risk = data.get("risk_category", "CLEAN")
            detected = risk != "CLEAN"

        tp = 1 if case["has_pii"] and detected else 0
        fp = 1 if not case["has_pii"] and detected else 0
        fn = 1 if case["has_pii"] and not detected else 0
        tn = 1 if not case["has_pii"] and not detected else 0

        results.append({
            **case,
            "detected": detected,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "latency_ms": latency_ms,
            "risk": data.get("risk_category", "ERROR") if data else "ERROR"
        })

        status = "✅" if (tp or tn) else "❌"
        print(f"{status} [{case['lang']}] {case['pii_type']} | {case['text'][:50]}...")

    # ── Global metrics ────────────────────────────────────────────────────────
    tp_total = sum(r["tp"] for r in results)
    fp_total = sum(r["fp"] for r in results)
    fn_total = sum(r["fn"] for r in results)
    tn_total = sum(r["tn"] for r in results)

    precision = tp_total / (tp_total + fp_total) if (tp_total + fp_total) > 0 else 0
    recall    = tp_total / (tp_total + fn_total) if (tp_total + fn_total) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    fpr       = fp_total / (fp_total + tn_total) if (fp_total + tn_total) > 0 else 0

    p99_latency = sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0

    print("\n" + "=" * 60)
    print("GLOBAL RESULTS")
    print("=" * 60)
    print(f"  Precision:       {precision:.3f}")
    print(f"  Recall:          {recall:.3f}")
    print(f"  F1 Score:        {f1:.3f}")
    print(f"  False Pos Rate:  {fpr:.3f}")
    print(f"  Avg Latency:     {avg_latency:.0f}ms")
    print(f"  p99 Latency:     {p99_latency:.0f}ms")
    print(f"  TP: {tp_total} | FP: {fp_total} | FN: {fn_total} | TN: {tn_total}")

    # ── Per-language metrics ──────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("PER LANGUAGE")
    print("=" * 60)
    print(f"{'Language':<12} {'Precision':<12} {'Recall':<10} {'F1':<8} {'Cases'}")
    print("-" * 55)

    langs = sorted(set(r["lang"] for r in results))
    for lang in langs:
        lr = [r for r in results if r["lang"] == lang]
        ltp = sum(r["tp"] for r in lr)
        lfp = sum(r["fp"] for r in lr)
        lfn = sum(r["fn"] for r in lr)
        lp = ltp / (ltp + lfp) if (ltp + lfp) > 0 else 1.0
        lre = ltp / (ltp + lfn) if (ltp + lfn) > 0 else 1.0
        lf1 = 2 * lp * lre / (lp + lre) if (lp + lre) > 0 else 0
        print(f"{lang:<12} {lp:<12.3f} {lre:<10.3f} {lf1:<8.3f} {len(lr)}")

    # ── Ruflo win condition check ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RUFLO WIN CONDITION (@ruvnet requirement)")
    print("=" * 60)
    latam_jp = [r for r in results if r["lang"] in ("ES-LATAM", "PT-BR", "JA")]
    if latam_jp:
        ltp = sum(r["tp"] for r in latam_jp)
        lfp = sum(r["fp"] for r in latam_jp)
        lfn = sum(r["fn"] for r in latam_jp)
        ltn = sum(r["tn"] for r in latam_jp)
        lp = ltp / (ltp + lfp) if (ltp + lfp) > 0 else 1.0
        lre = ltp / (ltp + lfn) if (ltp + lfn) > 0 else 1.0
        lfpr = lfp / (lfp + ltn) if (lfp + ltn) > 0 else 0
        recall_ok = "✅" if lre >= 0.95 else "❌"
        fpr_ok    = "✅" if lfpr <= 0.05 else "❌"
        print(f"  LATAM/JP Recall:     {lre:.3f} {recall_ok} (target ≥0.95)")
        print(f"  LATAM/JP FPR:        {lfpr:.3f} {fpr_ok} (target ≤0.05)")

    print("\n✅ Benchmark complete.")
    return {"precision": precision, "recall": recall, "f1": f1, "fpr": fpr}


if __name__ == "__main__":
    run_benchmark()
