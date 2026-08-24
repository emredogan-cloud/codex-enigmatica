#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KAPAK VE A+ PROMPT KATALOĞU — gravür dışı varlıkların brifi
================================================================================
`plate_prompts.py` yüz üç GRAVÜR promptunu bulmacaların kendi şeklinden
ÜRETİR. Bu modül onun yapamadığı ikisini taşır:

    KAPAK      iki ayrı konsept · ön kapak sanatı
    A+         altı modül · Amazon ürün sayfası

────────────────────────────────────────────────────────────────────────
⭑ NEDEN AYRI MODÜL ⭑

Gravür promptu ÖLÇÜLÜR: veri bölümü bulmacanın şeklinden türer ve elle
yazılamaz. Kapak ve A+ promptu ÖLÇÜLMEZ — onlar ticari birer karardır ve
kaynakları `BRIEF.md`dir. İkisini aynı dosyada tutmak, ölçülen ile
karar verileni karıştırmak olurdu.

⚠ VE İKİSİ DE AYNI İKİ KURALA TABİDİR:

  ① GÖRSELDE METİN YOK. Başlık, yazar adı ve A+ kopyası CLI ve Amazon'un
    kendi alanları tarafından dizilir. Bir görsele gömülen metin, dil
    değiştiğinde görselin yeniden üretilmesini zorunlu kılar.
  ② CEVAP YOK. Ürün sayfası herkese açıktır; oraya düşen bir cevap
    kitabın içindekinden DAHA GENİŞ yayılır.

