#!/usr/bin/env python3
"""
⭑ CEVAP UZAYI KAPISI ⭑ — Faz 2'nin birinci teslimatı
================================================================================
Faz 1'in kırmızı takımı, on yedi mekanizma ailesinin DOKUZUNDA tekillik
"ispatının" bir totoloji olduğunu gösterdi. Tekrar eden kusur aynıydı:

    SAYIM ALANINI, CEVABI ZATEN BİLEN YAZAR TANIMLIYORDU.

Yazarın seçtiği bir alan üzerinde yapılan ispat hiçbir şeyi ispatlamaz.
Bir örnek yeter: "bu tasnif bulmacasının cevap alanı şu altı yorumdur"
cümlesini yazan kişi, yedinci yorumu görmediği için yazmıştır.

BU KAPI O DÖNGÜYÜ KIRAR. Yazarın listesini OKUMAZ. Bulmacanın GİRDİSİNDEN
ve kitabın BASILI ÇİZELGELERİNDEN alanı yeniden üretir ve tek bir soru
sorar:

    Kitabın okura öğrettiği yordamlarla ulaşılabilen bütün dizeler
    içinde, BASILI kabul yordamından geçen KAÇ TANE var?

  0 → bulmaca ÇÖZÜLEMEZ   (okur mekanizmayı doğru işletir, hiçbir yere varmaz)
  1 → tekil ✅
  ≥2 → bulmacanın İKİNCİ CEVABI VAR — ve bu, çözülemez olmaktan DAHA KÖTÜDÜR:
       okur cevabını doğru sanır, doğrulama sayfası reddeder, kitabı bozuk sanır.

Sekiz denetim:

  ① her yazılmış bulmacanın makine okunur bir cevap uzayı VAR
  ② üreteç ve kabul yordamı İZİN LİSTESİNDE (yazar yeni bir tür icat edemez)
  ③ ⭑ ALAN BAĞIMSIZ AÇILDI ve ≥ minDomainSize üye taşıyor ⭑
  ④ ⭑ TAM OLARAK BİR ÜYE KABUL EDİLİYOR ⭑
  ⑤ kabul edilen üye, yazarın bildirdiği cevabın TA KENDİSİ
  ⑥ bildirilen kabul sayısı ölçülenle TUTARLI
  ⑦ ⭑ HİÇBİR İPUCU ALANIN YANLIŞ BİR ÜYESİNE GÖTÜRMÜYOR ⭑
  ⑧ 'yazar öyle diyor' biçiminde kabul yordamı YOK

⑦ NEDEN VAR: qa_hints ipucunu yalnızca DOĞRU cevaba karşı denetler. Ama bir
ipucu, alanın YANLIŞ bir üyesini adıyla vererek de bulmacayı bozar — okur
ipucunu izler, kabul edilmeyen bir dizeye varır ve kitabı bozuk sanır.

⚠ BU KAPI CEVAP İÇERİĞİ YAZDIRMAZ. Rapora yalnızca bulmaca kimliği, alan
boyu ve kabul sayısı gider. Bir sızıntı raporunun kendisinin sızıntı olması,
bu depoda düşülebilecek en gülünç tuzaktır.

Çıkış kodları:  0 = geçti   1 = kapı kırmızı   2 = kullanım hatası
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

TOOLS = os.path.join(pl.DESIGN_DIR, "tools-plate.json")

# Üreteç ve kabul yordamı İZİN LİSTESİDİR. Yasak listesi yalnızca akla gelen
# kaçamağı durdurur; izin listesi akla gelmemiş olanı da reddeder (K16).
GENERATORS = {"printed-lexicon", "printed-bestiary", "printed-beast-phrases",
              "printed-catalogue", "printed-gate-phrases", "printed-meta-list",
              "printed-phrase-list", "cyclic-shift",
              "reflection-map", "keyed-substitution", "transposition-order",
              "glyph-chart-reading", "positional-extraction"}
ACCEPTANCES = {"in-printed-lexicon", "in-printed-bestiary",
               "in-printed-phrase-list",
               "satisfies-printed-constraints", "plate-attribute",
               "table-row", "reachable-via-number-table",
               "matches-positional-extraction",
               "reachable-by-glyph-reading", "reachable-by-transposition",
               "reachable-by-printed-shift", "reachable-by-printed-grid",
               "grid-intersection",
               # ── KAPI II · YARATIKLAR ──────────────────────────────────
               "reachable-via-grid-coordinates",   # imza mekaniği (Polybius)
               "misclassified-in-printed-pens",    # sınıflama
               "reachable-by-keyed-alphabet",     # B3 · anahtarlı alfabe
               # ── FAZ 4 · KAPI III–V + META ─────────────────────────────
               "reachable-via-numeral-system",    # sayı sistemi
               "reachable-via-cyclic-calendar",   # çevrimsel takvim
               "reachable-via-path-graph",        # yol ve çizge
               "reachable-by-layered-chain",      # katmanlı zincir
               "reachable-by-back-reference",     # geriye gönderme
               "reachable-via-book-structure",    # kitabın yapısı
               "reachable-via-narrative",         # anlatıya gömülü
               "meta-synthesis"}                  # son soru

# ⚠ FAZ 2 BULGUSU — MEKANİZMA ALANI İSPAT İÇİN YETERSİZ KALABİLİR.
#
# Dört bulmacada mekanizmanın kendi ürettiği aday sayısı ikiye ve üçe kadar
# indi (glif okuma: düz/ters · sütun genişliği: 2/3/4). "İki adaydan biri
# doğru" bir tekillik ispatı DEĞİLDİR — okur zaten ikisini de deneyebilir.
#
# Doğru çerçeve terstir ve sözleşmeden gelir: okurun cevabı BASILI SÖZLÜĞÜN
# bir üyesidir (K22). Yani asıl soru şudur: altmış kabul edilebilir cevabın
# KAÇI bu mekanizmayla ulaşılabilir? Cevap bir olmalıdır.
#
# Bu yüzden küçük mekanizmalarda alan SÖZLÜKTÜR ve mekanizma KABUL
# YORDAMIDIR. İspat böylece güçlenir: yalnızca "ters okuma sözlükte yok"
# demez, "altmış üyeden yalnızca biri bu gliflerden okunabilir" der.
SMALL_MECHANISM_KINDS = {"reachable-by-glyph-reading",
                         "reachable-by-transposition",
                         "reachable-by-printed-shift",
                         "reachable-by-printed-grid"}

# ⭑ B1/K1 · ANAHTAR ARANMAZ, VERİLİR. ⭑
# Faz 2 öldürme kapısını düşüren şey buydu: okur 28 kaydırmayı ELLE
# deniyordu (84 elle işlem, en kötü 168). Anahtar levhada basılı olduğunda
# aynı bulmaca 7 işleme iner ve TEKİLLİK HİÇ ZAYIFLAMAZ — çünkü ispat
# yine altmış üyelik sözlüğün tamamını sayar, yalnızca OKUR gezmez (K25).
FORBIDDEN_ACCEPTANCE = {"author-asserted", "prose"}


# ── basılı çizelgeler ──────────────────────────────────────────────────
class Plate:
    """Kitabın ÖN MADDESİNDE basılı çizelgeler. Kabul yordamının tek
    dayanağı budur — yazarın kanaati değil."""

    def __init__(self, data: dict) -> None:
        ch = (data or {}).get("charts", {})
        self.charts = ch
        self.alphabet = ch.get("threshold-alphabet", {}).get("alphabet", "")
        self.lexicon = [e["word"] for e in
                        ch.get("threshold-lexicon", {}).get("entries", [])]
        self.phrases = ch.get("gate-sayings", {}).get("entries", [])
        self.numbers = ch.get("threshold-numbers", {}).get("entries", [])
        # ── KAPI II · basılı yetke ────────────────────────────────────
        self.bestiary = [e["word"] for e in
                         ch.get("bestiary-catalogue", {}).get("entries", [])]
        self.beastPhrases = ch.get("beast-sayings", {}).get("entries", [])

    @property
    def ok(self) -> bool:
        return bool(self.alphabet and self.lexicon)

    # ⭑ THE MARK GROUPS COME FROM THE CHART, NOT FROM ARITHMETIC ⭑
    # ⚠ These three methods used to compute `i // 5`, which silently
    # assumed a 29-letter alphabet split five-five-five-five-five-four.
    # The English alphabet is 26 letters and its groups are 5·5·4·4·4·4, so
    # the arithmetic would have put every letter from K onward in the wrong
    # group — and the gate would have accepted NOBODY while reporting a
    # clean "0 accepted" for seven puzzles. Chart A publishes `markGroups`;
    # that is the authority. The uniform fallback is kept only for
    # fixtures that predate the field.
    def _groups(self) -> list[str]:
        mg = (self.charts.get("threshold-alphabet") or {}).get("markGroups")
        if mg:
            return [g.get("letters", "") for g in mg]
        return [self.alphabet[i:i + 5] for i in range(0, len(self.alphabet), 5)]

    def group(self, ch: str) -> int:
        for i, g in enumerate(self._groups(), 1):
            if ch in g:
                return i
        raise ValueError(ch)

    def glyph_of(self, ch: str) -> str:
        for i, g in enumerate(self._groups()):
            if ch in g:
                return "',+/\\x"[i] * (g.index(ch) + 1)
        raise ValueError(ch)

    def decode_glyphs(self, seq: str) -> str | None:
        groups = self._groups()
        out = []
        for g in seq.split("│"):
            g = "".join(g.split())
            if not g or len(set(g)) != 1 or g[0] not in "',+/\\x" or len(g) > 5:
                return None
            gi = "',+/\\x".index(g[0])
            if gi >= len(groups) or len(g) > len(groups[gi]):
                return None
            out.append(groups[gi][len(g) - 1])
        return "".join(out)

    def shift(self, w: str, k: int) -> str:
        n = len(self.alphabet)
        return "".join(self.alphabet[(self.alphabet.index(c) + k) % n]
                       for c in w if c in self.alphabet)

    def reflect(self, w: str, axis: int) -> str:
        n = len(self.alphabet)
        return "".join(self.alphabet[(axis - self.alphabet.index(c)) % n]
                       for c in w if c in self.alphabet)

    def keyed_alphabet(self, key: str) -> str:
        seen, out = set(), []
        for c in key + self.alphabet:
            if c in self.alphabet and c not in seen:
                seen.add(c)
                out.append(c)
        return "".join(out)

    def keyed_decode(self, w: str, key: str) -> str:
        ka = self.keyed_alphabet(key)
        return "".join(self.alphabet[ka.index(c)] for c in w
                       if c in self.alphabet)


def col_read(ct: str, width: int) -> str:
    """Sütun sırasıyla yazılmışı satır sırasına geri çevirir."""
    n = len(ct)
    if width < 1 or width > n:
        return ""
    lens = [width] * (n // width) + ([n % width] if n % width else [])
    grid = [[""] * L for L in lens]
    i = 0
    for c in range(width):
        for r in range(len(lens)):
            if c < lens[r]:
                grid[r][c] = ct[i]
                i += 1
    return "".join("".join(r) for r in grid)


# ── ③ ALANIN BAĞIMSIZ AÇILMASI ─────────────────────────────────────────
def expand(gen: dict, plate: Plate) -> tuple[list[str], str | None]:
    """Yazarın listesini OKUMAZ; girdiden ve basılı çizelgelerden üretir."""
    kind = gen.get("kind")
    if kind == "printed-bestiary":
        return list(plate.bestiary), None
    if kind == "printed-catalogue":
        # ⭑ Kapı III–V'in kendi basılı listeleri ⭑ — her kapı kendi
        # sözlüğünü taşır; ortak bir liste bir kapının cevabını ötekine
        # gösterirdi.
        ref = gen.get("catalogueRef") or ""
        return [e["word"] for e in
                (plate.charts.get(ref) or {}).get("entries", [])], None
    if kind == "printed-gate-phrases":
        ref = gen.get("listRef") or ""
        return list((plate.charts.get(ref) or {}).get("entries", [])), None
    if kind == "printed-meta-list":
        ref = gen.get("listRef") or ""
        return list((plate.charts.get(ref) or {}).get("entries", [])), None
    if kind == "printed-beast-phrases":
        return list(plate.beastPhrases), None
    if kind == "printed-lexicon":
        return list(plate.lexicon), None
    if kind == "printed-phrase-list":
        return list(plate.phrases), None
    if kind == "cyclic-shift":
        ct = gen.get("input", "")
        return [plate.shift(ct, -k % len(plate.alphabet))
                for k in range(1, len(plate.alphabet))], None
    if kind == "reflection-map":
        ct = gen.get("input", "")
        return [plate.reflect(ct, a) for a in range(len(plate.alphabet))], None
    if kind == "keyed-substitution":
        ct = gen.get("input", "")
        return [plate.keyed_decode(ct, k) for k in plate.lexicon], None
    if kind == "transposition-order":
        ct = gen.get("input", "")
        widths = gen.get("widths") or list(range(2, max(3, len(ct))))
        return [col_read(ct, w) for w in widths if col_read(ct, w)], None
    if kind == "glyph-chart-reading":
        seq = gen.get("glyphs", "")
        parts = seq.split("│")
        out = []
        for name in gen.get("directions", ["forward", "reverse"]):
            g = "│".join(parts if name == "forward" else list(reversed(parts)))
            d = plate.decode_glyphs(g)
            if d:
                out.append(d)
        return out, None
    if kind == "positional-extraction":
        src, pos = gen.get("sources") or [], gen.get("positions") or []
        if not src or len(src) != len(pos):
            return [], "positional-extraction kaynak/konum sayısı uyuşmuyor"
        return ["".join(s[p - 1] for s, p in zip(src, pos))], None
    return [], "bilinmeyen üreteç türü: %s" % kind


# ── ④ BASILI KABUL YORDAMI ─────────────────────────────────────────────
def _constraint_ok(word: str, c: dict, plate: Plate) -> bool:
    op = c.get("op")
    if op == "length":
        return len(word) == c["value"]
    if op == "first-letter-group":
        return plate.group(word[0]) == c["value"]
    if op == "last-letter-group":
        return plate.group(word[-1]) == c["value"]
    if op == "nth-letter-group":
        n = c["n"]
        return len(word) >= n and plate.group(word[n - 1]) == c["value"]
    if op == "has-repeated-letter":
        return (len(set(word)) != len(word)) is bool(c["value"])
    return False



def grid_consistent(acc: dict, plate: Plate) -> tuple[bool, str]:
    """⭑ § 14 · KENDİNE GÖNDERMELİ TEKİLLİK YASAĞI ⭑

    Kesişim ızgarası ancak ETİKETLERİ DOĞRUYSA basılı veridir. Yazar
    "üçüncü satır III. gruptur" diye yazıp içine IV. gruptan bir sözcük
    koyarsa, okurun okuduğu şey artık bir kural değil bir iddiadır — ve
    tekillik yazarın sözüne dayanır.

    Bu yüzden her hücre KENDİ satır ve sütun etiketine karşı denetlenir.
    Tutmuyorsa kabul yordamı hiçbir üyeyi kabul etmez ve kapı kırmızı
    yanar; sessizce doğru cevabı vermez."""
    grid = acc.get("grid") or []
    rl, cl = acc.get("rowLabels") or [], acc.get("colLabels") or []
    if not grid or len(grid) != len(rl):
        return False, "ızgara satır sayısı etiket sayısıyla uyuşmuyor"
    for i, row in enumerate(grid):
        if len(row) != len(cl):
            return False, "%d. satır sütun sayısıyla uyuşmuyor" % (i + 1)
        for j, w in enumerate(row):
            # ⚠ Hücre BASILI bir listenin üyesi olmalı — hangi listenin
            # olduğunu ÜRETEÇ belirler (Kapı I sözlük, Kapı II katalog) ve
            # onu § ③ bağımsız açılım zaten denetler. Buradaki soru daha
            # dar: hücre uydurulmuş bir sözcük mü?
            if w not in plate.lexicon and w not in plate.bestiary:
                return False, "%s basılı bir listede yok" % w
            if not _constraint_ok(w, rl[i], plate):
                return False, "%d. satırın etiketi hücresine uymuyor" % (i + 1)
            if not _constraint_ok(w, cl[j], plate):
                return False, "%d. sütunun etiketi hücresine uymuyor" % (j + 1)
    flat = [w for row in grid for w in row]
    if len(set(flat)) != len(flat):
        return False, "ızgarada tekrarlanan sözcük var"
    return True, "ızgara etiketleriyle tutarlı"


# ═══ KAPI II · YARATIKLAR — üç yeni kabul yordamı ══════════════════════
def _grid_cell(chart: dict, r: int, c: int) -> str:
    """Basılı ızgaranın (satır, sütun) gözü — BİR TABANLI, okur gibi."""
    rows = chart.get("rows") or []
    if not (1 <= r <= len(rows)):
        return ""
    row = rows[r - 1]
    if not (1 <= c <= len(row)):
        return ""
    return row[c - 1]


def decode_grid(pairs, chart: dict) -> str:
    out = []
    for pr in pairs or []:
        if not (isinstance(pr, (list, tuple)) and len(pr) == 2):
            return ""
        ch = _grid_cell(chart, pr[0], pr[1])
        if not ch or ch == "·":
            return ""
        out.append(ch)
    return "".join(out)


def misclassified(acc: dict) -> tuple[str, int]:
    """(yanlış ağıldaki üye, kaç kural açıklıyor).

    ⭑ SINIFLAMA · § 14 ⭑ Okur kuralı BULUR, kural okura VERİLMEZ. Ama
    kural yazarın kafasında da durmaz: basılı NİTELİK TABLOSUNDAN
    hesaplanır. Bir kural, ağıl bölümlemesini TAM OLARAK BİR üye hariç
    açıklıyorsa o üye yanlış ağıldadır.

    ⚠ Tekillik için AÇIKLAYAN KURAL DA tek olmalıdır: iki kural aynı
    bölümlemeyi iki AYRI üye hariç açıklıyorsa okurun iki savunulabilir
    cevabı olur ve bulmaca çöker."""
    items = acc.get("items") or []
    attrs = acc.get("attributes") or {}
    pens = acc.get("pens") or {}
    hits = []
    for rule in acc.get("candidateRules") or []:
        wrong = [w for w in items
                 if bool(attrs.get(w, {}).get(rule)) != (pens.get(w) == "A")]
        if len(wrong) == 1:
            hits.append(wrong[0])
    return (hits[0] if len(set(hits)) == 1 and hits else ""), len(set(hits))


def keyed_decode_row(ct: str, row: str, alphabet: str) -> str:
    """Basılı anahtarlı satırla ÇÖZME — okur satırı KURMAZ, KULLANIR.

    Levha iki satır basar: üstte düz alfabe, altta anahtarlı satır.
    Okur şifreli harfi ALT satırda bulur, ÜSTTEKİNİ okur. Harf başına
    tek bakış; yirmi dokuz harfi yeniden dizmek YOK (B3 + yönerge § 6)."""
    if len(row) != len(alphabet):
        return ""
    out = []
    for c in ct:
        if c not in row:
            return ""
        out.append(alphabet[row.index(c)])
    return "".join(out)


# ═══ FAZ 4 · SEKİZ YENİ KABUL YORDAMI ══════════════════════════════════
def _table_of(plate: Plate, ref: str) -> dict:
    return plate.charts.get(ref) or {}


def numeral_value(symbols: str, chart: dict) -> int | None:
    """Basılı sayı çizelgesiyle bir sembol dizisini SAYIYA çevirir.

    ⭑ K1 · DEĞERLER BASILIDIR ⭑ Okur bir sistemi ezberlemez; çizelgeye
    bakar. Zorluk, sembolün DEĞERİNİ hatırlamak değil, dizinin nasıl
    TOPLANDIĞINI fark etmektir (büyükten küçüğe eklenir; küçük bir sembol
    büyüğün SOLUNDAysa çıkarılır)."""
    vals = {e["symbol"]: e["value"] for e in chart.get("entries", [])}
    toks = [c for c in symbols if c in vals]
    if not toks or len(toks) != len([c for c in symbols if not c.isspace()]):
        return None
    total, i = 0, 0
    while i < len(toks):
        v = vals[toks[i]]
        if i + 1 < len(toks) and vals[toks[i + 1]] > v:
            total += vals[toks[i + 1]] - v
            i += 2
        else:
            total += v
            i += 1
    return total


def cyclic_index(a: int, b: int, na: int, nb: int) -> int | None:
    """İki çevrimin kesiştiği TEK konum (Çin kalan teoremi · ebob 1).

    ⭑ Bu ailenin 'aha'sı şudur: iki küçük çevrim birlikte ÇOK BÜYÜK bir
    çevrim yapar ve bir tarih o büyük çevrimde TEK bir yere düşer."""
    if a < 1 or b < 1 or a > na or b > nb:
        return None
    for k in range(na * nb):
        if k % na == (a - 1) % na and k % nb == (b - 1) % nb:
            return k + 1
    return None


def walk_path(grid, start, moves) -> str:
    """Basılı ızgarada bir YOL yürür ve uğradığı harfleri toplar."""
    # ⚠ THE STEP LETTERS ARE THE ENGLISH ONES. The pilot used the Turkish
    # compass initials and "D" meant EAST there; in English "D" means DOWN.
    # A shared table would have silently walked one of the two the wrong
    # way, so there is only one table and it is the printed one.
    D = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}
    r, c = start
    out = []
    for m in moves:
        d = D.get(m)
        if not d:
            return ""
        r, c = r + d[0], c + d[1]
        if not (0 <= r < len(grid) and 0 <= c < len(grid[r])):
            return ""
        ch = grid[r][c]
        if ch and ch != "·":
            out.append(ch)
    return "".join(out)


def accepts(word: str, acc: dict, plate: Plate) -> bool:
    kind = acc.get("kind")
    if kind == "in-printed-lexicon":
        return word in plate.lexicon
    if kind == "in-printed-bestiary":
        return word in plate.bestiary
    if kind == "in-printed-phrase-list":
        return word in plate.phrases
    if kind == "satisfies-printed-constraints":
        if word not in plate.lexicon:
            return False
        return all(_constraint_ok(word, c, plate)
                   for c in acc.get("constraints", []))
    if kind == "plate-attribute":
        if word not in acc.get("labels", []):
            return False
        attrs, rule = acc.get("attributes", {}), acc.get("rule", {})
        if rule.get("op") == "eq-companion":
            return attrs.get(word) == acc.get("compare", {}).get(word)
        v, want = attrs.get(word), rule.get("value")
        return v == want if rule.get("op") == "==" else v != want
    if kind == "table-row":
        # ⭑⭑ BİR TEKİLLİK İSPATI, İSPATLADIĞI ŞEYİ VARSAYAMAZ ⭑⭑
        #
        # ⚠ FAZ 5 · LINE EDITOR BULGUSU. `g2-016`'nın süzgeçleri İKİ
        # taneydi: biri okurun sayfadan aldığı sütun, ÖTEKİ `take`
        # sütununa yazılmış ve değeri BULMACANIN KENDİ CEVABIYDI.
        # (Değerler burada YAZILMAZ; bu dosya takip edilir ve kanarya
        # ilk yazımda tam da bu yorumu yakaladı — haklıydı.)
        # İkincisi bir süzgeç değil, cevabın kopyasıdır. Onunla ispat
        # daima tek üye bulur ve kapı YEŞİL YANAR — ama okurun elinde o
        # süzgeç YOKTUR ve sayfa ona İKİ satır bırakır. Bulmacanın iki
        # cevabı vardı ve tekillik ispatı bunu göremiyordu, çünkü
        # ispatın kendisi daireseldi.
        #
        # `take` sütununa yapılan bir süzgeç ATILIR. İspat artık okurun
        # gerçekten sahip olduğu süzgeçlerle koşar.
        take, rows = acc.get("take", "ad"), acc.get("table", [])
        reader_filters = [f for f in acc.get("filters", [])
                          if f.get("col") != take]
        hits = []
        for row in rows:
            if all((row.get(f["col"]) == f["value"]) == (f["op"] == "==")
                   for f in reader_filters):
                hits.append(row.get(take))
        return word in hits
    if kind == "reachable-via-number-table":
        # ⭑ SEKİZ OKUMANIN TAMAMI AÇILIR. ⭑
        # Eski kurgu yalnızca yazarın seçtiği okumaya bakıyordu ve bu bir
        # totolojiydi: "doğru okuma doğru cevabı verir." Ölçüldüğünde
        # sekiz okumanın beşi tabloda çıktı — yani okurun yanlış köşeden
        # başlaması BEŞ ayrı geçerli cevap üretiyordu ve kapı bunu
        # görmüyordu. Artık bütün okumalar tabloya vurulur.
        rows = acc.get("table", [])
        quads = acc.get("readings") or [acc.get("reading", "")]
        for q in quads:
            for row in rows:
                if row.get("reading") == q:
                    idx = row.get("lexiconNo", 0)
                    if 1 <= idx <= len(plate.lexicon) and \
                            word == plate.lexicon[idx - 1]:
                        return True
        return False
    if kind == "reachable-by-glyph-reading":
        parts = acc.get("glyphs", "").split("│")
        reach = set()
        for name in acc.get("directions", ["forward", "reverse"]):
            g = "│".join(parts if name == "forward" else list(reversed(parts)))
            d = plate.decode_glyphs(g)
            if d:
                reach.add(d)
        return word in reach
    if kind == "reachable-by-transposition":
        ct = acc.get("input", "")
        return word in {col_read(ct, w) for w in acc.get("widths", [])}
    if kind == "reachable-by-printed-shift":
        # Alan basılı sözlüktür; kabul yordamı BASILI kaydırmadır.
        # accept(w) ⟺ w'nin basılı k kadar kaydırılmışı, sayfadaki dizedir.
        k, ct = acc.get("shift"), acc.get("input", "")
        if k is None or not ct:
            return False
        return plate.shift(word, k) == ct

    if kind == "reachable-by-printed-grid":
        ct, w = acc.get("input", ""), acc.get("width")
        return bool(ct) and w is not None and word == col_read(ct, w)

    if kind == "grid-intersection":
        # ⭑ K1/K5 · KESİŞİM ⭑ Okur ızgarayı taramaz: bir koşul SATIRI, öteki
        # SÜTUNU seçer ve cevap kesişimde durur. "Aha" işi kesişim fikrinin
        # kendisidir; transkripsiyon işi iki kenar okumaktır.
        ok, _why = grid_consistent(acc, plate)
        if not ok:
            return False
        rl, cl = acc.get("rowLabels") or [], acc.get("colLabels") or []
        rr, cr = acc.get("rowRule") or {}, acc.get("colRule") or {}
        ri = [i for i, r in enumerate(rl) if r == rr]
        ci = [j for j, c in enumerate(cl) if c == cr]
        if len(ri) != 1 or len(ci) != 1:
            return False          # koşul satırı/sütunu tekil seçmiyor
        return word == acc["grid"][ri[0]][ci[0]]

    if kind == "reachable-via-grid-coordinates":
        # ⭑ İSPAT BÜTÜN OKUMALARI AÇAR ⭑ — yanlış çapadan başlayan veya
        # ters dönen okurun GEÇERLİ bir cevaba düşemediğini göstermek
        # için. OKUR tek okuma yapar: çapa levhada basılıdır (K25).
        chart = plate.charts.get(acc.get("gridRef") or "") or {}
        reads = acc.get("readings") or [acc.get("coordinates")]
        return any(decode_grid(r, chart) == word for r in reads)

    if kind == "misclassified-in-printed-pens":
        who, n = misclassified(acc)
        return bool(who) and n == 1 and word == who

    if kind == "reachable-by-keyed-alphabet":
        row = acc.get("keyedRow") or ""
        return keyed_decode_row(acc.get("input", ""), row,
                                plate.alphabet) == word

    if kind == "reachable-via-numeral-system":
        chart = _table_of(plate, acc.get("numeralRef") or "")
        n = numeral_value(acc.get("symbols", ""), chart)
        cat = acc.get("catalogue") or []
        return bool(n) and 1 <= n <= len(cat) and word == cat[n - 1]

    if kind == "reachable-via-cyclic-calendar":
        k = cyclic_index(acc.get("a", 0), acc.get("b", 0),
                         acc.get("cycleA", 0), acc.get("cycleB", 0))
        cat = acc.get("catalogue") or []
        return bool(k) and 1 <= k <= len(cat) and word == cat[k - 1]

    if kind == "reachable-via-path-graph":
        # ⭑ İSPAT BÜTÜN YOLLARI AÇAR ⭑ — okur bir yol yürür; ispat
        # yanlış yolların GEÇERLİ bir cevaba varmadığını gösterir.
        for mv in acc.get("paths") or [acc.get("moves", "")]:
            if walk_path(acc.get("grid") or [],
                         tuple(acc.get("start") or (0, 0)), mv) == word:
                return True
        return False

    if kind == "reachable-by-layered-chain":
        # İki basılı dönüşüm ARDIŞIK uygulanır. Anahtarların ikisi de
        # levhada basılıdır (K1); okur aramaz, uygular.
        cur = acc.get("input", "")
        for st in acc.get("stages") or []:
            k = st.get("kind")
            if k == "shift":
                cur = plate.shift(cur, -int(st.get("by", 0)) % len(plate.alphabet))
            elif k == "grid":
                cur = col_read(cur, int(st.get("width", 0)))
            elif k == "reflect":
                ax, n = int(st.get("axis", 0)), len(plate.alphabet)
                cur = "".join(plate.alphabet[(ax - plate.alphabet.index(c)) % n]
                              for c in cur if c in plate.alphabet)
            else:
                return False
            if not cur:
                return False
        return cur == word

    if kind == "reachable-by-back-reference":
        # ⭑ GERİYE GÖNDERME ⭑ Anahtar, ÖNCEKİ BİR KAPININ cevabıdır ve
        # okurun elindedir. Yayılma yarıçapı qa_handoff'ta denetlenir.
        key = acc.get("key", "")
        table = acc.get("table") or []
        take = acc.get("take", "ad")
        hits = [r.get(take) for r in table if r.get(acc.get("keyColumn", "key")) == key]
        return word in hits

    if kind == "reachable-via-book-structure":
        # ⭑ § 14 · KENDİNE GÖNDERMELİ TEKİLLİK YASAĞI ⭑
        # İlk kurgu "cevap yazarın koyduğu değerdir" diyordu ve bu bir
        # TOTOLOJİydi — K21'in öldürmeye çalıştığı şeyin ta kendisi.
        #
        # Kitabın yapısı zaten BASILIDIR: çizelgelerin satırları, sıra
        # numaraları, başlıkları. Gönderme oraya yapılır ve kabul yordamı
        # o basılı yapıdan HESAPLANIR.
        #
        # ⚠ SAYFA NUMARASI AYRI BİR ŞEYDİR ve dizgiye bağlıdır (K12);
        # Faz 5'te dizgi dondurulduktan sonra `pageLocked` alanı gelir.
        chart = plate.charts.get(acc.get("structureRef") or "") or {}
        entries = chart.get("entries") or []
        i = acc.get("index", 0)
        if not (1 <= i <= len(entries)):
            return False
        e = entries[i - 1]
        val = e.get("word") if isinstance(e, dict) else e
        return pl.squeeze(val or "") == pl.squeeze(word)

    if kind == "reachable-via-narrative":
        text = acc.get("passage", "")
        words = [w.strip(".,;:!?—…\"'()") for w in text.split()]
        idx = acc.get("wordIndex", 0)
        if not (1 <= idx <= len(words)):
            return False
        return pl.squeeze(words[idx - 1]) == pl.squeeze(word)

    if kind == "meta-synthesis":
        # ⭑ SON SORU ⭑ Beş kapının ifadesi BİRLEŞTİRİLMEZ; her biri bir
        # KONUM verir ve konumlar tek bir sözcüğü kurar. § 8: "the meta
        # layer must require a final inference."
        src = acc.get("gatePhrases") or []
        pos = acc.get("positions") or []
        if not src or len(src) != len(pos):
            return False
        # ⭑ KONUM SONDAN SAYILIR ⭑ ve çıkarımın kendisi budur: baştan
        # sayan okur beş harf alır, onların bir sözcük OLMADIĞINI görür ve
        # yönü çevirir. İspat da sondan sayar — yoksa kapı, okurun yapması
        # beklenen çıkarımı atlamış olurdu.
        try:
            built = "".join(pl.squeeze(s)[-p] for s, p in zip(src, pos))
        except IndexError:
            return False
        return pl.squeeze(word) == pl.squeeze(built)

    if kind == "matches-positional-extraction":
        src, pos = acc.get("sources") or [], acc.get("positions") or []
        if not src or len(src) != len(pos):
            return False
        # ⭑ KAPI II · KONUM İKİ YÖNLÜ ⭑ Levha her satırın yanına sayımın
        # hangi UÇTAN başladığını basar. Yön verilmemişse baştandır (Kapı I).
        dirs = acc.get("directions") or ["head"] * len(src)
        if len(dirs) != len(src):
            return False
        try:
            built = "".join(w[p - 1] if d == "head" else w[len(w) - p]
                            for w, p, d in zip(src, pos, dirs))
        except IndexError:
            return False
        return pl.squeeze(word) == pl.squeeze(built)
    return False


# ── ⑦ YAKIN KAÇIRMA KÜMESİ ─────────────────────────────────────────────
def near_miss(domain: list[str], acc: dict, plate: Plate,
              answer: str) -> list[str]:
    """Alanın TEHLİKELİ üyeleri: okurun mekanizmayı işletirken gerçekten
    varabileceği YANLIŞ dizeler.

    ⚠ Bu küme neden bütün alan DEĞİL: alan çoğu bulmacada basılı sözlüğün
    tamamıdır (altmış üye) ve o üyelerin çoğu sıradan Türkçe sözcüklerdir.
    'KİLİT' bir sözlük üyesidir ve 'kilit taşı' sıradan bir tamlamadır —
    bütün alana karşı denetlemek, her ipucuyu gürültüyle kırmızı yakar.
    Gürültülü bir kapı kapatılan kapıdır.

    Tehlikeli olan dar kümedir: aynı levhanın DİĞER etiketleri, aynı
    çizelgenin DİĞER satırları, aynı mekanizmanın DİĞER okumaları ve
    kabul koşullarının BİRİ HARİÇ hepsini sağlayan üyeler. Bir ipucu
    bunlardan birini adıyla anarsa okuru gerçekten yanlış yere götürür."""
    kind = acc.get("kind")
    out: list[str] = []
    if kind == "plate-attribute":
        out = list(acc.get("labels", []))
    elif kind == "table-row":
        take = acc.get("take", "ad")
        out = [r.get(take, "") for r in acc.get("table", [])]
    elif kind == "reachable-via-number-table":
        out = [plate.lexicon[r["lexiconNo"] - 1]
               for r in acc.get("table", [])
               if 1 <= r.get("lexiconNo", 0) <= len(plate.lexicon)]
    elif kind == "in-printed-phrase-list" or \
            kind == "matches-positional-extraction":
        out = list(plate.phrases)
    elif kind == "reachable-by-glyph-reading":
        parts = acc.get("glyphs", "").split("│")
        for name in ("forward", "reverse"):
            g = "│".join(parts if name == "forward" else list(reversed(parts)))
            d = plate.decode_glyphs(g)
            if d:
                out.append(d)
    elif kind == "grid-intersection":
        out = [w for row in acc.get("grid") or [] for w in row]
    elif kind == "reachable-via-grid-coordinates":
        chart = plate.charts.get(acc.get("gridRef") or "") or {}
        out = [decode_grid(r, chart) for r in (acc.get("readings") or [])]
    elif kind == "misclassified-in-printed-pens":
        out = list(acc.get("items") or [])
    elif kind in ("reachable-via-numeral-system",
                  "reachable-via-cyclic-calendar"):
        out = list(acc.get("catalogue") or [])[:12]
    elif kind == "reachable-via-path-graph":
        out = [walk_path(acc.get("grid") or [],
                         tuple(acc.get("start") or (0, 0)), mv)
               for mv in (acc.get("paths") or [])]
    elif kind == "reachable-by-back-reference":
        out = [r.get(acc.get("take", "ad")) for r in acc.get("table") or []]
    elif kind == "meta-synthesis":
        out = list(domain)
    elif kind == "reachable-by-keyed-alphabet":
        row, ct = acc.get("keyedRow") or "", acc.get("input", "")
        out = [keyed_decode_row(ct, row, plate.alphabet)]
        # ters yön: okurun satırı yanlış yöne okuması
        if len(row) == len(plate.alphabet):
            out.append("".join(row[plate.alphabet.index(c)] for c in ct
                               if c in plate.alphabet))
    elif kind == "reachable-by-transposition":
        ct = acc.get("input", "")
        out = [col_read(ct, w) for w in acc.get("widths", [])]
    elif kind == "reachable-by-printed-grid":
        ct = acc.get("input", "")
        out = [col_read(ct, w) for w in (2, 3, 4, 5)]
    elif kind == "reachable-by-printed-shift":
        ct = acc.get("input", "")
        out = [plate.shift(ct, -k % len(plate.alphabet))
               for k in range(1, len(plate.alphabet))]
    elif kind == "satisfies-printed-constraints":
        cons = acc.get("constraints", [])
        for w in domain:
            miss = sum(0 if _constraint_ok(w, c, plate) else 1 for c in cons)
            if miss <= 1:
                out.append(w)
    elif kind == "in-printed-lexicon":
        out = list(domain)          # üretilmiş adaylar: çoğu anlamsız dize
    return [w for w in dict.fromkeys(out)
            if w and pl.squeeze(w) != pl.squeeze(answer)
            and len(pl.squeeze(w)) >= 4]


# ---------------------------------------------------------------------------
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
    print("  ⭑ CEVAP UZAYI ⭑ · kapı: %s" % gate_level)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    spec = cfg.get("solvability", {}).get("answerSpace", {})
    min_dom = spec.get("minDomainSize", 6)

    pre = pl.preflight(rep, gate_level, "cevap uzayı")
    if pre is None:
        return rep.finish("denetlenecek cevap uzayı yok", args.json)
    need, sols, designs = pre

    # Buraya ulaşıldıysa korumalı katman VARDIR (preflight aksi hâlde None
    # döndürür). Yani çizelgelerin okunamaması gerçek bir kusurdur: kabul
    # yordamının dayanağı yoktur.
    plate = Plate(pl.load_json(TOOLS) or {})
    if not plate.ok:
        rep.check(False, "⛔ korumalı katman VAR ama basılı çizelgeler "
                         "okunamadı (%s) — kabul yordamı DAYANAKSIZ"
                  % os.path.relpath(TOOLS, pl.ROOT))
        return rep.finish("çizelge yok", args.json)
    print("  basılı çizelge: alfabe %d harf · sözlük %d üye · ifade %d · "
          "sayı %d" % (len(plate.alphabet), len(plate.lexicon),
                       len(plate.phrases), len(plate.numbers)))

    missing, bad_kind, small, not_one = [], [], [], []
    wrong_member, counter_bad, hint_wrong, forbidden = [], [], [], []
    sizes: dict[str, int] = {}
    checked = 0
    near_total = 0

    print("\n── alanların bağımsız açılması ──")
    inconsistent: list[str] = []
    for p in need:
        pid = p["puzzleId"]
        rec = sols.get(pid) or {}
        dsg = designs.get(pid) or {}
        space = rec.get("answerSpace") or dsg.get("answerSpace")

        # ① var mı
        if not isinstance(space, dict) or not space.get("generator"):
            missing.append(pid)
            continue
        checked += 1
        gen, acc = space["generator"], space.get("acceptance") or {}

        # ② izin listesi + ⑧ yasak kabul yordamı
        if gen.get("kind") not in GENERATORS:
            bad_kind.append("%s üreteç '%s'" % (pid, gen.get("kind")))
        if acc.get("kind") in FORBIDDEN_ACCEPTANCE:
            forbidden.append("%s kabul '%s'" % (pid, acc.get("kind")))
        elif acc.get("kind") not in ACCEPTANCES:
            bad_kind.append("%s kabul '%s'" % (pid, acc.get("kind")))
            continue

        # ②b ⭑ BASILI VERİ GERÇEKTEN BASILI VERİ Mİ ⭑ (§ 14)
        if acc.get("kind") == "grid-intersection":
            ok, why = grid_consistent(acc, plate)
            if not ok:
                inconsistent.append("%s — %s" % (pid, why))

        # ③ BAĞIMSIZ AÇILIM
        domain, err = expand(gen, plate)
        if err:
            bad_kind.append("%s — %s" % (pid, err))
            continue
        domain = list(dict.fromkeys(domain))
        sizes[pid] = len(domain)
        if len(domain) < min_dom:
            small.append("%s (alan %d < %d)" % (pid, len(domain), min_dom))

        # ④ tam olarak bir kabul
        ok_members = [d for d in domain if accepts(d, acc, plate)]
        if len(ok_members) != 1:
            not_one.append("%s (kabul edilen %d)" % (pid, len(ok_members)))

        # ⑤ kabul edilen üye yazarın cevabı mı
        want = pl.squeeze(rec.get("finalAnswer", ""))
        if len(ok_members) == 1 and pl.squeeze(ok_members[0]) != want:
            wrong_member.append(pid)

        # ⑥ bildirilen sayaç
        declared = space.get("declaredAcceptedCount")
        if declared is not None and declared != len(ok_members):
            counter_bad.append("%s (bildirilen %s ≠ ölçülen %d)"
                               % (pid, declared, len(ok_members)))

        # ⑦ ipucu YAKIN KAÇIRMA kümesinden birini adıyla veriyor mu
        wrong_pool = near_miss(domain, acc, plate, rec.get("finalAnswer", ""))
        near_total += len(wrong_pool)
        for i, hint in enumerate(rec.get("hints") or [], 1):
            hs = pl.squeeze(hint)
            for w in wrong_pool:
                if pl.squeeze(w) in hs:
                    hint_wrong.append("%s kademe %d" % (pid, i))
                    break

    rep.facts.update({"checked": checked,
                      "domainMin": min(sizes.values()) if sizes else 0,
                      "domainMax": max(sizes.values()) if sizes else 0,
                      "domainTotal": sum(sizes.values()),
                      "minDomainSizeRequired": min_dom,
                      "nearMissCandidates": near_total})

    rep.check(not inconsistent,
              "⭑ KESİŞİM IZGARALARININ ETİKETLERİ BASILI VERİYLE TUTARLI ⭑"
              + ("" if not inconsistent else " — ⛔ %s" % inconsistent[:4]))
    rep.check(not missing,
              "her yazılmış bulmacanın makine okunur cevap uzayı var"
              + ("" if not missing else " — ⛔ UZAYSIZ: %s" % missing[:5]))
    rep.check(not bad_kind,
              "üreteç ve kabul yordamı İZİN LİSTESİNDE"
              + ("" if not bad_kind else " — TANIMSIZ: %s" % bad_kind[:5]))
    rep.check(not forbidden,
              "⭑ 'yazar öyle diyor' biçiminde kabul yordamı YOK ⭑"
              + ("" if not forbidden else " — ⛔ TOTOLOJİ: %s" % forbidden[:5]))
    rep.check(not small,
              "⭑ ALAN BAĞIMSIZ AÇILDI ve ≥%d üye taşıyor ⭑" % min_dom
              + ("" if not small else " — ⛔ SAYIM YOK: %s" % small[:5]))
    rep.check(not not_one,
              "⭑ TAM OLARAK BİR ÜYE KABUL EDİLİYOR ⭑"
              + ("" if not not_one else " — ⛔ TEKİL DEĞİL: %s" % not_one[:5]))
    rep.check(not wrong_member,
              "kabul edilen üye bildirilen cevabın TA KENDİSİ"
              + ("" if not wrong_member
                 else " — ⛔ AYRIŞMA: %s" % wrong_member[:5]))
    rep.check(not counter_bad,
              "bildirilen kabul sayısı ölçülenle tutarlı"
              + ("" if not counter_bad else " — ÇELİŞKİ: %s" % counter_bad[:5]))
    rep.check(not hint_wrong,
              "⭑ HİÇBİR İPUCU ALANIN YANLIŞ BİR ÜYESİNE GÖTÜRMÜYOR ⭑"
              + ("" if not hint_wrong
                 else " — ⛔ YANLIŞ YÖNLENDİRME: %s" % hint_wrong[:5]))

    return rep.finish(
        "%d bulmaca · %d aday dize bağımsız üretildi ve elendi"
        % (checked, sum(sizes.values())), args.json)


if __name__ == "__main__":
    sys.exit(main())
