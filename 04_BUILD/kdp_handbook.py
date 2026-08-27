#!/usr/bin/env python3
"""
KDP YÜKLEME EL KİTABI — kurucunun panelde izleyeceği adımlar
================================================================================
İki dosya üretir:

  08_OUTPUT/KDP_UPLOAD_HANDBOOK.md    başvuru metni
  08_OUTPUT/KDP_UPLOAD_GUIDE.html     Türkçe · çevrimdışı · etkileşimli

⚠ BU BELGE BİR ŞEYİN HAZIR OLDUĞUNU İDDİA ETMEZ — DOSYA SİSTEMİNE BAKAR.

Her gerekli dosyanın durumu üretim anında ÖLÇÜLÜR. Bir el kitabının en
tehlikeli hâli, olmayan bir dosyayı "hazır" göstermesidir: kurucu KDP
panelini açar, dosyayı arar, bulamaz ve hangi tarafın yanıldığını
bilemez. Bu yüzden hazırlık göstergesi elle yazılmaz, `os.path.exists`
ile doldurulur.

⚠ VE ÜÇ DURUM BİRLEŞTİRİLMEZ:
  🔵 AJAN HAZIRLADI     dosya var ve ölçüldü
  🟢 KURUCU EYLEMİ      yalnızca insan yapabilir (panel · onay · yayın)
  🔴 HENÜZ YOK          bilerek üretilmedi ya da bloklayıcı var

Çıkış kodları:  0 = üretildi   1 = hata
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402
import prompt_catalog as CAT                                   # noqa: E402

META = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "metadata.json")
OUT_MD = os.path.join(pl.ROOT, "08_OUTPUT", "KDP_UPLOAD_HANDBOOK.md")
OUT_HTML = os.path.join(pl.ROOT, "08_OUTPUT", "KDP_UPLOAD_GUIDE.html")

READY, PENDING, BLOCKED = "hazır", "bekliyor", "yok"


def probe(rel: str, kind: str = "file", need: int = 1) -> dict:
    """⭑ DOSYA GERÇEKTEN VAR MI ⭑ — iddia değil, ölçüm."""
    path = os.path.join(pl.ROOT, rel)
    if kind == "dir":
        n = (len([f for f in os.listdir(path) if f.endswith(".png")])
             if os.path.isdir(path) else 0)
        return {"path": rel, "n": n, "need": need,
                "state": READY if n >= need else PENDING}
    ok = os.path.isfile(path)
    size = os.path.getsize(path) if ok else 0
    return {"path": rel, "n": 1 if ok else 0, "need": 1, "bytes": size,
            "state": READY if ok else PENDING}


def collect(meta: dict) -> dict:
    """Yüklemenin ihtiyaç duyduğu her dosyanın durumu."""
    return {
        "plates": probe("07_ASSETS/plates", "dir", 103),
        "coverFront": probe("07_ASSETS/print", "dir", 2),
        "aplus": probe("07_ASSETS/web", "dir", 6),
        # ⚠ İÇ BLOK PDF'İ YOK ve bu bilerek böyledir: dizgi DONDURULMADI
        # (K12) ve gerçek levhalar yeni geldi. Var gibi göstermek,
        # kurucuyu olmayan bir dosyayı aramaya göndermektir.
        # ⚠ YOLLAR GERÇEK ÇIKTIYLA AYNI OLMAK ZORUNDA. Önceki sürümde
        # burada var olmayan adlar yazılıydı ve el kitabı, üretilmiş
        # dosyaları "bekliyor" gösteriyordu — kurucuyu hazır bir dosyayı
        # aramaya göndermek, olmayan bir dosyayı hazır göstermek kadar
        # kötüdür.
        "interiorPb": probe("08_OUTPUT/PAPERBACK/interior.pdf"),
        "coverPb": probe("08_OUTPUT/PAPERBACK/cover.pdf"),
        "metaPb": probe("08_OUTPUT/PAPERBACK/metadata.json"),
        "sumsPb": probe("08_OUTPUT/PAPERBACK/SHA256SUMS"),
        "aplusPkg": probe("08_OUTPUT/APLUS", "dir", 6),
        "interiorHc": probe("08_OUTPUT/HARDCOVER/interior.pdf"),
        "wrapHc": probe("08_OUTPUT/HARDCOVER/cover.pdf"),
        "kindleEpub": probe("08_OUTPUT/KINDLE/codex-enigmatica.epub"),
        "kindleCover": probe("08_OUTPUT/KINDLE/cover.jpg"),
        "wrapRaw1": probe("07_ASSETS/raw/%s" % CAT.WRAPS[0]["file"]),
        "wrapRaw2": probe("07_ASSETS/raw/%s" % CAT.WRAPS[1]["file"]),
    }


# ── KURUCUYA AİT EYLEMLER ─────────────────────────────────────────────────
# ⚠ § 31: ajanın YAPAMAYACAĞI şeyler. Bunların "yapıldı" görünmesi bu
# projedeki en pahalı yalandır — kurucu yayımlandığını sanır.
FOUNDER_ONLY = [
    ("KDP hesabına giriş ve panel kullanımı",
     "Ajan tarayıcıda hesabınıza giremez, giremeyecektir."),
    ("Previewer'da sayfa sayfa görsel onay",
     "Bir insanın bakması gerekir; ölçüm bunu değiştirmez."),
    ("⭑ YAPAY ZEKÂ İÇERİK BEYANINI KDP PANELİNDE SİZ TAMAMLARSINIZ ⭑",
     "Hukuki bir beyandır ve yalnızca siz verebilirsiniz. Ajan bir değer "
     "UYDURMADI ve uydurmayacak: `metadata.json → "
     "founderPending.aiDisclosureConfirmed` HÂLÂ false ve öyle kalacak. "
     "KDP, YZ-ÜRETİMİ metin/görsel/çevirinin bildirilmesini ister; "
     "YZ-DESTEKLİ içerik için bildirim gerekmez — ayrımı siz yaparsınız."),
    ("⭑ ISBN'İ KDP PANELİNDE SİZ GİRERSİNİZ ⭑",
     "`founderPending.isbn` BOŞ ve bilerek boş. Ajan ISBN üretmedi, "
     "tahmin etmedi, yeniden kullanmadı ve YER TUTUCU BASMADI — basılmış "
     "yanlış bir ISBN geri alınamaz. KDP ücretsiz ISBN mi, kendi "
     "ISBN'iniz mi: karar sizin ve panelde girilir."),
    ("⭑ KINDLE TELİF PLANINI SİZ SEÇERSİNİZ ⭑",
     "Ölçüm: EPUB 46,3 MB → %70 planında teslimat ücreti 6,95 $ "
     "(46,3 × 0,15 $) ve telif 2,13 $; %35 planında telif 3,50 $. "
     "Yani BU DOSYADA %35 daha çok kazandırır ve başabaş nokta "
     "~33,3 MB'dır. Formül KDP'nin kendi telif sayfasından alındı: "
     "%70 × (liste − KDV − teslimat). Seçim panelde sizindir."),
    ("Yazar biyografisi",
     "`founderPending.authorBio` boş. Yer tutucu basmak geri alınamaz."),
    ("Fiziksel POD provası (A9)",
     "Gravürlerin nokta yayılması altındaki davranışı YALNIZCA basılı "
     "provada ölçülür. Ekranda kusursuz görünen levha kâğıtta kapanabilir."),
    ("⭑ DOĞRULAMA ALAN ADININ KAYDI ⭑",
     "Kitap `valicepress.com/codex-enigmatica/verify` adresini SON "
     "YAPRAĞINA BASAR. Alan adı 26 Ağustos 2026'da KAYITSIZ ölçüldü "
     "(~11,25 $/yıl) — yani serbest, ama BİZİM DEĞİL. Alan adı kaydı bir "
     "ÖDEME işlemidir ve ajan yapamaz. ⚠ BASILMIŞ BİR URL DÜZELTİLEMEZ: "
     "alan adı başkasının eline geçerse satılmış her nüsha okuru yabancı "
     "bir siteye gönderir."),
    ("⭑ DOĞRULAMA SAYFASININ YAYINA ALINMASI ⭑",
     "Vercel projesi şu an `live: false` ve üretim hedefi `target: null` "
     "— site HİÇBİR YERDE yayında değildir. Sayfa yayına alınmadan kitap "
     "BASILAMAZ; `qa_verification.py` `release` kapısını KIRMIZI tutar."),
    ("⭑ DOĞRULAMA SIRLARININ VERCEL'E GİRİLMESİ ⭑",
     "`CODEX_VERIFY_PEPPER` ve `CODEX_VERIFY_DIGEST`. Üretimi: "
     "`node scripts/codex-verify-digest.mjs` — cevabı STDIN'den okur, "
     "dosyaya ve kabuk geçmişine YAZMAZ. ⚠ Sunucuda düz cevap saklanmaz; "
     "saklanan şey biberli SHA-256 özetidir. İkisi de depoda DEĞİLDİR."),
    ("Publish düğmesi",
     "Yayımlama kararı kurucuya aittir."),
    ("A+ içeriğinin moderasyona gönderilmesi",
     "Amazon insan moderasyonu uygular; ajan gönderemez."),
]


def steps(meta: dict, files: dict) -> list:
    """A–G bölümleri. Her adım § 28'deki yedi başlığı taşır."""
    ed = {e["id"]: e for e in meta["editions"]}
    pages = meta["pageCount"]
    return [
        ("A", "PAPERBACK", "📕", [
            {
                "id": "pb-1", "flag": "🔵",
                "adim": "İç blok dosyasını hazırla",
                "ne": "6×9 inç trim, krem kâğıt, siyah mürekkep iç blok "
                      "PDF'i. Sayfa modeli %d sayfa ölçtü." % pages,
                "nere": "Bookshelf → Create → Paperback → "
                        "Manuscript → Upload paperback manuscript",
                "gir": "—",
                "dosya": files["interiorPb"]["path"],
                "kontrol": "Kenar boşluğu (gutter) sayfa sayısına bağlıdır: "
                           "%d sayfa için KDP iç kenarda daha geniş pay "
                           "ister. Levha sayfalarında kırpma olmamalı."
                           % pages,
                "basari": "KDP 'Manuscript uploaded successfully' der ve "
                          "Previewer açılır.",
                "state": files["interiorPb"]["state"],
            },
            {
                "id": "pb-2", "flag": "🔵",
                "adim": "Kapak dosyasını hazırla",
                "ne": "Paperback SARMAL kapak (arka + sırt + ön), tek PDF — "
                      "ÜRETİLDİ.",
                "nere": "Paperback Content → Book Cover → Upload a "
                        "cover you already have",
                "gir": "—",
                "dosya": files["coverPb"]["path"],
                "kontrol": "Sırt ÖLÇÜLEN sayfa sayısından türetildi. "
                           "Previewer'da sırt yazısının ortalandığını ve "
                           "barkod alanının boş olduğunu doğrulayın.",
                "basari": "KDP kapağı kabul eder ve Previewer açılır.",
                "state": files["coverPb"]["state"],
            },
            {
                "id": "pb-3", "flag": "🟢",
                "adim": "Fiyat ve dağıtım",
                "ne": "Liste fiyatı %s $ (paperback)." % ed["paperback"]["list"],
                "nere": "Paperback Rights & Pricing",
                "gir": "%s USD" % ed["paperback"]["list"],
                "dosya": "—",
                "kontrol": "Basım maliyeti sayfa sayısıyla değişir; "
                           "%d sayfa değişirse telif de değişir." % pages,
                "basari": "KDP net telif tutarını gösterir.",
                "state": PENDING,
            },
        ]),
        ("B", "HARDCOVER", "📗", [
            {
                "id": "hc-1", "flag": "🔵",
                "adim": "İç blok (hardcover)",
                "ne": "Aynı iç blok, hardcover trim ve pay kurallarıyla.",
                "nere": "Create → Hardcover → Manuscript",
                "gir": "—",
                "dosya": files["interiorHc"]["path"],
                "kontrol": "Hardcover'da KDP daha geniş iç pay ve "
                           "menteşe (hinge) payı ister; paperback "
                           "dosyası olduğu gibi KULLANILAMAZ.",
                "basari": "Yükleme kabul edilir ve Previewer açılır.",
                "state": files["interiorHc"]["state"],
            },
            {
                "id": "hc-2", "flag": "🔵",
                "adim": "Kapak (hardcover)",
                "ne": "Hardcover sarmal — ÜRETİLDİ. Sırt 0,7833 in, menteşe "
                      "0,394 in, tam kapak 14,359 × 10,417 in. Değerler "
                      "hardcover-calculator.png'den OKUNDU.",
                "nere": "Hardcover Content → Book Cover",
                "gir": "—",
                "dosya": files["wrapHc"]["path"],
                "kontrol": "Hardcover sarmalı ayrı şablondur (14,359 in — "
                           "ciltsizin 12,910'u DEĞİL). Previewer'da menteşe "
                           "ve sırtı doğrulayın.",
                "basari": "KDP kapağı kabul eder ve Previewer açılır.",
                "state": files["wrapHc"]["state"],
            },
        ]),
        ("C", "KINDLE", "📱", [
            {
                "id": "kd-1", "flag": "🔵",
                "adim": "Kindle EPUB'ını yükle",
                "ne": "Akışkan EPUB 3 · 18 bölüm · 99 gravür · kapak "
                      "YALNIZCA ÖN (1600 × 2560).",
                "nere": "Bookshelf → Create → Kindle eBook → "
                        "Content → Upload eBook manuscript",
                "gir": "—",
                "dosya": "08_OUTPUT/KINDLE/codex-enigmatica.epub",
                "kontrol": "⭑ TELİF PLANI: dosya 46 MB. %70 planı "
                           "teslimat ücreti keser ve kitap başına "
                           "0,09 $ bırakır; %35 planı 3,50 $ bırakır. "
                           "%35 SEÇİN (ya da EPUB 23 MB altına indirilsin). "
                           "Previewer'da levhaların yakınlaştığını doğrulayın.",
                "basari": "Önizleyici bölümleri ve levhaları gösterir.",
                "state": files["kindleEpub"]["state"],
            },
        ]),
        ("D", "A+ İÇERİK", "🖼", [
            {
                "id": "ap-1", "flag": "🔵",
                "adim": "Altı A+ modül görselini yükle",
                "ne": "Görseller METİNSİZDİR; başlık ve gövde metni "
                      "Amazon'un kendi alanlarına yazılır.",
                "nere": "Bookshelf → ⋯ → Edit A+ Content → Create A+ Content",
                "gir": "Her modülün başlık ve gövde metni (aşağıda "
                       "kopyalanabilir).",
                "dosya": "07_ASSETS/web/ (%d/6 hazır)"
                         % files["aplus"]["n"],
                "kontrol": "Modül türü ve piksel ölçüsü kartla aynı "
                           "olmalı. Görselde metin GÖRÜNMEMELİ.",
                "basari": "Önizlemede görsel + metin ayrı ayrı görünür.",
                "state": files["aplus"]["state"],
            },
            {
                "id": "ap-2", "flag": "🟢",
                "adim": "Moderasyona gönder",
                "ne": "Amazon insan moderasyonu uygular (birkaç gün).",
                "nere": "A+ Content → Submit for approval",
                "gir": "—",
                "dosya": "—",
                "kontrol": "Reddedilirse gerekçe e-postayla gelir; en "
                           "sık sebep görselde metin olmasıdır.",
                "basari": "Durum 'Submitted' → 'Approved' olur.",
                "state": PENDING,
            },
        ]),
        ("E", "SON ÖNİZLEME", "🔍", [
            {
                "id": "pv-1", "flag": "🟢",
                "adim": "Previewer'da sayfa sayfa bak",
                "ne": "Özellikle 103 levha sayfası.",
                "nere": "Paperback/Hardcover Content → Launch Previewer",
                "gir": "—",
                "dosya": "—",
                "kontrol": "Her levhada: kırpılma yok · çizgiler kapanmamış "
                           "· sayılabilir işaretler sayılabilir · sayfa "
                           "numarası levhanın üstüne binmiyor.",
                "basari": "Previewer hata vermez ve levhalar okunur.",
                "state": PENDING,
            },
            {
                "id": "pv-2", "flag": "🟢",
                "adim": "Fiziksel prova (A9)",
                "ne": "Basılı prova kopya sipariş edilir.",
                "nere": "Proof or author copy",
                "gir": "—",
                "dosya": "—",
                "kontrol": "⭑ EKRAN PROVASI BUNUN YERİNE GEÇMEZ. Nokta "
                           "yayılması yalnızca kâğıtta ölçülür.",
                "basari": "Elinizde basılı kopya olur ve levhalar "
                          "ÖLÇÜLEREK doğrulanır.",
                "state": PENDING,
            },
        ]),
        ("F", "FİYAT", "💰", [
            {
                "id": "pr-1", "flag": "🟢",
                "adim": "Liste fiyatlarını gir",
                "ne": "Hardcover %s $ · Paperback %s $"
                      % (ed["hardcover"]["list"], ed["paperback"]["list"]),
                "nere": "Rights & Pricing",
                "gir": "Yukarıdaki tutarlar",
                "dosya": "—",
                "kontrol": "Sayfa sayısı değişirse basım maliyeti ve "
                           "dolayısıyla telif değişir — fiyat modeli "
                           "%d sayfaya göre kuruldu." % pages,
                "basari": "KDP her pazar için telif tutarını gösterir.",
                "state": PENDING,
            },
        ]),
        ("G", "YAYIMLAMA", "🚀", [
            {
                "id": "pubtwo", "flag": "🟢",
                "adim": "Yapay zekâ içerik beyanı",
                "ne": "KDP, AI kullanımını sorar. Bu bir HUKUKİ BEYANDIR.",
                "nere": "Paperback Details → AI-Generated Content",
                "gir": "Kendi doğru cevabınız",
                "dosya": "—",
                "kontrol": "`founderPending.aiDisclosureConfirmed` = "
                           "false. Ajan bunu sizin yerinize dolduramaz.",
                "basari": "Beyan kaydedilir.",
                "state": PENDING,
            },
            {
                "id": "pub-2", "flag": "🟢",
                "adim": "Publish",
                "ne": "Yayımlama kararı.",
                "nere": "Publish Your Paperback Book",
                "gir": "—",
                "dosya": "—",
                "kontrol": "⭑ BU KİTAP HİÇBİR İNSANIN ELİNDE "
                           "ÇÖZÜLMEDİ. Harici çözücü oturumu: 0/5 "
                           "(A12b). Ölçülen öldürme kapısı kararı "
                           "HARD-STOP'tur.",
                "basari": "Kitap 24–72 saat içinde yayında olur.",
                "state": PENDING,
            },
        ]),
    ]


