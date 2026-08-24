#!/usr/bin/env python3
"""
⭑ EDİTORYAL BÜTÜNLÜK KAPISI ⭑ — line editor'ın bulduklarını KALICI kılar
================================================================================
Faz 5'te üç bağımsız line editor alt-ajanı okurun gördüğü 17.877 kelimeyi
taradı ve yirmi üç BLOKLAYICI bulgu bildirdi. Bulguların çoğu tek tek
düzeltilebilirdi; **sınıfları** düzeltilemezdi. Bu kapı sınıfları tutar.

Yol haritası Faz 5 § 13'ün uyarısı burada da geçerlidir: *"Line Editor
bir alt-ajandır ve körü körüne kabul edilmez."* Aşağıdaki her kural, ana
ajan tarafından ÜRETİM VERİSİNDE doğrulanmış bir kusurdan doğdu.

Yedi ölçüm:

  ① YAPIM KİMLİĞİ  — okur sayfasında `g4-001` gibi bir kimlik var mı
  ② ÇİFT BASIM     — aynı çizelge sayfada İKİ KEZ mi basılıyor
  ③ İKİZ LEVHA     — iki bulmaca AYNI veriyi mi basıyor
  ④ TEKRARLANAN BAŞLIK — iki sayfa aynı adı mı taşıyor
  ⑤ ANLATI KAYDI   — anlatı satırı MEKANİK içerik taşıyor mu
  ⑥ SAYI SÜTUNU    — cevabın satır numarası akranların arasında mı
  ⑦ BOŞ VAAT       — "şunu yaparsan çıkmaz" denen şey GERÇEKTEN bozuyor mu

────────────────────────────────────────────────────────────────────────
⭑ ⑤ HAKKINDA: KURAL DARALTILDI, ÇÜNKÜ ÖLÇÜLDÜ ⭑

`STYLE § 1` anlatı satırı için şunu diyor: *"bir sayı, bir yön, bir konum
veya bir çizelge adı geçemez."* Kural harfi harfine uygulandığında
**otuz dört sayfa** kırmızı yandı — ve otuz dördün büyük çoğunluğu şuydu:

    "İkinci yol birinciyle aynı görünür."
    "Üçüncü sayım. Artık ne aradığınızı biliyorsunuz."

Bunlar mekanik değil, ANLATI SIRALAMASIDIR: bir kütüphaneci kaçıncı
kayıtta olduğunuzu söyleyebilir. Kuralın koruduğu şey sıralama değil,
**bir üslup düzeltmesinin bir bulmacayı sessizce bozması**dır.

O yüzden kural ölçüye göre daraltıldı ve daraltıldığı YAZILDI (K42):

    ⛔ ÇİZELGE ADI  — bir çizelge adı daima mekaniktir
    ⛔ YÖN SÖZCÜĞÜ  — bu kitapta yön daima mekaniktir
    ⛔ RAKAM        — nesirde bir rakam daima bir niceliktir
    ⛔ ÇELİŞKİ      — anlatının söylediği sayı, sayfanın bastığı sayıyla
                      tutmuyorsa okur ikisinden birine inanır ve
                      yanılabilir

    ✅ sıra sözcüğü ("İkinci yol") — anlatı sıralamasıdır

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

BOOK = os.path.join(pl.ROOT, "02_MANUSCRIPT", "book.json")

BUILD_ID = re.compile(r"\b(g\d+-\d{3}|meta-\d{3}|pl-[a-z0-9-]+)\b")
CHART_NAME = re.compile(r"Çizelge\s+[A-ZÇĞİÖŞÜ]|Katalo[ğg]u|Sözlü[ğg]ü")
DIRECTION = re.compile(
    r"\b(soldan|sağdan|yukarıdan|aşağıdan|ters(?:ine|ten)?|baştan|sondan"
    r"|saat yönünde|sol kenar|sağ kenar)\b", re.IGNORECASE)
DIGIT = re.compile(r"\d")
ORDINAL = re.compile(
    r"\b(birinci|ikinci|üçüncü|dördüncü|beşinci|altıncı|yedinci|sekizinci"
    r"|dokuzuncu|onuncu|son)\b", re.IGNORECASE)

READER_FIELDS = ("title", "objective", "readerAction")

ALPHABET = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def _shift(text: str, k: int) -> str:
    return "".join(ALPHABET[(ALPHABET.index(c) + k) % len(ALPHABET)]
                   if c in ALPHABET else c for c in text)


def _reflect(text: str, axis: int) -> str:
    return "".join(ALPHABET[(axis - ALPHABET.index(c)) % len(ALPHABET)]
                   if c in ALPHABET else c for c in text)


def _ungrid(text: str, width: int) -> str:
    n = len(text)
    rows = (n + width - 1) // width if width else n
    out = [""] * n
    i = 0
    for c in range(width):
        for r in range(rows):
            pos = r * width + c
            if pos < n and i < n:
                out[pos] = text[i]
                i += 1
    return "".join(out)


def _undo(text: str, stages: list) -> str:
    """Katmanları verilen sırayla GERİ ALIR — ⑦'nin ölçüsü."""
    for st in reversed(stages):
        kind = st.get("kind")
        if kind == "shift":
            text = _shift(text, -int(st.get("by", 0)))
        elif kind == "reflect":
            text = _reflect(text, int(st.get("axis", 0)))
        elif kind == "grid":
            text = _ungrid(text, int(st.get("width", 1)))
    return text


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    gate_level = args.gate or pl.read_gate()
    if gate_level not in pl.VALID_GATES:
        print("HATA: geçersiz kapı seviyesi: %s" % gate_level, file=sys.stderr)
        return 2

    print("=" * 74)
    print("  ⭑ EDİTORYAL BÜTÜNLÜK ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    book = pl.load_json(BOOK) or {}
    if not book:
        print("\n  ⊘ manuscript bu ortamda yok (korumalı katman) — "
              "denetim YAPILAMADI")
        rep.warn("editoryal bütünlük BOŞ KOŞTU — yerelde koşturun")
        return rep.finish("manuscript yok", args.json)

    pages = book.get("puzzles", [])
    warm = book.get("warmUp") or []

    # ── ① YAPIM KİMLİĞİ ────────────────────────────────────────────────
    # `g4-001` bir yapım kimliğidir. Okur bulmacaları BAŞLIKLA ve SIRA
    # SAYISIYLA tanır; kitabın hiçbir yerinde böyle bir dize basılı
    # değildir. Bir sayfa ona gönderme yaparsa okur bulamayacağı bir şeyi
    # arar — sözleşmenin ikinci maddesi.
    build_id = []
    for p in pages:
        txt = " ".join([str(p.get(f) or "") for f in READER_FIELDS]
                       + [str(x) for x in (p.get("clues") or [])]
                       + [str(x) for x in (p.get("constraints") or [])]
                       + [str(p.get("flavour") or "")])
        found = sorted(set(BUILD_ID.findall(txt)))
        # Kendi levha kimliğine yapılan atıf `input` alanındadır ve o
        # alan okurun gördüğü LEVHA TARİFİDİR; burada aranmaz.
        found = [x for x in found if x != p.get("plateId")]
        if found:
            build_id.append("%s → %s" % (p["puzzleId"], " ".join(found)))

    # ── ② ÇİFT BASIM ───────────────────────────────────────────────────
    twice = [p["puzzleId"] for p in pages
             if p.get("figure") and p.get("printedTable")
             and str(p["figure"]).strip() == str(p["printedTable"]).strip()]

    # ── ③ İKİZ LEVHA ───────────────────────────────────────────────────
    seen: dict = collections.defaultdict(list)
    for p in pages:
        for key in ("figure", "printedTable"):
            if p.get(key):
                seen[str(p[key]).strip()].append(p["puzzleId"])
    twins = sorted({tuple(sorted(set(v))) for v in seen.values()
                    if len(set(v)) > 1})

    # ── ④ TEKRARLANAN BAŞLIK ───────────────────────────────────────────
    titles = collections.Counter(
        [str(p.get("title") or "") for p in pages]
        + [str(w.get("title") or "") for w in warm])
    dup_title = sorted("%s ×%d" % (t, n) for t, n in titles.items()
                       if t and n > 1)

    # ── ⑤ ANLATI KAYDI ─────────────────────────────────────────────────
    voice, contradict = [], []
    for p in pages:
        f = str(p.get("flavour") or "")
        if not f:
            continue
        tags = []
        if CHART_NAME.search(f):
            tags.append("çizelge adı")
        if DIRECTION.search(f):
            tags.append("yön")
        if DIGIT.search(f):
            tags.append("rakam")
        if tags:
            voice.append("%s (%s)" % (p["puzzleId"], " + ".join(tags)))

        # ⭑ ÇELİŞKİ ⭑ Anlatının sıra sözcüğü, sayfanın bastığı sayıyla
        # aynı şeyi anlatıyorsa ve TUTMUYORSA okur ikisinden birine
        # inanır. Ölçülen: Kapı V'te başlık "Beşinci Sözcük" derken levha
        # altıncı sözcüğü istiyordu.
        fig = str(p.get("figure") or "")
        m = re.search(r"sözcük\s*:\s*(\d+)", fig)
        if m:
            said = ORDINAL.search(f)
            word = {"birinci": 1, "ikinci": 2, "üçüncü": 3, "dördüncü": 4,
                    "beşinci": 5, "altıncı": 6, "yedinci": 7,
                    "sekizinci": 8, "dokuzuncu": 9, "onuncu": 10}
            if said and word.get(said.group(1).lower()) not in (None,
                                                               int(m.group(1))):
                contradict.append("%s: anlatı '%s' · levha %s"
                                  % (p["puzzleId"], said.group(1), m.group(1)))

    # ── ⑥ SAYI SÜTUNU CEVABI ELE VERİYOR MU ────────────────────────────
    # ⭑⭑ ÖLÇÜLDÜ: YEDİ LEVHANIN YEDİSİNDE ⭑⭑
    # Sınıflama levhaları her üyenin yanına katalog satır numarasını
    # basar. Akranlar havuzdan sırayla alındığı için numaraları kendi
    # aralarında kümeleniyor, cevabınki kümenin DIŞINDA kalıyordu.
    # Okur levhaya hiç bakmadan, yalnızca sayı sütununu tarayarak iki
    # kapının sınıflama bulmacalarını çözebilirdi.
    sols, _ = pl.load_protected()
    # ⚠ İLK KALIP EN AZ ÜÇ SÜTUN VARSAYIYORDU ve iki sütunlu bir çizelgeyi
    # hiç görmüyordu — fikstür yakaladı. Kalıp artık aradaki sütun
    # sayısına bakmaz.
    ROW = re.compile(
        r"\|\s*([A-ZÇĞİÖŞÜ]+)\s*\|(?:[^|\n]*\|)*?\s*(\d+)\s*\|")
    NUM = re.compile(r"\|\s*(\d+)\s*\|")
    outlier = []
    for p in pages:
        blob = str(p.get("figure") or "") + str(p.get("printedTable") or "")
        answer = (sols.get(p["puzzleId"]) or {}).get("finalAnswer")
        if not answer:
            continue
        mine = next((int(m.group(2)) for m in ROW.finditer(blob)
                     if m.group(1) == answer), None)
        nums = [int(x) for x in NUM.findall(blob)]
        if mine is None or len(nums) < 5:
            continue
        rest = [n for n in nums if n != mine]
        if rest and (mine < min(rest) or mine > max(rest)):
            outlier.append("%s (#%d ∉ [%d..%d])"
                           % (p["puzzleId"], mine, min(rest), max(rest)))

    # ── ⑦ VAAT EDİLEN HATA SİNYALİ GERÇEKTEN ATEŞLİYOR MU ──────────────
    # ⭑⭑ ÖLÇÜLDÜ: YEDİ SAYFANIN YEDİSİNDE ATEŞLEMİYORDU ⭑⭑
    #
    # Katmanlı zincir sayfaları şunu basıyordu: *"Katmanlar ters sırada
    # uygulanırsa ad çıkmaz."* Ama katmanların biri harf DEĞİŞTİRİR,
    # öteki harf YERİ değiştirir; bu iki işlem birbirinin yerine geçer
    # ve ters sıra AYNI cevabı verir.
    #
    # Bu, kolay bir bulmacadan kötüdür: kitap OLMAYAN bir hata sinyali
    # vaat ediyordu. İki sırayı da deneyen okur aynı cevabı iki kez alır
    # ve sözleşmenin birinci sözü gereği KİTABI bozuk sanır.
    #
    # Kural geneldir: bir sayfa "şunu yaparsan cevap ÇIKMAZ" diyorsa, o
    # şey gerçekten cevabı bozmak ZORUNDADIR.
    ORDER_CLAIM = re.compile(
        r"ters\s+sıra|sıra\s+levhadaki|ters\s+uygulan", re.IGNORECASE)
    hollow = []
    for p in pages:
        rec = sols.get(p["puzzleId"]) or {}
        acc = ((rec.get("answerSpace") or {}).get("acceptance") or {})
        if acc.get("kind") != "reachable-by-layered-chain":
            continue
        txt = " ".join([str(p.get(f) or "") for f in READER_FIELDS]
                       + [str(x) for x in (p.get("clues") or [])]
                       + [str(x) for x in (p.get("constraints") or [])])
        if not ORDER_CLAIM.search(txt):
            continue
        stages = acc.get("stages") or []
        if len(stages) < 2:
            continue
        if _undo(acc.get("input", ""), list(reversed(stages))) == \
                rec.get("finalAnswer"):
            hollow.append(p["puzzleId"])

    print("\n── ölçülen ──")
    print("  okur sayfası       %d" % len(pages))
    print("  ısınma örneği      %d" % len(warm))
    print("  anlatı satırı      %d"
          % sum(1 for p in pages if p.get("flavour")))

    rep.facts.update({"pages": len(pages), "buildIdLeak": build_id,
                      "printedTwice": twice,
                      "twinPlates": ["+".join(t) for t in twins],
                      "duplicateTitles": dup_title,
                      "voiceBreaches": voice, "contradictions": contradict,
                      "numberOutliers": outlier,
                      "hollowPromises": hollow})

    rep.check(not build_id,
              "⭑ ① HİÇBİR OKUR SAYFASI YAPIM KİMLİĞİ BASMIYOR ⭑ "
              "(`g4-001` kitapta hiçbir yerde yazmaz; okur onu arayamaz)"
              + ("" if not build_id else " — ⛔ %s" % build_id[:6]))
    rep.check(not twice,
              "⭑ ② HİÇBİR ÇİZELGE AYNI SAYFADA İKİ KEZ BASILMIYOR ⭑ "
              "(sayfa 'çizelge tek yetkedir' derken iki kopya basarsa "
              "okur hangisinin yetke olduğunu sorar)"
              + ("" if not twice else " — ⛔ %s" % twice[:6]))
    rep.check(not twins,
              "⭑ ③ İKİ BULMACA AYNI LEVHA VERİSİNİ BASMIYOR ⭑ "
              "(okur ya baskı hatası sanır ya da önceki cevabın "
              "geçerli olduğunu)"
              + ("" if not twins else " — ⛔ %s"
                 % ["+".join(t) for t in twins][:6]))
    rep.check(not dup_title,
              "④ hiçbir başlık iki kez kullanılmıyor "
              "(ipucu ve çözüm bölümleri başlıkla dizinlenir)"
              + ("" if not dup_title else " — ⛔ %s" % dup_title))
    rep.check(not voice,
              "⭑ ⑤ ANLATI SATIRI MEKANİK İÇERİK TAŞIMIYOR ⭑ "
              "(çizelge adı · yön · rakam — bir üslup düzeltmesi bir "
              "bulmacayı sessizce bozamaz · STYLE § 1 · K42)"
              + ("" if not voice else " — ⛔ %s" % voice[:6]))
    rep.check(not outlier,
              "⭑ ⑥ CEVABIN SATIR NUMARASI AKRANLARIN ARASINDA ⭑ "
              "(uçta duran bir numara, okurun levhaya HİÇ BAKMADAN "
              "çözmesini sağlar — mekanizma devre dışı kalır)"
              + ("" if not outlier else " — ⛔ %s" % outlier[:6]))
    rep.check(not hollow,
              "⭑ ⑦ VAAT EDİLEN HATA SİNYALİ GERÇEKTEN ATEŞLİYOR ⭑ "
              "(kitap OLMAYAN bir hatayı vaat edemez: iki yolu da deneyen "
              "okur aynı cevabı iki kez alır ve KİTABI bozuk sanar)"
              + ("" if not hollow else " — ⛔ BOŞ VAAT: %s" % hollow[:6]))
    rep.check(not contradict,
              "⭑ ⑤b ANLATI, SAYFANIN BASTIĞI SAYIYLA ÇELİŞMİYOR ⭑"
              + ("" if not contradict else " — ⛔ %s" % contradict[:5]))

    return rep.finish("%d sayfa · %d anlatı satırı denetlendi"
                      % (len(pages),
                         sum(1 for p in pages if p.get("flavour"))),
                      args.json)


if __name__ == "__main__":
    sys.exit(main())
