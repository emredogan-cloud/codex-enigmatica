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
GENERATORS = {"printed-lexicon", "printed-phrase-list", "cyclic-shift",
              "reflection-map", "keyed-substitution", "transposition-order",
              "glyph-chart-reading", "positional-extraction"}
ACCEPTANCES = {"in-printed-lexicon", "in-printed-phrase-list",
               "satisfies-printed-constraints", "plate-attribute",
               "table-row", "reachable-via-number-table",
               "matches-positional-extraction",
               "reachable-by-glyph-reading", "reachable-by-transposition"}

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
                         "reachable-by-transposition"}
FORBIDDEN_ACCEPTANCE = {"author-asserted", "prose"}


# ── basılı çizelgeler ──────────────────────────────────────────────────
class Plate:
    """Kitabın ÖN MADDESİNDE basılı çizelgeler. Kabul yordamının tek
    dayanağı budur — yazarın kanaati değil."""

    def __init__(self, data: dict) -> None:
        ch = (data or {}).get("charts", {})
        self.alphabet = ch.get("esik-alfabesi", {}).get("alphabet", "")
        self.lexicon = [e["word"] for e in
                        ch.get("esik-sozlugu", {}).get("entries", [])]
        self.phrases = ch.get("kapi-sozleri", {}).get("entries", [])
        self.numbers = ch.get("esik-sayilari", {}).get("entries", [])

    @property
    def ok(self) -> bool:
        return bool(self.alphabet and self.lexicon)

    def group(self, ch: str) -> int:
        i = self.alphabet.index(ch)
        return i // 5 + 1

    def glyph_of(self, ch: str) -> str:
        i = self.alphabet.index(ch)
        return "',+/\\x"[i // 5] * (i % 5 + 1)

    def decode_glyphs(self, seq: str) -> str | None:
        out = []
        for g in seq.split("│"):
            g = "".join(g.split())
            if not g or len(set(g)) != 1 or g[0] not in "',+/\\x" or len(g) > 5:
                return None
            i = "',+/\\x".index(g[0]) * 5 + len(g) - 1
            if i >= len(self.alphabet):
                return None
            out.append(self.alphabet[i])
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


def accepts(word: str, acc: dict, plate: Plate) -> bool:
    kind = acc.get("kind")
    if kind == "in-printed-lexicon":
        return word in plate.lexicon
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
        take, rows = acc.get("take", "ad"), acc.get("table", [])
        hits = []
        for row in rows:
            if all((row.get(f["col"]) == f["value"]) == (f["op"] == "==")
                   for f in acc.get("filters", [])):
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
                if row.get("dortlu") == q:
                    idx = row.get("sozlukNo", 0)
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
    if kind == "matches-positional-extraction":
        src, pos = acc.get("sources") or [], acc.get("positions") or []
        if not src or len(src) != len(pos):
            return False
        built = "".join(s[p - 1] for s, p in zip(src, pos))
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
        out = [plate.lexicon[r["sozlukNo"] - 1]
               for r in acc.get("table", [])
               if 1 <= r.get("sozlukNo", 0) <= len(plate.lexicon)]
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
    elif kind == "reachable-by-transposition":
        ct = acc.get("input", "")
        out = [col_read(ct, w) for w in acc.get("widths", [])]
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

    plate = Plate(pl.load_json(TOOLS) or {})
    if not plate.ok:
        rep.check(False, "⛔ basılı çizelgeler okunamadı (%s) — kabul yordamı "
                         "DAYANAKSIZ" % os.path.relpath(TOOLS, pl.ROOT))
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