def copy_fields(meta: dict) -> list:
    """§ 30 — panelde kopyalanacak her alan."""
    fp = meta["founderPending"]
    out = [
        ("Başlık", meta["title"]),
        ("Alt başlık", meta["subtitle"]),
        ("Yazar", meta["author"]),
        ("Yayıncı", meta["publisher"]),
        ("Seri", "%s · cilt %d" % (meta["series"]["name"],
                                   meta["series"]["volume"])),
        ("Açıklama", meta["description"]),
    ]
    out += [("Anahtar kelime %d" % (i + 1), k)
            for i, k in enumerate(meta["keywords"])]
    out += [("Kategori %d" % (i + 1), "%s — %s" % (b["code"], b["label"]))
            for i, b in enumerate(meta["bisac"])]
    # ⚠ BOŞ ALAN BOŞ GÖSTERİLİR. Yer tutucu basmak geri alınamaz bir
    # hatadır: kurucu onu gerçek sanıp panele yapıştırır.
    out.append(("Yazar biyografisi",
                fp["authorBio"] or "⛔ KURUCU YAZMADI — boş bırakılamaz"))
    out.append(("ISBN", fp["isbn"] or
                "⛔ KARAR VERİLMEDİ (strateji: %s)" % fp["isbnStrategy"]))
    return out


