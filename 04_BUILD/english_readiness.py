#!/usr/bin/env python3
"""
İNGİLİZCE DÖNÜŞÜM HAZIRLIĞI — pilot mimarisi üretim diline nasıl taşınır
================================================================================
⚠ BU BETİK BİR ÇEVİRİ YAPMAZ VE DÖNÜŞÜMÜ BAŞLATMAZ.

Talimat § 23 açıktır: dönüşüm ancak Türkçe pilot YETERİNCE DOĞRULANDIKTAN
sonra başlar. Doğrulama harici çözücü oturumlarıyla olur (A12) ve onlar
YAPILMADI. Dolayısıyla bu betik yalnızca **iş listesini ölçer**.

Ve ölçtüğü şey rahatsız edicidir:

    HİÇBİR BULMACA "ÇEVRİLEBİLİR" DEĞİLDİR.

Sebep tek bir sayıdır: Türk alfabesi **29**, İngiliz alfabesi **26** harf.
Eşik Alfabesi altı işaret grubunu beşerli kurar (5·5+4=29). İngilizcede bu
5·5+1 olur — yani **grup yapısı değişir** ve grup yapısına dayanan her
kısıt bulmacası (`ilk harf üçüncü gruptan`) YENİDEN KURULUR. Kaydırma
uzayı 28'den 25'e, yansıma ekseni 29'dan 26'ya iner; her şifreli dize
YENİDEN ÜRETİLİR. Basılı Sözlük yeniden yazılır, dolayısıyla her cevap
DEĞİŞİR. Kapı ifadesinin on dokuz harfi yeniden atanır.

  → "Türkçe başarı, İngilizce çözülebilirliğin kanıtı değildir" (K20) bir
    ihtiyat cümlesi değil, ÖLÇÜLMÜŞ bir olgudur.

Üç taşınabilirlik sınıfı ve gerçek anlamları:

  mechanical → MEKANİZMA taşınır, VERİ yeniden üretilir
  lexical    → mekanizma alfabe yapısına bağlı; KISIT yeniden tasarlanır
  phonetic   → ifadeye/sese bağlı; BULMACA yeniden tasarlanır

Çıkış kodları:  0 = rapor üretildi   2 = korumalı katman yok
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "06_REPORTS", "tracked",
                   "english-readiness.json")

WORK = {
    "mechanical": [
        "şifreli dize İngiliz alfabesiyle YENİDEN ÜRETİLİR (26 harf)",
        "cevap yeni İngilizce Sözlük'ten seçilir",
        "qa_answerspace ile tekillik YENİDEN ölçülür",
    ],
    "lexical": [
        "harf grubu yapısı 26 harfe göre YENİDEN KURULUR (5·5+1)",
        "kısıt kümesi yeni sözlükte TEK cevap bırakacak şekilde yeniden seçilir",
        "eleme adımlarının sırası ve ipucu merdiveni yeniden türetilir",
    ],
    "phonetic": [
        "ifade İngilizce olarak YENİDEN SEÇİLİR",
        "on dokuz cevabın harf/konum ataması BAŞTAN çözülür",
        "hata tespit listesi yeni ifadelerle yeniden kurulur ve",
        "asgari Hamming mesafesi YENİDEN ölçülür",
    ],
}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=OUT)
    args = ap.parse_args()

    print("=" * 74)
    print("  İNGİLİZCE DÖNÜŞÜM HAZIRLIĞI")
    print("=" * 74)

    cfg = pl.load_config()
    lang = cfg.get("language", {})
    conv = lang.get("englishConversion", {})
    fnd = cfg.get("founder", {}).get("externalSolvers", {})
    sols, designs = pl.load_protected()
    puzzles = [p for p in pl.load_index() if p.get("pilotCohort")]

    if not designs:
        print("\n  ⊘ korumalı katman bu ortamda yok — hazırlık ölçülemedi")
        return 2

    buckets: dict[str, list[str]] = {"mechanical": [], "lexical": [],
                                     "phonetic": [], "unclassified": []}
    for p in puzzles:
        d = designs.get(p["puzzleId"]) or {}
        k = d.get("languagePortability") or "unclassified"
        buckets.setdefault(k, []).append(p["puzzleId"])

    sessions = fnd.get("sessionsRecorded", 0)
    allowed = sessions >= cfg.get("killGate", {}).get("solversRequired", 5)

    print("\n── kapı ──")
    print("  pilot dili            %s" % lang.get("pilotLanguage"))
    print("  üretim dili           %s" % lang.get("productionLanguage"))
    print("  makine çevirisi       %s"
          % ("YASAK" if conv.get("forbidMachineTranslation") else "serbest"))
    print("  tam yeniden test      %s"
          % ("ZORUNLU" if conv.get("requiresFullRetest") else "hayır"))
    print("  harici oturum         %d" % sessions)
    print("  ⛔ DÖNÜŞÜM %s" % ("BAŞLAYABİLİR" if allowed
                               else "BAŞLAYAMAZ — pilot doğrulanmadı (A12)"))

    print("\n── taşınabilirlik ──")
    for k in ("mechanical", "lexical", "phonetic", "unclassified"):
        if buckets.get(k):
            print("  %-13s %2d bulmaca · %s"
                  % (k, len(buckets[k]), ", ".join(buckets[k][:6])
                     + (" …" if len(buckets[k]) > 6 else "")))

    print("\n── alfabe ölçüsü ──")
    print("  Türkçe 29 harf → 6 grup (5·5+4)")
    print("  İngilizce 26 harf → 6 grup (5·5+1)  ⚠ GRUP YAPISI DEĞİŞİR")
    print("  kaydırma uzayı 28 → 25 · yansıma ekseni 29 → 26")
    print("  ⇒ şifreli dizelerin TAMAMI yeniden üretilir")
    print("  ⇒ grup koşuluna dayanan kısıt bulmacaları YENİDEN TASARLANIR")

    report = {
        "pilotLanguage": lang.get("pilotLanguage"),
        "productionLanguage": lang.get("productionLanguage"),
        "conversionAllowed": allowed,
        "blockedBy": None if allowed else "A12",
        "requiresFullRetest": conv.get("requiresFullRetest"),
        "forbidMachineTranslation": conv.get("forbidMachineTranslation"),
        "retestGates": conv.get("retestGates", []),
        "portability": {k: v for k, v in buckets.items() if v},
        "workPerClass": WORK,
        "alphabet": {"tr": 29, "en": 26,
                     "groupStructureChanges": True,
                     "shiftSpace": {"tr": 28, "en": 25},
                     "reflectionAxes": {"tr": 29, "en": 26}},
        "invariantsToPreserve": [
            "bulmaca mantığı ve ipucu ilişkileri",
            "cevap tekilliği — YENİDEN ÖLÇÜLEREK",
            "zorluk bandı (★)",
            "atmosfer ve anlatı tonu",
            "kapı bulmacasının hata tespiti ve teşhis mekaniği",
        ],
        "note": ("Hiçbir bulmaca 'çevrilebilir' değildir; mekanizma taşınır, "
                 "veri yeniden üretilir. Türkçe başarı İngilizce "
                 "çözülebilirliğin kanıtı DEĞİLDİR."),
    }
    os.makedirs(os.path.dirname(args.json), exist_ok=True)
    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("\n" + "=" * 74)
    print("  ✍ %s" % os.path.relpath(args.json, pl.ROOT))
    print("  ⚑ DÖNÜŞÜM BAŞLATILMADI — talimat § 23 ve A12 gereği")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
