#!/usr/bin/env python3
"""
GRAVÜR ÜRETİMİ — OpenAI Image · SERT BÜTÇE KORUMASIYLA
================================================================================
⚠ BU BETİK PARA HARCAR. Bu yüzden önce bütçeyi, sonra görseli düşünür.

Kurucu YALNIZCA on dört düzeltilmiş gravür için harcama yetkisi verdi:

    HEDEF        3,00 $
    SERT TAVAN   4,00 $      ← aşılmaz; aşacaksa çağrı YAPILMAZ

⭑ ÜÇ KURAL ⭑

  ① Harcama defteri DİSKTE tutulur. Betik yeniden koşarsa toplam
    SIFIRLANMAZ — yoksa "her koşuda 3 dolar" olur ve tavan anlamını
    yitirir.
  ② Maliyet, çağrıdan DÖNEN token sayısıyla hesaplanır; tahmin yalnızca
    çağrı ÖNCESİ kapı içindir. Tahmine göre rapor yazmak, harcanmamış
    parayı harcanmış (ya da tersi) göstermektir.
  ③ Geçerli bir görsel ASLA yeniden üretilmez. Dosya varsa atlanır.

⚠ ANAHTAR: `.env` içinden okunur, EKRANA BASILMAZ, RAPORA YAZILMAZ,
COMMIT EDİLMEZ. `.env` zaten `.gitignore`dadır (§ ⑥ SIRLAR).

Çıkış kodları:  0 = tamam   1 = hata/bütçe   2 = kullanım
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

LIB = os.path.join(pl.ROOT, "07_ASSETS", "IMAGE_PROMPT_LIBRARY.html")
RAW = os.path.join(pl.ROOT, "07_ASSETS", "raw")
LEDGER = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "openai-spend.json")
ENV = os.path.join(pl.ROOT, ".env")

TARGET_USD = 3.00
CEILING_USD = 4.00

MODEL = "gpt-image-1"
SIZE = "1024x1024"
QUALITY = "high"

# ⚠ FİYATLAR gpt-image-1 token fiyatlandırmasından türer:
#   metin girdi  5,00 $ / 1M    · görsel çıktı 40,00 $ / 1M
# Gerçek maliyet çağrının döndürdüğü `usage` ile hesaplanır; aşağıdaki
# sabit yalnızca ÇAĞRI ÖNCESİ kapı için kullanılan TAHMİNDİR ve bilerek
# YÜKSEK tutulmuştur — düşük tahmin, tavanı delen tahmindir.
USD_PER_INPUT_TOKEN = 5.00 / 1_000_000
USD_PER_OUTPUT_TOKEN = 40.00 / 1_000_000
ESTIMATE_USD = 0.175            # 1024×1024 · high · ~4160 çıktı tokeni

# ⭑ ÜRETİLECEK ON DÖRT ⭑ Yönergede tek tek sayılmıştır; liste burada
# SABİTTİR ki bir hata bütün seti yeniden üretmeye dönüşmesin.
TARGETS = [
    "pl-g1-07", "pl-g1-08",
    "pl-g2-02", "pl-g2-05", "pl-g2-09", "pl-g2-12", "pl-g2-15", "pl-g2-18",
    "pl-g3-03", "pl-g3-08", "pl-g3-13", "pl-g3-18",
    "pl-g4-06", "pl-g4-18",
]


def read_key() -> str | None:
    """.env'den anahtar — DÖNDÜRÜLÜR, BASILMAZ."""
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"].strip()
    if not os.path.isfile(ENV):
        return None
    for line in open(ENV, encoding="utf-8"):
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == "OPENAI_API_KEY":
            return v.strip().strip('"').strip("'")
    return None


def load_ledger() -> dict:
    if os.path.isfile(LEDGER):
        try:
            return json.load(open(LEDGER, encoding="utf-8"))
        except (OSError, ValueError):
            pass
    return {"$comment": ["ÜRETİLEN DOSYA — 04_BUILD/engrave_openai.py.",
                         "Kümülatif OpenAI harcaması. ANAHTAR İÇERMEZ."],
            "model": MODEL, "size": SIZE, "quality": QUALITY,
            "targetUsd": TARGET_USD, "ceilingUsd": CEILING_USD,
            "calls": [], "totalUsd": 0.0}