def verification_state() -> dict:
    """⭑ BASKIYA GİDEN KİTABIN İÇİNDEKİ ADRES ⭑

    ⚠ Bu el kitabının en tehlikeli hâli, olmayan bir şeyi "hazır"
    göstermesidir. Doğrulama adresi bu depodaki EN PAHALI TEK DİZEDİR:
    basılmış bir URL düzeltilemez. Bu yüzden durum burada `metadata`dan
    DEĞİL, tek yetkesinden — `project_config.json` — okunur ve üç ayrı
    şey ayrı ayrı gösterilir; hiçbiri ötekinin yerine geçmez.
    """
    ver = ((pl.load_config().get("founder") or {}).get("verification")) or {}
    return {
        "url": ver.get("printedUrl") or "",
        "registered": bool(ver.get("domainRegistered")),
        "deployed": bool(ver.get("deployed")),
        "live": ver.get("liveVerifiedAt"),
        "temporary": ver.get("temporary") or {},
    }


def bare(u: str) -> str:
    """Şemasız gösterim.

    ⚠ El kitabının HTML kılavuzu ÇEVRİMDIŞI çalışmak zorundadır ve bunu
    bir kapı tutar: belgede `http://` ya da `https://` GEÇEMEZ. Kural
    blunt ama haklı — bir `<img src="https://…">` kılavuzu internete
    bağımlı kılardı. Adresi şemasız basmak kuralı zayıflatmadan aynı
    bilgiyi verir, ve zaten kitaba basılan adres de şemasızdır.
    """
    return (u or "").replace("https://", "").replace("http://", "")


