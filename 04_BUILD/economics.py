#!/usr/bin/env python3
"""
BASKI EKONOMİSİ — ÖLÇÜLEN sayfa sayısından telif
================================================================================
⚠ BRIEF § 7'deki telif tablosu **208 sayfalık bir modele** dayanıyordu ve
açıkça "hipotezdir" diyordu. İç blok artık ÜRETİLDİ ve sayfa sayısı
ÖLÇÜLDÜ. Bu betik eski hipotezi değil, ölçümü kullanır.

⭑ KINDLE'DA BİR TUZAK VAR ⭑ %70 telif planı **teslimat ücreti** keser
(dosya boyutu × MB başına ücret). Bu kitabın EPUB'ı 99 gravür taşıyor ve
onlarca MB. Büyük dosyada %70 planı, %35 planından DAHA AZ kazandırır —
ve bu hesaplanmadan seçilirse kitap başına dolarlar kaybedilir.

⚠ FİYATLAR ABD PAZARI İÇİNDİR ve KDP tarafından değiştirilebilir.
Kaynak sabitleri aşağıda açıkça yazılıdır; KDP değiştirirse BURASI
güncellenir — hesap değil, girdi değişir.

Çıkış kodları:  0 = hesaplandı   1 = eksik girdi
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
INT_PB = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "interior.json")
INT_HC = os.path.join(pl.ROOT, "06_REPORTS", "tracked",
                      "interior-hardcover.json")
KINDLE = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "kindle.json")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "economics.json")

# ── KDP ABD BASKI MALİYETİ (siyah mürekkep, normal trim) ──────────────
# Ciltsiz: sabit + sayfa başına.  Ciltli: daha yüksek sabit, aynı sayfa payı.
PB_FIXED, PB_PER_PAGE = 0.85, 0.012
HC_FIXED, HC_PER_PAGE = 5.65, 0.012
ROYALTY_RATE = 0.60                    # ABD genişletilmiş olmayan dağıtım

# ── KINDLE ────────────────────────────────────────────────────────────
# %70 planı teslimat ücreti keser; %35 planı kesmez.
KDP_70_MIN, KDP_70_MAX = 2.99, 9.99
DELIVERY_PER_MB = 0.15


def print_cost(pages: int, binding: str) -> float:
    if binding == "hardcover":
        return HC_FIXED + pages * HC_PER_PAGE
    return PB_FIXED + pages * PB_PER_PAGE


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  BASKI EKONOMİSİ · ölçülen sayfadan")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    meta = pl.load_json(META) or {}
    pb = (pl.load_json(INT_PB) or {}).get("facts") or {}
    hc = (pl.load_json(INT_HC) or {}).get("facts") or {}
    kin = (pl.load_json(KINDLE) or {}).get("facts") or {}
    eds = {e["id"]: e for e in meta.get("editions") or []}

    rep.check(bool(pb.get("pages")), "ciltsiz sayfa sayısı ölçüldü")
    if not pb.get("pages"):
        return rep.finish("sayfa yok", None)

    rows = []
    print("\n── baskı ──")
    print("  %-11s %6s %9s %9s %9s %8s" %
          ("sürüm", "sayfa", "liste", "maliyet", "TELİF", "marj"))
    for eid, facts in (("paperback", pb), ("hardcover", hc)):
        ed = eds.get(eid) or {}
        if not ed.get("enabled") or not facts.get("pages"):
            continue
        pages = facts["pages"]
        lst = float(ed.get("list") or 0)
        cost = print_cost(pages, eid)
        roy = lst * ROYALTY_RATE - cost
        rows.append({"edition": eid, "pages": pages, "list": lst,
                     "printCost": round(cost, 4),
                     "royalty": round(roy, 4),
                     "marginPct": round(100 * roy / lst, 1) if lst else 0})
        print("  %-11s %6d %8.2f$ %8.2f$ %8.2f$ %7.1f%%"
              % (eid, pages, lst, cost, roy, 100 * roy / lst if lst else 0))
        rep.check(roy > 0,
                  "%s telifi pozitif (%.2f $)" % (eid, roy))

    # ── KINDLE ────────────────────────────────────────────────────────
    ked = eds.get("kindle") or {}
    kindle_row = None
    if ked.get("enabled"):
        mb = (kin.get("bytes") or 0) / 1e6
        lst = float(ked.get("list") or 0)
        deliver = mb * DELIVERY_PER_MB
        # ⭑ TESLİMAT ÜCRETİ ORANDAN ÖNCE DÜŞÜLÜR ⭑
        # ⚠ Bu satır önce `0.70 * lst - deliver` diyordu — yani ücreti
        # oranı UYGULADIKTAN sonra düşüyordu. KDP'nin kendi telif
        # sayfası tersini söyler ve birebir şöyledir:
        #   "70% Royalty Rate x (List Price – applicable VAT -
        #    Delivery Costs) = Royalty"
        #   → kdp.amazon.com/en_US/help/topic/G200634500
        # 46,3 MB'lık bu dosyada fark küçük değildi: 0,05 $ yerine
        # 2,13 $. Öneri (%35) değişmiyor ama SAYI yanlıştı, ve yanlış
        # bir sayı doğru bir karara götürse bile yanlıştır.
        r70 = (0.70 * (lst - deliver)) if KDP_70_MIN <= lst <= KDP_70_MAX else None
        r35 = 0.35 * lst
        best = "35%" if (r70 is None or r35 > r70) else "70%"
        kindle_row = {"list": lst, "fileMB": round(mb, 1),
                      "deliveryFee": round(deliver, 4),
                      "royalty70": None if r70 is None else round(r70, 4),
                      "royalty35": round(r35, 4), "bestPlan": best}
        print("\n── Kindle ──")
        print("  %-24s %.1f MB" % ("EPUB boyutu", mb))
        print("  %-24s %.2f $" % ("liste", lst))
        print("  %-24s %.2f $" % ("teslimat ücreti (%70 planı)", deliver))
        print("  %-24s %s" % ("telif · %70 planı",
                              "uygun değil" if r70 is None
                              else "%.2f $" % r70))
        print("  %-24s %.2f $" % ("telif · %35 planı", r35))
        print("  %-24s ⭑ %s ⭑" % ("ÖNERİLEN PLAN", best))

        # ⭑ ASIL BULGU ⭑
        if r70 is not None and r35 > r70:
            rep.warn("⚑ %%70 PLANI BU DOSYADA DAHA AZ KAZANDIRIR "
                     "(%.2f $ < %.2f $): teslimat ücreti %.1f MB × %.2f $ = "
                     "%.2f $. %%35 planı seçilmeli YA DA EPUB küçültülmeli — "
                     "%%70'in kârlı olduğu sınır ~%.1f MB."
                     % (r70, r35, mb, DELIVERY_PER_MB, deliver,
                        # başabaş: 0,70·(L − 0,15·M) = 0,35·L
                        #        → M = (0,35·L) / (0,70 · 0,15)
                        (0.35 * lst) / (0.70 * DELIVERY_PER_MB)))
        rep.check(max(r35, r70 or 0) > 0, "Kindle telifi pozitif")

    # ── BRIEF ile karşılaştır ─────────────────────────────────────────
    print("\n── BRIEF § 7 (208 sayfalık HİPOTEZ) ile fark ──")
    brief = {"hardcover": (29.99, 8.15, 9.85), "paperback": (19.99, 3.50, 8.50)}
    for r in rows:
        b = brief.get(r["edition"])
        if not b:
            continue
        print("  %-11s maliyet %.2f → %.2f $  ·  telif %.2f → %.2f $"
              % (r["edition"], b[1], r["printCost"], b[2], r["royalty"]))
        if abs(r["printCost"] - b[1]) > 0.25:
            rep.warn("%s baskı maliyeti BRIEF'teki hipotezden %.2f $ "
                     "farklı (%d sayfa ölçüldü, model 208 varsaymıştı)"
                     % (r["edition"], r["printCost"] - b[1], r["pages"]))

    rep.facts.update({"print": rows, "kindle": kindle_row,
                      "royaltyRate": ROYALTY_RATE,
                      "source": "KDP ABD · siyah mürekkep · normal trim"})
    return rep.finish("%d baskı sürümü" % len(rows), STATS)


if __name__ == "__main__":
    sys.exit(main())