def save_ledger(led: dict) -> None:
    led["totalUsd"] = round(sum(c["usd"] for c in led["calls"]), 6)
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    json.dump(led, open(LEDGER, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def prompts_from_library() -> dict:
    """⭑ PROMPT EZBERDEN YAZILMAZ ⭑ — üretecin bastığı metin okunur.

    ⚠ Yönerge açık: "Do NOT hand-write substitute prompts from memory."
    Kütüphane üreteçten doğar, üreteç bulmacadan. Buraya elle bir cümle
    yazmak, düzeltilen hatayı elle geri getirmektir.
    """
    doc = open(LIB, encoding="utf-8").read()
    out = {}
    for pid in TARGETS:
        m = re.search(r'<div class="prompt" id="%s-p">(.*?)</div>' % pid,
                      doc, re.S)
        if not m:
            continue
        out[pid] = html.unescape(re.sub("<[^>]+>", "", m.group(1))).strip()
    return out


def cost_of(usage: dict | None) -> float:
    """Gerçek maliyet — çağrının döndürdüğü token sayısından."""
    if not usage:
        return ESTIMATE_USD
    it = usage.get("input_tokens") or 0
    ot = usage.get("output_tokens") or 0
    if not ot:
        return ESTIMATE_USD
    return it * USD_PER_INPUT_TOKEN + ot * USD_PER_OUTPUT_TOKEN


def generate(key: str, prompt: str, timeout: int = 300) -> tuple:
    """Tek görsel. (png_bytes, usage) ya da (None, hata)."""
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": SIZE,
                       "quality": QUALITY, "n": 1}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations", data=body,
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        try:
            msg = json.load(e).get("error", {}).get("message", "")[:220]
        except Exception:                                      # noqa: BLE001
            msg = e.reason
        return None, "HTTP %s · %s" % (e.code, msg)
    except Exception as exc:                                   # noqa: BLE001
        return None, str(exc)[:220]
    try:
        return base64.b64decode(d["data"][0]["b64_json"]), d.get("usage")
    except (KeyError, IndexError, ValueError) as exc:
        return None, "yanıt çözülemedi: %s" % exc


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", help="tek levha (tekrarlanır)")
    ap.add_argument("--dry-run", action="store_true",
                    help="çağrı YAPMA — plan ve bütçe tahminini göster")
    ap.add_argument("--force", action="store_true",
                    help="dosya varsa bile yeniden üret (BÜTÇE HARCAR)")
    args = ap.parse_args()

    print("=" * 74)
    print("  GRAVÜR ÜRETİMİ · %s · %s · %s" % (MODEL, SIZE, QUALITY))
    print("=" * 74)

    led = load_ledger()
    spent = round(sum(c["usd"] for c in led["calls"]), 6)
    prompts = prompts_from_library()

    todo = [p for p in (args.only or TARGETS) if p in TARGETS]
    missing_prompt = [p for p in todo if p not in prompts]
    if missing_prompt:
        print("⛔ kütüphanede promptu YOK: %s" % missing_prompt)
        return 1
    if not args.force:
        skip = [p for p in todo
                if os.path.isfile(os.path.join(RAW, p + ".png"))]
        if skip:
            print("  ⊙ zaten var, ATLANDI (bütçe harcanmaz): %s"
                  % " ".join(skip))
        todo = [p for p in todo if p not in skip]

    est = len(todo) * ESTIMATE_USD
    print("\n── bütçe ──")
    print("  %-26s %.4f $" % ("şimdiye kadar harcanan", spent))
    print("  %-26s %d görsel × %.3f $ = %.3f $"
          % ("bu koşu (tahmin)", len(todo), ESTIMATE_USD, est))
    print("  %-26s %.4f $" % ("tahmini toplam", spent + est))
    print("  %-26s %.2f $ / %.2f $" % ("hedef / TAVAN", TARGET_USD,
                                       CEILING_USD))

    if spent + est > CEILING_USD:
        print("\n⛔ TAVAN AŞILIR (%.3f $ > %.2f $) — HİÇBİR ÇAĞRI YAPILMADI"
              % (spent + est, CEILING_USD))
        return 1
    if spent + est > TARGET_USD:
        print("\n  ⚠ hedef (%.2f $) aşılıyor ama tavan altında — devam"
              % TARGET_USD)

    if not todo:
        print("\n  ✓ üretilecek görsel yok")
        return 0
    if args.dry_run:
        print("\n  ⊙ KURU KOŞU — çağrı yapılmadı")
        for p in todo:
            print("     %-9s prompt %d karakter" % (p, len(prompts[p])))
        return 0

    key = read_key()
    if not key:
        print("\n⛔ OPENAI_API_KEY bulunamadı (.env ya da ortam)")
        return 1

    os.makedirs(RAW, exist_ok=True)
    ok, fail = [], []
    for i, pid in enumerate(todo, 1):
        # ⭑ HER ÇAĞRIDAN ÖNCE KAPI ⭑ Döngü içinde tekrar bakılır: gerçek
        # maliyet tahminden yüksek çıkarsa döngü kendini durdurmalıdır.
        spent = round(sum(c["usd"] for c in led["calls"]), 6)
        if spent + ESTIMATE_USD > CEILING_USD:
            print("\n⛔ TAVAN — %d görsel üretilmeden DURULDU" % (len(todo) - i + 1))
            fail += [{"id": p, "why": "bütçe tavanı"} for p in todo[i - 1:]]
            break

        t0 = time.time()
        png, usage = generate(key, prompts[pid])
        if png is None:
            print("  [%2d/%d] ⛔ %-9s %s" % (i, len(todo), pid, usage))
            fail.append({"id": pid, "why": str(usage)[:200]})
            continue

        usd = cost_of(usage if isinstance(usage, dict) else None)
        path = os.path.join(RAW, pid + ".png")
        with open(path, "wb") as fh:
            fh.write(png)
        led["calls"].append({
            "id": pid, "usd": round(usd, 6),
            "inputTokens": (usage or {}).get("input_tokens"),
            "outputTokens": (usage or {}).get("output_tokens"),
            "bytes": len(png), "seconds": round(time.time() - t0, 1)})
        save_ledger(led)
        ok.append(pid)
        print("  [%2d/%d] ✓ %-9s %6.1f KB · %.4f $ · toplam %.4f $ · %.0f sn"
              % (i, len(todo), pid, len(png) / 1024, usd,
                 led["totalUsd"], time.time() - t0))

    save_ledger(led)
    print("\n" + "=" * 74)
    print("  ✓ %d üretildi · ⛔ %d başarısız" % (len(ok), len(fail)))
    print("  ⭑ TOPLAM HARCAMA: %.4f $  (hedef %.2f · tavan %.2f)"
          % (led["totalUsd"], TARGET_USD, CEILING_USD))
    if led["totalUsd"] > CEILING_USD:
        print("  ⛔ TAVAN AŞILDI")
    print("=" * 74)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