def verification_rows(v: dict) -> list:
    ok = "✅ EVET"
    no = "⛔ HAYIR"
    rows = [
        ("Kitaba BASILAN adres (kalıcı)", v["url"] or "⛔ SEÇİLMEDİ"),
        ("Alan adı kurucunun elinde", ok if v["registered"] else no),
        ("Kalıcı alan adı yayında", ok if v["deployed"] else no),
        ("Kalıcı adres canlı doğrulandı", v["live"] or "⛔ HİÇ"),
    ]
    t = v.get("temporary") or {}
    if t:
        live = t.get("liveState") or {}
        rows += [
            ("— — —", "— — —"),
            ("GEÇİCİ doğrulama adresi",
             bare(t.get("temporaryVerificationBaseUrl")) or "—"),
            ("Geçici adres KİTABA BASILIYOR mu",
             no if not t.get("printedInBook") else "⛔ EVET — HATA"),
            ("Geçici sayfa canlı", ok if live.get("pageLive") else no),
            ("Geçici uç nokta çalışıyor",
             ok if live.get("endpointOperational") else
             "⛔ HAYIR — " + bare(live.get("endpointBlockedBy") or "")),
        ]
    return rows


def render_md(meta: dict, files: dict, secs: list) -> str:
    """Başvuru metni — panelde değil, masada okunur."""
    L = ["# KDP YÜKLEME EL KİTABI — Codex Enigmatica", ""]
    L += ["> ⚠ **BU BELGE BİR ŞEYİN YAYIMLANDIĞINI İDDİA ETMEZ.**",
          "> Aşağıdaki her dosya durumu üretim anında dosya sistemine",
          "> bakılarak doldurulmuştur. `Publish` düğmesine yalnızca",
          "> kurucu basar.", ""]

    ready = sum(1 for s in secs for x in s[3] if x["state"] == READY)
    total = sum(len(s[3]) for s in secs)
    L += ["## 0 · Hazırlık", "",
          "| | |", "|---|---|",
          "| Ölçülen sayfa | %d |" % meta["pageCount"],
          "| Bulmaca · kapı · ipucu | %d · %d · %d |"
          % (meta["measured"]["puzzles"], meta["measured"]["gates"],
             meta["measured"]["hintCount"]),
          "| İşlenmiş levha | %d / 103 |" % files["plates"]["n"],
          "| İşlenmiş ön kapak | %d / 2 |" % files["coverFront"]["n"],
          "| İşlenmiş A+ | %d / 6 |" % files["aplus"]["n"],
          "| Ajan tarafından hazır adım | %d / %d |" % (ready, total), ""]

    # ⭑ ZORUNLU CÜMLE ⭑ — project_config § killGate.externalValidation
    # .releaseBuildOverride.mandatoryReportLine. Kurucu nihai paketin
    # üretilmesine izin verdi; İZİN VERİLEN ŞEY ÜRETİMDİR ve bu blok
    # onun bir doğrulama SANILMASINI engellemek için vardır.
    ev = ((pl.load_config().get("killGate") or {})
          .get("externalValidation") or {})
    if ev.get("founderOverride") and not ev.get("humanValidationPassed"):
        L += ["## 0.0 · ⛔ İNSAN DOĞRULAMASI YAPILMADI", "",
              "> **HUMAN VALIDATION: NOT PERFORMED — FOUNDER OVERRIDE.**",
              ">",
              "> Bu kitabı **hiçbir harici insan çözmedi.** Yapılan çözücü",
              "> oturumu: **%d**. Ölçülen öldürme kapısı kararı:"
              % ev.get("sessionsPerformed", 0),
              "> **HARD-STOP**. İnsan doğrulaması geçti mi: **HAYIR**.",
              ">",
              "> Nihai paket, kurucunun **bunu bilerek** verdiği izinle",
              "> üretildi (%s). Bu bir **risk kabulüdür**, bir doğrulama"
              % (ev.get("releaseBuildOverride", {}).get("authorisedAt")
                 or "—"),
              "> değildir — ve hiçbir rapor onu doğrulama diye yazmaz.", ""]

    v = verification_state()
    blocked = not (v["url"] and v["registered"] and v["deployed"] and v["live"])
    L += ["## 0.1 · ⭑ DOĞRULAMA SAYFASI ⭑", ""]
    t = v.get("temporary") or {}
    if t:
        L += ["> ⚠ **ALAN ADI HENÜZ KALICI DEĞİL.**",
              ">",
              "> Kalıcı adres — ve **kitaba basılan** adres — şudur:",
              "> `%s`" % v["url"],
              ">",
              "> Bu adres **henüz yayında değildir**: alan adı alınmadı.",
              "> O güne kadar doğrulama sistemi **geçici olarak** şurada",
              "> canlı test edilir: `%s`"
              % (bare(t.get("temporaryVerificationBaseUrl")) or "—"),
              ">",
              "> ⛔ **Geçici adres kitaba BASILMAZ** ve basılmadı. Bir",
              "> önizleme alan adı kiracıdır; proje adı değişince ölür,",
              "> kitap ise basılmıştır.",
              ">",
              "> ⭑ **Üretim kalıcı olarak yayına alınmış SAYILMAZ**",
              "> ta ki kurucu `valicepress.com` alan adını alıp bağlayana",
              "> kadar.", ""]
    if blocked:
        L += ["> ⛔ **BASKIYA HAZIR DEĞİL — VE BU BİR BİÇİM SORUNU DEĞİL.**",
              ">",
              "> Kitap son yaprağına bir adres **basar**. O adres canlı",
              "> değilken basmak, okura ölü bir kapı vermektir; ve alan adı",
              "> başkasının eline geçerse **satılmış her nüsha** okuru",
              "> yabancı bir siteye gönderir. Basılmış bir URL",
              "> **düzeltilemez.**", ""]
    L += ["| | |", "|---|---|"]
    for k, val in verification_rows(v):
        L += ["| %s | %s |" % (k, val)]
    L += [""]
    if blocked:
        L += ["`python3 04_BUILD/qa_verification.py --gate release --live`",
              "koşturun ve **kararı okuyun**. Üçü de yeşil olmadan",
              "`release` kapısı **KIRMIZIDIR**.", ""]

    L += ["## 1 · ⭑ YALNIZCA KURUCUNUN YAPABİLECEĞİ İŞLER ⭑", "",
          "Ajan bunları **yapmadı ve yapamaz**. Yapıldığını iddia eden",
          "bir rapor yanlıştır.", ""]
    for what, why in FOUNDER_ONLY:
        L += ["- **%s** — %s" % (what, why)]
    L += [""]

    for code, name, icon, items in secs:
        L += ["## %s · %s" % (code, name), ""]
        for it in items:
            L += ["### %s %s" % (it["flag"], it["adim"]), "",
                  "| | |", "|---|---|",
                  "| NE YAPACAĞIM | %s |" % it["ne"].replace("\n", " "),
                  "| KDP'DE NEREYE | %s |" % it["nere"],
                  "| NE GİRECEĞİM | %s |" % it["gir"].replace("\n", " "),
                  "| HANGİ DOSYA | `%s` |" % it["dosya"],
                  "| NE KONTROL EDECEĞİM | %s |" % it["kontrol"].replace("\n", " "),
                  "| BAŞARILI OLURSA | %s |" % it["basari"],
                  "| DURUM | **%s** |" % it["state"].upper(), ""]

    L += ["## H · Panele girilecek alanlar", "", "| Alan | Değer |",
          "|---|---|"]
    for k, v in copy_fields(meta):
        L += ["| %s | %s |" % (k, v.replace("\n", " ")[:300])]
    L += [""]

    L += ["## I · A+ metni (İngilizce — ürün sayfası dili)", "",
          "| Modül | Başlık | Gövde |", "|---|---|---|"]
    for m in CAT.APLUS:
        t, b = CAT.APLUS_COPY[m["id"]]
        L += ["| `%s` | %s | %s |" % (m["id"], t, b)]
    L += ["", "> Görsellerde **metin yoktur**; bu metin Amazon'un kendi",
          "> başlık ve gövde alanlarına girilir.", ""]
    return "\n".join(L)