⚠ TİCARİ MESAJ UYDURULMAZ. Aşağıdaki her modülün `claim` alanı
`BRIEF.md § 4` (dört satın alma gerekçesi) ve `§ 6` (beş farklılaşma)
içindeki ONAYLI ifadelere dayanır. Yeni bir iddia eklenmez.
"""
from __future__ import annotations

# ⚠ PROMPT GÖVDESİ İNGİLİZCEDİR, KÜNYE TÜRKÇE.
# Gerekçe: prompt gövdesi bir GÖRSEL MODELE girer ve gravür promptları
# zaten İngilizcedir; karışık dilli bir kütüphane kurucuyu her kartta dil
# değiştirmeye zorlar ve modelin tutarlılığını düşürür. Künye, sinyal ve
# ticari dayanak KURUCUYA aittir ve deponun dilinde kalır.

# ═══ ORTAK ═══════════════════════════════════════════════════════════
# Kapak ve A+ görselleri gravür DEĞİLDİR: iç blok tek renk, kapak ve
# ürün sayfası renklidir. Ama nesne kimliği aynı kalır.
COMMERCIAL_STYLE = (
    "Premium editorial illustration for an adult puzzle book. The look of "
    "a 17th–18th century scholar's cabinet photographed for a modern "
    "publishing catalogue: hand-inked copperplate linework over flat, "
    "restrained colour. Not fantasy art, not game-box art, not "
    "photorealistic, not 3D render, not cartoon."
)

COMMERCIAL_COLOUR = (
    "Restrained and warm: cream and aged paper, iron-gall ink black, "
    "deep indigo, oxblood red, tarnished brass, stone grey. No neon, no "
    "candy palette, no heavy gradients, no teal-and-orange grading."
)

COMMERCIAL_LIGHT = (
    "Soft, even editorial light from the upper left. Gentle contact "
    "shadows. No dramatic rim light, no god rays, no glow, no lens flare."
)

# ⭑ ORTAK OLUMSUZ KISIT ⭑
# İlk üç madde SÖZLEŞMEYİ korur, kalanı ÜSLUBU. Sırası budur.
NEGATIVE_COMMON = [
    "no text of any kind — no title, no author name, no subtitle, no "
    "tagline, no caption, no page number, no signature",
    "no letters, no words, no numerals, no invented script, no rune-like "
    "or glyph-like marks that a reader could try to decode",
    "no logo, no publisher mark, no barcode, no ISBN block, no watermark, "
    "no QR code",
    "no solved puzzle, no filled-in grid, no answer key, no marked "
    "solution path",
    "no modern objects — no screens, no phones, no laptops, no plastic",
    "no people, no faces, no hands",
    "no fantasy clichés — no wizards, no dragons, no glowing runes, no "
    "magic particles, no arcane energy",
    "no photorealism, no 3D render look, no CGI sheen, no HDR",
    "no blur, no bokeh, no vignette, no film grain overlay, no dust "
    "scratches, no distressed texture filter",
    "no colour banding, no neon, no oversaturation",
    "no cluttered edges — the outer margin stays calm",
]

# ═══ KAPAK ════════════════════════════════════════════════════════════
# ⚠ SIRT GEOMETRİSİ BURADA YOKTUR VE OLAMAZ.
# Sırt genişliği sayfa sayısından türer; iç blok Faz 5'te DONDURULMADI
# (gerçek levhalar gelmeden dondurulamaz · K12). Bu yüzden burada
# yalnızca ÖN KAPAK sanatı istenir; sarmal, sayfa sayısı kesinleştikten
# sonra seçilen ön kapaktan ve dizgi araçlarından kurulur.
COVER_TRIM = "6 × 9 in"
COVER_ASPECT = "2 : 3 (dikey)"
COVER_PIXELS = "1800 × 2700 px · 300 dpi · RGB"

COVERS = [
    {
        "id": "cover-option-01",
        "name": "SEÇENEK 01 — “BİLGİNİN MASASI”",
        "concept": (
            "An antiquarian puzzle table in a scholar's cabinet, arranged "
            "as a researcher would leave it at the end of a working day: "
            "engraved copper plates, cipher wheels, manuscripts, "
            "geometric puzzle objects, a folded map, astronomical "
            "markings, wax seals and fragments of a mechanical puzzle."),
        "signal": (
            "Zekâ · gizem · keşif · bilim · zarafet · meydan okuma · "
            "el işçiliği. Pahalı bir koleksiyoncu cildi gibi durur; bir "
            "çocuk etkinlik kitabı gibi DEĞİL."),
        "composition": (
            "The table seen from slightly above, three-quarter angle. One "
            "strong focal object: an open book of engraved plates at the "
            "centre. Around it, in the order a scholar would leave them — "
            "a brass cipher wheel turned half a step, two copper plates "
            "laid one over the other, the edge of a folded map, a rule "
            "and a pair of dividers, and a row of BLANK wax seal "
            "impressions. Detail density FALLS from the centre toward the "
            "edges: the upper third and the lower fifth stay calm."),
        "safe": (
            "TOP 22% — a calm band for the title and subtitle: dark, "
            "flat, low-detail ground.\n"
            "BOTTOM 15% — a calm band for the author name and series "
            "line.\n"
            "Neither band may contain high-contrast detail that would "
            "fight typography set over it."),
        "claim": "BRIEF § 4.3 nesne değeri · § 4.1 meydan okuma",
    },
    {
        "id": "cover-option-02",
        "name": "SEÇENEK 02 — “BÜYÜK BULMACA ARŞİVİ”",
        "concept": (
            "A great puzzle archive seen from directly above: engraved "
            "copper plates, rotating cipher wheels, layered diagrams, "
            "folded maps, sealed documents, geometric marks and antique "
            "instruments — with fine, deliberate lines connecting some of "
            "them."),
        "signal": (
            "“Her şeyin arkasında gizli bir düzen var.” Premium · "
            "entelektüel · merak uyandırıcı · editoryal · tarihsel. "
            "Fantezi-oyun klişesi YOK."),
        "composition": (
            "STRICT TOP-DOWN, flat overhead view. Objects are laid out as "
            "an archivist would sort them: close to a grid but NOT "
            "perfectly aligned. Fine engraved lines between them imply an "
            "order — some objects are linked, others are not — and the "
            "pattern must read as a SYSTEM, never as a legible diagram. A "
            "clear opening is left at the centre and the composition "
            "spreads outward from it. NO triptych, NO three panels — one "
            "continuous surface."),
        "safe": (
            "CENTRE — a calm opening for the title: roughly a 30% × 20% "
            "rectangle of flat ground at the middle of the frame.\n"
            "BOTTOM 15% — a calm band for the author name.\n"
            "Connecting lines must NOT enter either zone."),
        "claim": "BRIEF § 6.3 tek meta-mister · § 6.1 levhanın içindeki şifre",
    },
]

COVER_NEGATIVE = NEGATIVE_COMMON + [
    "no spine, no back cover, no wrap-around layout — FRONT COVER ART "
    "ONLY; the print wrap is assembled later from this artwork",
    "no book mockup, no 3D book on a shelf, no perspective book object",
    "no border frame that would be cropped by trim",
    "no three-panel or triptych layout",
]

# ═══ A+ İÇERİK ════════════════════════════════════════════════════════
# ⚠ ÖLÇÜLER VE MODÜL TÜRLERİ UYDURULMADI. Portföyün üretimde kullanılan
# A+ spesifikasyonundan alındı (THE-MYTH-HUNTERS-FIELD-BOOK ·
# 07_ASSETS/IMAGE_PROMPT_LIBRARY.html § 9.3). Codex Enigmatica'nın kendi
# A+ üretim betiği (`aplus.py`) Faz 6 teslimatıdır ve henüz yoktur.
APLUS_SPEC = {
    "overlay": ("Standard Image & Text Overlay", "1940 × 600 px",
                "min kabul alanı 970 × 300"),
    "header": ("Standard Image Header with Text", "1940 × 600 px",
               "min kabul alanı 970 × 300"),
    "sidebar": ("Standard Single Image & Sidebar", "600 × 600 px",
                "kare · min 220 × 220"),
    "leftimage": ("Standard Single Left Image", "600 × 600 px",
                  "kare · min 220 × 220"),
}

APLUS = [
    {
        "id": "aplus-01",
        "name": "MODÜL 01 — CODEX ENIGMATICA'NIN DÜNYASI",
        "module": "overlay",
        "purpose": (
            "Tek cümlelik vaat: bu bir bulmaca kitabı değil, gizli bir "
            "sistemi olan bir NESNE."),
        "claim": "BRIEF § 4.3 nesne değeri · § 1 tek cümlede",
        "concept": (
            "A premium antiquarian puzzle archive holding every visual "
            "puzzle form in the book at once: engraved plates, cipher "
            "wheels, geometric diagrams, incised marks, aged paper and "
            "measuring instruments."),
        "composition": (
            "Wide horizontal banner. Objects THIN OUT from left to right: "
            "the left third is dense and rich, the right third is calm and "
            "nearly empty. Nothing readable anywhere — marks on paper read "
            "as hatching and measuring ticks, never as letterforms."),
        "safe": "RIGHT 40% — kept flat and low-contrast; the module heading and body\n"
            "text are set in Amazon's own fields, not in this image",
    },
    {
        "id": "aplus-02",
        "name": "MODÜL 02 — BİR BULMACANIN ANATOMİSİ",
        "module": "sidebar",
        "purpose": (
            "Farklılaştırıcı: şifre levhanın YANINDA değil, İÇİNDEDİR."),
        "claim": "BRIEF § 6.1 bulmaca levhanın İÇİNDE",
        "concept": (
            "A carefully ordered scholar's worktable showing the "
            "relationship between observation, pattern, logic, cipher and "
            "inference through PHYSICAL objects — never through an "
            "interface or a screen."),
        "composition": (
            "Square composition, strict top-down. A single engraved plate "
            "at the centre; the instruments used to read it arranged "
            "around it in a loose ring — a lens, dividers, a rule, a "
            "cipher wheel, one blank sheet. The hatching on the plate's "
            "own surface looks regular and COUNTABLE, but spells "
            "nothing."),
        "safe": "RIGHT edge — kept calm for the Amazon sidebar text, which is set\n"
            "outside this image",
    },
    {
        "id": "aplus-03",
        "name": "MODÜL 03 — KEŞİF DENEYİMİ",
        "module": "leftimage",
        "purpose": (
            "Satın alma gerekçesi: üç kademeli ipucu — pes etmenize izin "
            "verilir."),
        "claim": "BRIEF § 6.2 üç kademeli ipucu",
        "concept": (
            "A visual transformation: raw observation becoming a hidden "
            "pattern becoming a discovery — told entirely through imagery, "
            "with no words and no arrows."),
        "composition": (
            "Square composition built in three physical layers. At the "
            "bottom, a flat unread engraved surface; over it, a "
            "semi-transparent measuring sheet; above both, one small "
            "lens ring in which a region of the same surface resolves "
            "into "
            "something ORDERED and sharp. NO arrows, NO labels, NO "
            "numbers — the sequence is carried only by depth and "
            "focus."),
        "safe": "RIGHT half — kept calm; module text is set in Amazon's own field",
    },
    {
        "id": "aplus-04",
        "name": "MODÜL 04 — GÖZLEMDEN ÇIKARIMA",
        "module": "sidebar",
        "purpose": (
            "Deneyim vaadi: yüksek düşünce, düşük sürtünme — iş değil "
            "fark etmek."),
        "claim": "BRIEF § 4.1 meydan okuma · § 4.4 süre",
        "concept": (
            "A close, measured composition of several engraved plates "
            "with exactly ONE quiet anomaly among them."),
        "composition": (
            "Square composition. Six similar engraved plates in two rows "
            "of three. Five share the same arrangement; one differs in a "
            "single detail — a wider margin, one missing incision. The "
            "anomaly is NOT highlighted, NOT lit, NOT circled: the viewer "
            "finds it unaided. Which plate differs is a COMPOSITION "
            "choice and is not the answer to anything in the book."),
        "safe": "SAĞ kenar · Amazon sidebar metni ayrı alanda",
    },
    {
        "id": "aplus-05",
        "name": "MODÜL 05 — KAPILARDAN GEÇEN YOLCULUK",
        "module": "header",
        "purpose": (
            "Kapsam: beş kapı, yüz bulmaca, yükselen derinlik."),
        "claim": "BRIEF § 1 tek cümlede · § 6.3 tek meta-mister",
        "concept": (
            "A visual journey through several successive thresholds: "
            "distinct objects, rising complexity, increasing depth and a "
            "convergence at the end."),
        "composition": (
            "Wide horizontal banner. FIVE distinct clusters of objects "
            "from left to right; each cluster is one step more layered "
            "than the one before it. Fine engraved lines run between the "
            "clusters and draw together toward a single point on the "
            "right. NO labels, NO stage names, NO numbered steps — "
            "progression is carried only by density and convergence."),
        "safe": "TOP 30% — kept flat; the heading is set in Amazon's header field",
    },
    {
        "id": "aplus-06",
        "name": "MODÜL 06 — SON AÇILIŞ",
        "module": "overlay",
        "purpose": (
            "Kapanış: yüz bulmacanın çıktısı tek bir son soruya bağlanır "
            "ve cevap doğrulama sayfasına yazılır."),
        "claim": "BRIEF § 6.3 tek meta-mister · § 6.4 doğrulanabilir çözüm",
        "concept": (
            "A final scene of resolution: a completed scholar's archive, "
            "an opened manuscript, engraved plates brought into alignment, "
            "a cipher wheel, and one SEALED, unopened envelope."),
        "composition": (
            "Wide horizontal banner seen from slightly above. On the left, "
            "work that has been finished and put in order; on the right, "
            "standing alone, a sealed and UNOPENED envelope. The envelope "
            "is blank and bears no writing of any kind. The scene should "
            "feel like resolution while REVEALING nothing: the final "
            "answer is not printed in the book and is not printed here."),
        "safe": "LEFT 40% — kept flat and low-contrast; module text is set in\n"
            "Amazon's own field",
    },
]

APLUS_NEGATIVE = NEGATIVE_COMMON + [
    "no headline, no body copy, no call to action baked into the image — "
    "Amazon's own module fields carry all commercial text",
    "no book cover reproduction, no title lettering on any object",
    "no star ratings, no review quotes, no badges, no price",
    "no readable page content — pages show hatching and measuring marks "
    "only",
]


def commercial_prompt(item: dict, negative: list, extra: str = "") -> str:
    """Kopyalanabilir TEK blok — kurucunun görsel modele vereceği şey.

    ⚠ Kompozisyon, üslup, renk, ışık ve güvenli alan TEK METİNDE
    birleşir. Kurucu üç ayrı yerden derleme yapmak zorunda kalmaz;
    kopyala düğmesi yalnızca bunu kopyalar."""
    parts = [
        item["concept"].strip(),
        "",
        "COMPOSITION — " + item["composition"].strip(),
        "",
        "STYLE — " + COMMERCIAL_STYLE,
        "",
        "COLOUR — " + COMMERCIAL_COLOUR,
        "",
        "LIGHT — " + COMMERCIAL_LIGHT,
        "",
        "TEXT-SAFE AREA — " + item["safe"].replace("\n", " ").strip()
        + " Bu alan düz ve sakin kalır; tipografi sonradan dizilir.",
    ]
    if extra:
        parts += ["", extra.strip()]
    parts += [
        "",
        "ABSOLUTE CONSTRAINTS — " + "; ".join(negative[:4]) + ".",
    ]
    return "\n".join(parts)