CSS = """
:root{--bg:#faf7f2;--ink:#241f1a;--mut:#6d6459;--line:#ded5c7;
--card:#fff;--acc:#8a6a3b;--ok:#2f6b46;--warn:#8a5a1b;--bad:#8f2f2f;
--okbg:#e9f3ec;--warnbg:#f7efe1;--badbg:#f6e9e9;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
--bg:#17150f;--ink:#ece5d8;--mut:#a2988a;--line:#3a3328;--card:#1f1c15;
--acc:#c9a86a;--ok:#7fc79b;--warn:#e0b271;--bad:#e79191;
--okbg:#1b2a20;--warnbg:#2b2317;--badbg:#2c1c1c;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.65 "Iowan Old Style",Palatino,Georgia,serif;}
.wrap{max-width:980px;margin:0 auto;padding:0 20px 90px}
h1{font-size:1.9rem;margin:34px 0 6px;letter-spacing:-.01em}
h2{font-size:1.3rem;margin:44px 0 10px;padding-bottom:7px;
border-bottom:2px solid var(--line)}
h3{font-size:1.02rem;margin:0}
.sub{color:var(--mut);margin:0 0 18px}
nav{position:sticky;top:0;z-index:9;background:var(--bg);
border-bottom:1px solid var(--line);padding:9px 0;margin-bottom:6px;
display:flex;gap:6px;flex-wrap:wrap}
nav a{font:600 12px/1 ui-monospace,Menlo,monospace;color:var(--mut);
text-decoration:none;border:1px solid var(--line);border-radius:99px;
padding:6px 11px;white-space:nowrap}
nav a:hover{color:var(--ink);border-color:var(--acc)}
.bar{position:sticky;top:44px;z-index:8;background:var(--card);
border:1px solid var(--line);border-radius:12px;padding:11px 14px;
margin:8px 0 16px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.track{flex:1;min-width:170px;height:9px;background:var(--line);
border-radius:99px;overflow:hidden}
.fill{height:100%;width:0;background:var(--ok);transition:width .25s}
.cnt{font:700 13px ui-monospace,monospace}
.card{background:var(--card);border:1px solid var(--line);
border-radius:12px;padding:14px 16px;margin:12px 0}
.hd{display:flex;gap:10px;align-items:flex-start}
.hd input{margin-top:5px;width:17px;height:17px;flex:none;accent-color:var(--ok)}
table{width:100%;border-collapse:collapse;margin:10px 0;font-size:.9rem}
th,td{text-align:left;vertical-align:top;padding:7px 9px;
border-bottom:1px solid var(--line)}
th{width:210px;color:var(--mut);font-weight:600;font-size:.76rem;
text-transform:uppercase;letter-spacing:.05em}
.scroll{overflow-x:auto}
code{font:.86em ui-monospace,Menlo,monospace;background:var(--warnbg);
padding:1px 5px;border-radius:4px}
.pill{display:inline-block;font:700 10.5px/1 ui-monospace,monospace;
padding:4px 8px;border-radius:99px;text-transform:uppercase;
letter-spacing:.05em;white-space:nowrap}
.p-ok{background:var(--okbg);color:var(--ok)}
.p-wait{background:var(--warnbg);color:var(--warn)}
.p-no{background:var(--badbg);color:var(--bad)}
.note{border-left:4px solid var(--acc);background:var(--card);
padding:11px 14px;margin:13px 0;border-radius:0 9px 9px 0}
.stop{border-left-color:var(--bad);background:var(--badbg)}
.go{border-left-color:var(--ok);background:var(--okbg)}
button.c{font:600 11px ui-monospace,monospace;cursor:pointer;
background:var(--card);color:var(--mut);border:1px solid var(--line);
border-radius:7px;padding:4px 9px;margin-left:6px}
button.c:hover{border-color:var(--acc);color:var(--ink)}
.val{white-space:pre-wrap;word-break:break-word}
details{margin:8px 0}
summary{cursor:pointer;color:var(--acc);font-size:.85rem;font-weight:600}
footer{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);
color:var(--mut);font-size:.82rem}
"""

JS = """
(function(){
 var K="enigmatica-kdp-v1";
 function load(){try{return JSON.parse(localStorage.getItem(K))||{}}
   catch(e){return {}}}
 function save(s){try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}}
 var st=load();
 var boxes=[].slice.call(document.querySelectorAll('input[type=checkbox]'));
 function tick(){
   var n=boxes.filter(function(b){return b.checked}).length;
   var pct=boxes.length?Math.round(n*100/boxes.length):0;
   document.getElementById('fill').style.width=pct+'%';
   document.getElementById('cnt').textContent=n+' / '+boxes.length+
     '  ('+pct+'%)';
   var r=document.getElementById('ready');
   if(n===boxes.length){r.textContent='TÜM ADIMLAR İŞARETLİ';
     r.className='pill p-ok';}
   else {r.textContent='EKSİK ADIM VAR';r.className='pill p-wait';}
 }
 boxes.forEach(function(b){
   if(st[b.id]){b.checked=true}
   b.addEventListener('change',function(){st[b.id]=b.checked;save(st);tick()});
 });
 tick();
 document.querySelectorAll('button.c').forEach(function(b){
   b.addEventListener('click',function(){
     var el=document.getElementById(b.dataset.t); if(!el){return}
     var t=el.innerText.trim(), done=function(){
       var o=b.textContent;b.textContent='kopyalandı';
       setTimeout(function(){b.textContent=o},1100)};
     if(navigator.clipboard&&navigator.clipboard.writeText){
       navigator.clipboard.writeText(t).then(done,done)
     } else {
       var a=document.createElement('textarea');a.value=t;
       document.body.appendChild(a);a.select();
       try{document.execCommand('copy')}catch(e){}
       document.body.removeChild(a);done();
     }
   });
 });
})();
"""


def pill(state: str) -> str:
    cls = {READY: "p-ok", PENDING: "p-wait", BLOCKED: "p-no"}[state]
    txt = {READY: "AJAN HAZIRLADI", PENDING: "BEKLİYOR",
           BLOCKED: "ÜRETİLMEYECEK"}[state]
    return '<span class="pill %s">%s</span>' % (cls, txt)


def render_html(meta: dict, files: dict, secs: list) -> str:
    e = html.escape
    P = []
    A = P.append

    A('<title>KDP Yükleme Kılavuzu</title>')
    A('<style>%s</style>' % CSS)
    A('<div class="wrap">')
    A('<h1>KDP Yükleme Kılavuzu</h1>')
    A('<p class="sub"><b>%s</b> · %s · ölçülen %d sayfa · '
      'bu dosya <code>04_BUILD/kdp_handbook.py</code> tarafından '
      'üretildi — elle düzenlemeyin.</p>'
      % (e(meta["title"]), e(meta["author"]), meta["pageCount"]))

    navs = [("durum", "Durum"), ("dogrulama", "Doğrulama"),
            ("kurucu", "Kurucu işi")]
    navs += [(c.lower(), "%s · %s" % (c, n)) for c, n, _i, _x in secs]
    navs += [("alan", "Alanlar"), ("aplus", "A+ metni"),
             ("kindlenote", "Kindle notu"), ("liste", "Kontrol listesi")]
    A('<nav>%s</nav>' % "".join(
        '<a href="#%s">%s</a>' % (a, e(b)) for a, b in navs))

    A('<div class="bar"><span class="cnt" id="cnt">0 / 0</span>'
      '<span class="track"><span class="fill" id="fill"></span></span>'
      '<span class="pill p-wait" id="ready">EKSİK ADIM VAR</span></div>')

    # ── DURUM ──────────────────────────────────────────────────────────
    A('<h2 id="durum">Durum — ölçüm, iddia değil</h2>')
    A('<div class="scroll"><table>')
    for label, got, need in (
            ("İşlenmiş gravür", files["plates"]["n"], 103),
            ("İşlenmiş ön kapak", files["coverFront"]["n"], 2),
            ("İşlenmiş A+ modülü", files["aplus"]["n"], 6)):
        st = READY if got >= need else PENDING
        A('<tr><th>%s</th><td>%d / %d %s</td></tr>'
          % (label, got, need, pill(st)))
    for label, key in (("Paperback iç blok", "interiorPb"),
                       ("Hardcover iç blok", "interiorHc"),
                       ("Paperback sarmal kapak", "coverPb"),
                       ("Hardcover sarmal kapak", "wrapHc")):
        A('<tr><th>%s</th><td><code>%s</code> %s</td></tr>'
          % (label, files[key]["path"], pill(files[key]["state"])))
    A('</table></div>')

    A('<div class="note stop"><b>⚠ ÜÇ ŞEY HENÜZ YOK VE BU BİLEREK '
      'BÖYLEDİR.</b><br>'
      '① <b>İç blok PDF\'i</b> — dizgi <b>dondurulmadı</b> (K12) ve '
      'gerçek levhalar yeni geldi. Sayfa sayısı değişebilir, sırt '
      'genişliği ona bağlıdır.<br>'
      '② <b>Sarmal kapak</b> — elimizdeki kapak sanatı <b>yalnızca ön '
      'kapaktır</b>. Gerilerek sarmal yapılamaz; iki yeni sarmal '
      'promptu kütüphaneye eklendi ve <b>sizin üretmenizi bekliyor</b>.<br>'
      '③ <b>Fiziksel prova</b> — hiç alınmadı (A9).</div>')

    A('<div class="note stop"><b>⭑ VE EN ÖNEMLİSİ ⭑</b><br>'
      'Bu kitap <b>hiçbir insanın elinde çözülmedi</b>. Harici çözücü '
      'oturumu <b>0 / 5</b> (A12b). Ölçülen öldürme kapısı kararı '
      '<b>HARD-STOP</b>. Yayımlama kararı bu gerçeği bilerek '
      'verilmelidir.</div>')

    # ── ⭑ DOĞRULAMA SAYFASI ⭑ ──────────────────────────────────────────
    # ⚠ Kitap son yaprağına bir ADRES BASAR. Bu tablo `metadata`dan
    # değil tek yetkesinden okunur ve üç ayrı şeyi ayrı gösterir:
    # alan adı BİZDE mi · site YAYINDA mı · adres YANIT VERDİ mi.
    # Hiçbiri ötekinin yerine geçmez, ve üçü de yeşil olmadan bu kutu
    # kırmızıdır.
    ev = ((pl.load_config().get("killGate") or {})
          .get("externalValidation") or {})
    if ev.get("founderOverride") and not ev.get("humanValidationPassed"):
        A('<div class="note stop"><b>⛔ HUMAN VALIDATION: NOT PERFORMED '
          '— FOUNDER OVERRIDE.</b><br>'
          'Bu kitabı <b>hiçbir harici insan çözmedi</b>. Yapılan çözücü '
          'oturumu <b>%d</b>. Ölçülen öldürme kapısı kararı '
          '<b>HARD-STOP</b>. Nihai paket kurucunun <b>bunu bilerek</b> '
          'verdiği izinle üretildi — bu bir <b>risk kabulüdür</b>, bir '
          'doğrulama değildir.</div>' % ev.get("sessionsPerformed", 0))

    v = verification_state()
    blocked = not (v["url"] and v["registered"] and v["deployed"] and v["live"])
    A('<h2 id="dogrulama">⭑ Doğrulama sayfası — basılan adres</h2>')
    _t = v.get("temporary") or {}
    if _t:
        A('<div class="note stop"><b>⚠ ALAN ADI HENÜZ KALICI DEĞİL.</b><br>'
          'Kitaba <b>basılan</b> kalıcı adres: <code>%s</code><br>'
          'Bu adres <b>henüz yayında değil</b> — alan adı alınmadı. O güne '
          'kadar doğrulama <b>geçici olarak</b> şurada canlı test edilir: '
          '<code>%s</code><br>'
          '⛔ <b>Geçici adres kitaba BASILMAZ</b> ve basılmadı: bir '
          'önizleme alan adı <b>kiracıdır</b>, kitap ise basılmıştır.<br>'
          '⭑ Üretim, kurucu <code>valicepress.com</code> alan adını alıp '
          'bağlayana kadar <b>kalıcı olarak yayına alınmış sayılmaz</b>.'
          '</div>' % (e(v["url"]),
                      e(bare(_t.get("temporaryVerificationBaseUrl")) or "—")))
    if blocked:
        A('<div class="note stop"><b>⛔ BASKIYA HAZIR DEĞİL.</b><br>'
          'Kitap son yaprağına bir adres <b>basar</b>. O adres canlı '
          'değilken basmak okura <b>ölü bir kapı</b> vermektir — ve alan '
          'adı başkasının eline geçerse <b>satılmış her nüsha</b> okuru '
          'yabancı bir siteye gönderir. <b>Basılmış bir URL '
          'düzeltilemez.</b></div>')
    A('<div class="scroll"><table>')
    for label, val in verification_rows(v):
        A('<tr><th>%s</th><td>%s</td></tr>' % (e(label), e(str(val))))
    A('</table></div>')
    if blocked:
        A('<p class="sub">Karar için: '
          '<code>python3 04_BUILD/qa_verification.py --gate release '
          '--live</code> — üçü de yeşil olmadan <code>release</code> '
          'kapısı <b>KIRMIZIDIR</b>.</p>')

    # ── KURUCU İŞİ ─────────────────────────────────────────────────────
    A('<h2 id="kurucu">🟢 Yalnızca sizin yapabileceğiniz işler</h2>')
    A('<p class="sub">Ajan bunları yapmadı, yapamaz ve yaptığını '
      'söylemeyecek.</p><div class="scroll"><table>')
    for what, why in FOUNDER_ONLY:
        A('<tr><th>%s</th><td>%s</td></tr>' % (e(what), e(why)))
    A('</table></div>')

    # ── ADIMLAR ────────────────────────────────────────────────────────
    for code, name, icon, items in secs:
        A('<h2 id="%s">%s %s · %s</h2>' % (code.lower(), icon, code, e(name)))
        for it in items:
            A('<div class="card"><div class="hd">'
              '<input type="checkbox" id="%s">'
              '<h3><label for="%s">%s %s</label></h3>'
              '<span style="margin-left:auto">%s</span></div>'
              % (it["id"], it["id"], it["flag"], e(it["adim"]),
                 pill(it["state"])))
            A('<div class="scroll"><table>')
            for th, td in (("Ne yapacağım", it["ne"]),
                           ("KDP panelinde nereye gideceğim", it["nere"]),
                           ("Ne gireceğim", it["gir"]),
                           ("Hangi dosyayı seçeceğim", it["dosya"]),
                           ("Neleri kontrol edeceğim", it["kontrol"]),
                           ("Başarılı olursa ne göreceğim", it["basari"])):
                A('<tr><th>%s</th><td>%s</td></tr>' % (th, e(td)))
            A('</table></div></div>')

    # ── ALANLAR ────────────────────────────────────────────────────────
    A('<h2 id="alan">Panele girilecek alanlar</h2>')
    A('<p class="sub">Her satır kopyalanabilir. Boş alanlar '
      '<b>boş gösterilir</b> — yer tutucu basmak geri alınamaz.</p>')
    A('<div class="scroll"><table>')
    for i, (k, v) in enumerate(copy_fields(meta)):
        vid = "f%d" % i
        A('<tr><th>%s<button class="c" data-t="%s">kopyala</button></th>'
          '<td><span class="val" id="%s">%s</span></td></tr>'
          % (e(k), vid, vid, e(v)))
    A('</table></div>')

    # ── A+ METNİ ───────────────────────────────────────────────────────
    A('<h2 id="aplus">A+ metni — İngilizce</h2>')
    A('<div class="note"><b>Görsellerde metin YOKTUR.</b> Aşağıdaki '
      'başlık ve gövde Amazon\'un <b>kendi</b> alanlarına girilir; '
      'görsele çizilmez. Ürün sayfası İngilizcedir, bu yüzden bu metin '
      'de İngilizcedir.</div>')
    A('<div class="scroll"><table>')
    for m in CAT.APLUS:
        t, b = CAT.APLUS_COPY[m["id"]]
        A('<tr><th><code>%s</code><br>%s<br>'
          '<button class="c" data-t="%s-t">başlık</button>'
          '<button class="c" data-t="%s-b">gövde</button></th>'
          '<td><b class="val" id="%s-t">%s</b><br><br>'
          '<span class="val" id="%s-b">%s</span></td></tr>'
          % (e(m["id"]), e(m["name"]), m["id"], m["id"],
             m["id"], e(t), m["id"], e(b)))
    A('</table></div>')

    # ── KINDLE ALICI BİLGİLENDİRMESİ ───────────────────────────────────
    try:
        import kindle as KN
        A('<h2 id="kindlenote">Kindle alıcı bilgilendirmesi</h2>')
        A('<div class="note"><b>Bu metin ürün açıklamasının sonuna '
          'eklenir.</b> Özür değildir: ne aldığını söyler, olmayan bir '
          'şey vaat etmez ve satın almaktan caydırmaz.</div>')
        A('<div class="scroll"><table><tr>'
          '<th>Kindle notu<button class="c" data-t="knote">kopyala</button>'
          '</th><td><span class="val" id="knote">%s</span></td></tr>'
          '</table></div>' % e(KN.KINDLE_NOTE_EN))
    except Exception:                                          # noqa: BLE001
        pass

    # ── SON KONTROL LİSTESİ ────────────────────────────────────────────
    A('<h2 id="liste">Son önizleme kontrol listesi</h2>')
    checks = [
        ("PAPERBACK", ["iç blok yüklendi", "kapak yüklendi",
                       "gutter payı sayfa sayısına uygun",
                       "bleed doğru", "sayfa sayısı KDP ile aynı"]),
        ("HARDCOVER", ["iç blok yüklendi (264 s · iç pay 0,625 in)",
                       "kapak yüklendi (14,359 × 10,417 in)",
                       "sırt 0,7833 in doğru", "menteşe 0,394 in doğru",
                       "sarma (wrap) 0,591 in doğru"]),
        ("KINDLE", ["EPUB yüklendi", "kapak YALNIZCA ÖN (sırt/barkod yok)",
                    "⭑ %35 telif planı seçildi (46 MB dosya)",
                    "önizleyicide levhalar yakınlaşıyor",
                    "alıcı bilgilendirmesi açıklamaya eklendi"]),
        ("A+", ["6 görsel yüklendi", "başlıklar girildi",
                "gövde metni girildi", "önizleme kontrol edildi",
                "moderasyona gönderildi"]),
        ("LEVHA", ["103 levha Previewer'da tek tek görüldü",
                   "hiçbir levhada kırpma yok",
                   "sayılabilir işaretler sayılabiliyor",
                   "fiziksel provada ölçüldü (A9)"]),
    ]
    for grp, items in checks:
        A('<div class="card"><h3>%s</h3><div>' % grp)
        for j, c in enumerate(items):
            cid = "chk-%s-%d" % (grp.lower(), j)
            A('<div class="hd" style="margin-top:7px">'
              '<input type="checkbox" id="%s">'
              '<label for="%s">%s</label></div>' % (cid, cid, e(c)))
        A('</div></div>')

    A('<footer>Codex Enigmatica · bu kılavuz ölçümden üretildi · '
      'hiçbir satırı bir insanın yaptığı işi üstlenmez.</footer>')
    A('</div><script>%s</script>' % JS)
    return "\n".join(P)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    print("=" * 74)
    print("  KDP YÜKLEME EL KİTABI")
    print("=" * 74)

    rep = pl.Report(args.verbose)
    if not os.path.isfile(META):
        rep.check(False, "metadata.json yok — `04_BUILD/metadata.py` koştur")
        return rep.finish("metadata yok", None)

    meta = json.load(open(META, encoding="utf-8"))
    files = collect(meta)
    secs = steps(meta, files)

    md = render_md(meta, files, secs)
    doc = render_html(meta, files, secs)

    if args.check:
        stale = []
        for path, body in ((OUT_MD, md), (OUT_HTML, doc)):
            cur = (open(path, encoding="utf-8").read()
                   if os.path.exists(path) else None)
            if cur != body:
                stale.append(os.path.relpath(path, pl.ROOT))
        rep.check(not stale, "⭑ EL KİTABI ÜRETEÇLE AYNI ⭑"
                  + ("" if not stale else " — ⛔ BAYAT: %s" % stale))
    else:
        os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
        open(OUT_MD, "w", encoding="utf-8").write(md)
        open(OUT_HTML, "w", encoding="utf-8").write(doc)
        print("\n  ✍ %s" % os.path.relpath(OUT_MD, pl.ROOT))
        print("  ✍ %s" % os.path.relpath(OUT_HTML, pl.ROOT))

    # ── DENETİMLER ─────────────────────────────────────────────────────
    ids = [x["id"] for s in secs for x in s[3]]
    rep.check(len(ids) == len(set(ids)), "her adım kimliği tekil")
    rep.check(len(secs) == 7, "yedi bölüm var: A–G (%d)" % len(secs))

    need = ("adim", "ne", "nere", "gir", "dosya", "kontrol", "basari")
    miss = [x["id"] for s in secs for x in s[3]
            if any(not str(x.get(k) or "").strip() for k in need)]
    rep.check(not miss, "⭑ HER ADIM YEDİ BAŞLIĞI DA TAŞIYOR ⭑"
              + ("" if not miss else " — ⛔ %s" % miss[:5]))

    # ⚠ EN KRİTİK DENETİM: el kitabı olmayan bir dosyayı hazır göstermesin.
    lying = [k for k, v in files.items()
             if v["state"] == READY and v["n"] < v["need"]]
    rep.check(not lying, "⭑ HİÇBİR DOSYA OLMADIĞI HÂLDE HAZIR "
              "GÖSTERİLMİYOR ⭑" + ("" if not lying else " — ⛔ %s" % lying))

    # ⚠ § 33: ürün sayfasına giden metin İngilizce olmalıdır.
    import re as _re
    tr = [k for k, (t, b) in CAT.APLUS_COPY.items()
          if _re.search(r"[çğıöşüÇĞİÖŞÜ]", t + b)]
    rep.check(not tr, "⭑ A+ TİCARİ METNİ TÜRKÇE KARAKTER TAŞIMIYOR ⭑ "
              "(ürün sayfası İngilizcedir)"
              + ("" if not tr else " — ⛔ %s" % tr))
    rep.check(set(CAT.APLUS_COPY) == {m["id"] for m in CAT.APLUS},
              "her A+ modülünün ticari metni var")

    rep.check("localStorage" in doc and "checkbox" in doc,
              "kutucuk durumu localStorage ile korunuyor")
    rep.check("http://" not in doc and "https://" not in doc,
              "⭑ ÇEVRİMDIŞI ÇALIŞIR ⭑ (dış bağ yok)")
    nb = len(_re.findall(r'button class="c"', doc))
    rep.check(nb >= 20, "yeterli kopya düğmesi var (%d)" % nb)

    # ── ⭑ ÜRETİLEN HTML YAPISAL OLARAK DENETLENİR ⭑ ────────────────────
    # ⚠ Bir kılavuz ÇALIŞMAZSA yoktur: hedefi olmayan bir kopya düğmesi
    # ya da etiketi bağlanmamış bir kutucuk, kurucunun yanlış değeri
    # panele yapıştırması demektir.
    hids = _re.findall(r'\bid="([^"]+)"', doc)
    dupe = sorted({i for i in hids if hids.count(i) > 1})
    rep.check(not dupe, "hiçbir HTML kimliği iki kez kullanılmıyor"
              + ("" if not dupe else " — ⛔ %s" % dupe[:5]))

    tgt = _re.findall(r'data-t="([^"]+)"', doc)
    orphan = sorted({t for t in tgt if t not in hids})
    rep.check(not orphan, "⭑ HER KOPYA DÜĞMESİNİN HEDEFİ VAR ⭑"
              + ("" if not orphan else " — ⛔ %s" % orphan[:5]))

    cbs = _re.findall(r'<input type="checkbox" id="([^"]+)">', doc)
    labs = set(_re.findall(r'<label for="([^"]+)"', doc))
    nolab = sorted(set(cbs) - labs)
    rep.check(not nolab, "her kutucuğun tıklanabilir etiketi var"
              + ("" if not nolab else " — ⛔ %s" % nolab[:5]))
    rep.check(len(cbs) >= 25, "yeterli kutucuk var (%d)" % len(cbs))

    anc = _re.findall(r'href="#([^"]+)"', doc)
    brk = sorted({a for a in anc if a not in hids})
    rep.check(not brk, "her gezinme çıpası çözülüyor"
              + ("" if not brk else " — ⛔ %s" % brk))

    for tag in ("table", "div", "details", "script", "style"):
        o = len(_re.findall(r"<%s[ >]" % tag, doc))
        c = len(_re.findall(r"</%s>" % tag, doc))
        rep.check(o == c, "<%s> dengeli (%d/%d)" % (tag, o, c))

    sec = _re.findall(r"(?i)(api[_-]?key|CANARY_SALT|password|secret)", doc)
    rep.check(not sec, "⭑ SIR SIZINTISI YOK ⭑"
              + ("" if not sec else " — ⛔ %s" % sorted(set(sec))))

    rep.facts.update({"pageCount": meta["pageCount"],
                      "steps": len(ids), "copyButtons": nb,
                      "files": {k: v["state"] for k, v in files.items()}})
    return rep.finish("%d adım · %d kopya düğmesi" % (len(ids), nb), None)


if __name__ == "__main__":
    sys.exit(main())
