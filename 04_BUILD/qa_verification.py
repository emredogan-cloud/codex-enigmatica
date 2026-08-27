#!/usr/bin/env python3
"""
DOĞRULAMA SAYFASI KAPISI — kitabın vaat ettiği adres GERÇEK Mİ
================================================================================
⭑ NEDEN BU KAPI VAR ⭑

Sözleşme sayfası okura ADIYLA bir söz verir:

    "You enter it on the VERIFICATION PAGE, whose address is printed on
     the last leaf of this book."

Ve kapanış şunu der: *"When you have it, you know where to write it."*

Faz 5 sonunda bu sözün karşılığı YOKTU: hiçbir yaprakta adres basılı
değildi, ve `verificationPending` — **kurucuya ait açık bir iş kaydı** —
bir ara yapıda okura doğrulama adresi diye basılmıştı. Yani kitap ilk
sayfalarında verdiği sözü son sayfalarında bozuyordu.

⚠ VE BASILI BİR URL GERİ ALINAMAZ. Bu, bu depodaki en pahalı tek dizedir:

  · alan adı kayıtlı değilse — başkası kaydeder ve satılmış her nüsha
    okuru YABANCI bir siteye gönderir
  · süresi dolarsa — aynı şey, ama sessizce
  · yol değişirse — kitap 404'e işaret eder ve düzeltilemez

Bu yüzden kapı üç ayrı şeyi ayrı ayrı ölçer ve **hiçbirini diğerinin
yerine saymaz**:

    printedUrl        BASILAN dize   → yer tutucu olamaz, biçimi geçerli
    domainRegistered  alan adı BİZDE mi (kurucu · ödeme işlemi)
    liveVerifiedAt    adres GERÇEKTEN yanıt verdi mi, ne zaman

⭑ KAPI SEVİYESİNE GÖRE SERTLEŞİR ⭑
  phase0–phase5   adres yoksa UYARI (henüz kurucu kararı)
  release         adres yok / kayıtlı değil / hiç doğrulanmamış → ⛔ KIRMIZI

Gerekçe: `release` "BASKIYA GİDİYOR" demektir. Kayıtlı olmayan bir alan
adına işaret eden bir kitabı basmak, kapının önlemek için var olduğu tek
şeydir.

⭑ VE BİR ŞEYİ DAHA ÖLÇER: SÖZ İLE MEKANİZMANIN ÖRTÜŞMESİ ⭑

Sayfa YALNIZCA son sorunun cevabını doğrular (`scope: final-answer-only`).
Kitap bundan FAZLASINI vaat ederse — örneğin her bulmacayı sayfanın
hakem edeceğini — söz karşılıksızdır. `FORBIDDEN_PROMISES` o cümleleri
basılı metinde arar.

⚠ 101 CEVAP ALANI NEDEN YOK (A7'nin 'evet' dalı): cevap uzayının tamamı
5.086 aday dizedir. 101 cevabı kabul eden bir kâhin, kitabı hiç almamış
birine ~5.086 istekle ÇÖZÜM KİTABININ TAMAMINI verir. Bir bulmaca
kitabının çözümleri ürünün kendisidir (PROJECT_CONTEXT § 5·②).

Çıkış kodları:  0 = temiz   1 = kapı kırmızı
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _protected_layer as pl                                  # noqa: E402

OUT = os.path.join(pl.ROOT, "08_OUTPUT")
STATS = os.path.join(pl.ROOT, "06_REPORTS", "tracked", "qa-verification.json")

# ⚠ YER TUTUCU BASMAK, HİÇ BASMAMAKTAN KÖTÜDÜR: hiç basılmamış bir adres
# kitabı eksik bırakır; basılmış bir yer tutucu okura YANLIŞ yer söyler
# ve ikisi arasındaki fark geri alınamazdır.
PLACEHOLDER = re.compile(
    r"example\.(com|org|net)|localhost|127\.0\.0\.1|0\.0\.0\.0"
    r"|\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|yer\s*tutucu|placeholder"
    r"|your-?site|change-?me|kurucu|founder|\bA4\b|\bpending\b"
    r"|\.(test|invalid|example|local|localdomain)(/|$)"
    r"|\bvercel\.app\b",
    re.IGNORECASE)

# ⚠ VE BASILI METİN AYNI SÜZGEÇLE TARANAMAZ. Yukarıdaki desen ADRESE
# göre yazılmıştır ve "founder", "pending", "A4" gibi sözcükleri yasak
# sayar — İngilizce bir kitabın gövdesinde bunlar OLAĞAN sözcüklerdir ve
# kapıyı yanlış yere kırmızı yakarlardı. Basılı metinde yalnızca
# TARTIŞMASIZ yer tutucular aranır: URL biçimli olanlar ve bir kez
# gerçekten dizilmiş olan o tek dize.
PENDING_MARKER = "verification page address"
PLACEHOLDER_IN_PRINT = re.compile(
    r"example\.(com|org|net)|localhost|127\.0\.0\.1"
    r"|\bTODO\b|\bFIXME\b|your-?site|change-?me"
    r"|\bvercel\.app\b|verification\s+page\s+address",
    re.IGNORECASE)

# ⚠ `vercel.app` bilerek yasaktır: bir önizleme alan adı KİRACIDIR.
# Vercel projesi silinirse ya da ad değişirse adres ölür — ve kitap
# basılmıştır.

URL_SHAPE = re.compile(
    r"^(?:https?://)?"                       # şema isteğe bağlı (basılı biçim)
    r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,24}"
    r"(?:/[A-Za-z0-9\-._~/]*)?$")

# Sayfanın YAPMADIĞI şeyi vaat eden cümleler.
FORBIDDEN_PROMISES = [
    "the verification page will tell you which",
    "enter each answer on the verification page",
    "the verification page checks every answer",
    "the verification page will confirm each",
    "check every puzzle on the verification page",
]


def pdf_text(path: str) -> str:
    try:
        r = subprocess.run(["pdftotext", "-q", path, "-"],
                           capture_output=True, text=True, timeout=300)
        return r.stdout if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def epub_text(path: str) -> str:
    try:
        z = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile):
        return ""
    out = []
    for n in z.namelist():
        if n.endswith((".xhtml", ".html", ".opf")):
            out.append(re.sub(r"<[^>]+>", " ",
                              z.read(n).decode("utf-8", "ignore")))
    return "\n".join(out)


def flat(s: str) -> str:
    """Dizgi satır sonlarını ve boşlukları yok sayan karşılaştırma yüzeyi.

    ⚠ Basılı bir URL satır sonunda bölünebilir. `pdftotext` onu iki
    parçaya ayırır ve düz `in` araması BULAMAZ — kapı adres basılıyken
    "basılı değil" derdi. Bütün boşluklar atılarak aranır.
    """
    return re.sub(r"\s+", "", s or "").lower()


def check_live(url: str, timeout: float = 10.0) -> tuple[bool, str]:
    """⚠ AĞ İSTEĞE BAĞLIDIR — `--live` olmadan HİÇ yapılmaz.

    CI'da ağ yoktur ve alan adı henüz kayıtlı değildir; her koşuda
    kırmızı yanan bir denetim, kapıyı gürültüye boğar ve okunmaz hâle
    getirir. Canlılık AYRI bir sorudur ve ayrıca sorulur.
    """
    import urllib.error
    import urllib.request
    full = url if url.startswith("http") else "https://" + url
    req = urllib.request.Request(full, method="GET",
                                 headers={"User-Agent": "codex-enigmatica-qa"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return (200 <= r.status < 400), "HTTP %s" % r.status
    except urllib.error.HTTPError as e:
        return False, "HTTP %s" % e.code
    except Exception as e:                                # noqa: BLE001
        return False, type(e).__name__


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", default=None)
    ap.add_argument("--json", default=STATS)
    ap.add_argument("--live", action="store_true",
                    help="adresi GERÇEKTEN çağır (ağ ister)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    gate = args.gate or pl.read_gate()
    release = gate == "release"

    print("=" * 74)
    print("  DOĞRULAMA SAYFASI KAPISI · kapı: %s" % gate)
    print("=" * 74)

    rep = pl.Report(args.verbose)
    cfg = pl.load_config()
    ver = ((cfg.get("founder") or {}).get("verification")) or {}
    url = (ver.get("printedUrl") or "").strip()
    rep.facts["gate"] = gate

    # ── ① ADRESİN KENDİSİ ──────────────────────────────────────────────
    print("\n── basılan adres ──")
    if not url:
        msg = ("⭑ DOĞRULAMA ADRESİ SEÇİLMEMİŞ ⭑ (A4 · kurucu) — sözleşme "
               "sayfası bir adres VAAT EDİYOR")
        if release:
            rep.check(False, msg)
        else:
            rep.warn(msg + " · `release` kapısında KIRMIZI olacak")
        rep.facts["printedUrl"] = None
        return rep.finish("adres yok", args.json)

    rep.facts["printedUrl"] = url
    ph = PLACEHOLDER.search(url)
    rep.check(not ph, "adres bir YER TUTUCU DEĞİL"
              + ("" if not ph else " — ⛔ %r" % ph.group(0)))
    rep.check(bool(URL_SHAPE.match(url)),
              "adresin biçimi geçerli (%s)" % url)
    rep.check(url == url.strip() and " " not in url,
              "adres tek parça, boşluksuz")
    rep.check(url.lower() == url,
              "adres tamamen küçük harf — basılı bir URL'de "
              "büyük/küçük fark okurun hatasına dönüşür")
    # ⚠ Basılı adres ELLE YAZILIR. Uzunluk ve derinlik okurun hata
    # payıdır: her ek bölüm bir yazım hatası fırsatıdır.
    rep.check(len(url) <= 60,
              "adres elle yazılabilir uzunlukta (%d ≤ 60)" % len(url))
    rep.check(url.count("/") <= 3,
              "adres en fazla üç bölüm derinliğinde (%d)" % url.count("/"))

    # ── ② YOL, SİTE ROTASIYLA AYNI MI ──────────────────────────────────
    print("\n── site rotası ──")
    route = (ver.get("route") or "").strip()
    canonical = (ver.get("canonicalUrl") or "").strip()
    rep.check(bool(route) and route.startswith("/"),
              "site rotası tanımlı (%s)" % (route or "—"))
    if route:
        rep.check(url.endswith(route),
                  "basılan adres site rotasıyla BİTİYOR (%s)" % route)
    if canonical:
        rep.check(flat(canonical).endswith(flat(url)),
                  "canonicalUrl basılan adresle örtüşüyor")
        rep.check(canonical.startswith("https://"),
                  "canonicalUrl HTTPS")

    # ── ③ SÖZ İLE MEKANİZMA ────────────────────────────────────────────
    print("\n── söz ile mekanizma ──")
    scope = (ver.get("scope") or "").strip()
    rep.check(scope == "final-answer-only",
              "kapsam `final-answer-only` (%s) — 101 cevap alanı bir "
              "KÂHİNDİR ve çözüm kitabını dağıtır" % (scope or "—"))

    # ── ④ SIR MODELİ ───────────────────────────────────────────────────
    print("\n── sır modeli ──")
    rep.check((ver.get("secretModel") or "") == "peppered-sha256",
              "sunucu sırrı biberli SHA-256 (düz cevap saklanmıyor)")

    # ── ⑤ BASILI ÜRÜNDE GERÇEKTEN VAR MI ───────────────────────────────
    print("\n── basılı üründe ──")
    needle = flat(url)
    targets = [
        ("paperback iç blok", os.path.join(OUT, "PAPERBACK", "interior.pdf"),
         pdf_text),
        ("hardcover iç blok", os.path.join(OUT, "HARDCOVER", "interior.pdf"),
         pdf_text),
        ("Kindle EPUB",
         os.path.join(OUT, "KINDLE", "codex-enigmatica.epub"), epub_text),
    ]
    seen = {}
    for label, path, reader in targets:
        if not os.path.isfile(path):
            rep.warn("%s YOK — taranamadı" % label)
            continue
        text = reader(path)
        if not text.strip():
            rep.warn("%s metni çıkarılamadı" % label)
            continue
        low = flat(text)
        rep.check(needle in low, "⭑ %s ADRESİ TAŞIYOR ⭑" % label.upper())
        seen[label] = needle in low

        # ⚠ Yer tutucu okura BASILMAMALI. `verificationPending` bir kez
        # doğrulama adresi diye dizilmişti — kapı o kusurun tekrarını
        # mekanik olarak imkânsız kılar.
        leak = PLACEHOLDER_IN_PRINT.search(text)
        rep.check(leak is None, "%s YER TUTUCU BASMIYOR" % label
                  + ("" if leak is None else " — ⛔ %r" % leak.group(0)))

        # ⚠ Sayfanın yapmadığı şeyi vaat eden cümle.
        bad = [p for p in FORBIDDEN_PROMISES if flat(p) in low]
        rep.check(not bad, "%s KARŞILIKSIZ SÖZ VERMİYOR" % label
                  + ("" if not bad else " — ⛔ %s" % bad))
    rep.facts["printedIn"] = seen

    # ── ⑤b ⭑ GEÇİCİ VERCEL GEÇERSİZ KILMASI ⭑ ─────────────────────────
    # ⚠ BU BÖLÜM KALICI KURALI ZAYIFLATMAZ VE ZAYIFLATAMAZ.
    # Yukarıdaki ① hâlâ `printedUrl` içinde *.vercel.app görürse KIRMIZI
    # yanar ve o denetim buraya BAKMAZ. Burada ölçülen tek şey şudur:
    # geçici test hedefi, basım hedefinin YERİNE GEÇMİŞ Mİ?
    #
    # Gerekçe: bir kiracı alan adının kitaba sızmasının en olası yolu,
    # "geçici" diye açılan bir alanın sessizce basım alanına kopyalanması
    # olurdu. Kapı tam olarak onu arar.
    tmp = ver.get("temporary") or {}
    if tmp:
        print("\n── geçici Vercel geçersiz kılması ──")
        base = (tmp.get("temporaryVerificationBaseUrl") or "").strip()
        rep.facts["temporary"] = {
            "baseUrl": base,
            "printedInBook": bool(tmp.get("printedInBook")),
            "liveState": tmp.get("liveState") or {},
        }
        rep.check(tmp.get("overrideName") == "FOUNDER_TEMPORARY_VERCEL_OVERRIDE",
                  "geçersiz kılma ADIYLA kayıtlı")
        rep.check(bool(tmp.get("authorisedAt")),
                  "geçersiz kılmanın TARİHİ var (%s)" % (tmp.get("authorisedAt") or "—"))
        rep.check(bool(tmp.get("reason")), "geçersiz kılmanın GEREKÇESİ yazılı")
        rep.check(bool(tmp.get("removeWhen")),
                  "geçersiz kılmanın KALDIRMA KOŞULU yazılı")
        # ⭑ EN ÖNEMLİ ÜÇ DENETİM ⭑
        rep.check(tmp.get("printedInBook") is False,
                  "⭑ GEÇİCİ URL KİTABA BASILMIYOR ⭑ (printedInBook=false)")
        rep.check(flat(base) != flat(url) and flat(url) not in flat(base),
                  "⭑ GEÇİCİ HEDEF, BASIM HEDEFİNİN YERİNE GEÇMEMİŞ ⭑")
        rep.check("valicepress.com" in (tmp.get("permanenceRule") or "").lower(),
                  "kalıcılık kuralı KALICI alan adını adıyla anıyor")
        # Ve basılan adres HÂLÂ geçici olamaz — ① zaten bakıyor, ama bu
        # kapının en pahalı hatası olduğu için İKİ KEZ ölçülür.
        rep.check("vercel.app" not in url.lower(),
                  "⭑ BASILAN ADRES BİR ÖNİZLEME ALAN ADI DEĞİL ⭑ "
                  "(kiracı alan adı kitaba giremez)")

        live = tmp.get("liveState") or {}
        if live:
            print("\n── geçici dağıtımın ÖLÇÜLEN durumu ──")
            for lbl, key in (("sayfa canlı", "pageLive"),
                             ("HTTPS zorunlu", "httpsEnforced"),
                             ("GET 405", "getReturns405"),
                             ("istemci sızıntısı yok",
                              "failsClosedVerifiedLive")):
                print("  %-28s %s" % (lbl, "EVET" if live.get(key) else "HAYIR"))
            if not live.get("endpointOperational"):
                rep.warn("⚠ GEÇİCİ UÇ NOKTA ÇALIŞMIYOR — %s"
                         % (live.get("endpointBlockedBy") or "sebep yazılmamış"))
                print("     ⭑ ve bu KAPALI DÜŞME davranışıdır, bir kusur")
                print("       değil: sınırlayıcısız bir kâhin sınırsız")
                print("       denemedir. Kapı bunun için zayıflatılmadı.")

    # ── ⑥ ALAN ADI VE CANLILIK — KURUCUYA AİT ──────────────────────────
    print("\n── alan adı ve canlılık ──")
    registered = bool(ver.get("domainRegistered"))
    live_at = ver.get("liveVerifiedAt")
    deployed = bool(ver.get("deployed"))
    rep.facts.update({"domainRegistered": registered,
                      "deployed": deployed, "liveVerifiedAt": live_at})

    msg_reg = ("⭑ ALAN ADI KURUCUNUN ELİNDE ⭑ — kayıtlı değilken basmak, "
               "okuru başkasının sitesine göndermektir")
    msg_live = "⭑ ADRES CANLI OLARAK DOĞRULANDI ⭑ (liveVerifiedAt)"
    msg_dep = "⭑ SİTE YAYINDA ⭑ (deployed)"
    if release:
        rep.check(registered, msg_reg)
        rep.check(bool(live_at), msg_live)
        rep.check(deployed, msg_dep)
    else:
        for ok, m in ((registered, msg_reg), (bool(live_at), msg_live),
                      (deployed, msg_dep)):
            if ok:
                rep.check(True, m)
            else:
                rep.warn(m + " · HAYIR — `release` kapısında KIRMIZI olacak")

    # ── ⑦ İSTEĞE BAĞLI: GERÇEKTEN ÇAĞIR ────────────────────────────────
    if args.live:
        print("\n── canlı çağrı ──")
        ok, why = check_live(canonical or url)
        rep.facts["liveProbe"] = why
        rep.check(ok, "adres yanıt verdi (%s)" % why)
    else:
        print("\n  ⊘ canlı çağrı yapılmadı (--live ile açılır)")

    # ── ÖZET ───────────────────────────────────────────────────────────
    print("\n── özet ──")
    print("  %-28s %s" % ("basılan adres", url))
    print("  %-28s %s" % ("kapsam", scope or "—"))
    print("  %-28s %s" % ("alan adı kayıtlı", "EVET" if registered else "HAYIR"))
    print("  %-28s %s" % ("yayında", "EVET" if deployed else "HAYIR"))
    print("  %-28s %s" % ("canlı doğrulandı", live_at or "HİÇ"))
    if not (registered and deployed and live_at):
        print()
        print("  ⚠ BUNLAR KURUCUYA AİTTİR ve ajan yapamaz:")
        print("    · alan adı kaydı bir ÖDEME işlemidir")
        print("    · yayına alma kurucunun Vercel hesabındadır")
        print("    · üçü de tamamlanmadan `release` kapısı KIRMIZIDIR")

    return rep.finish("doğrulama adresi", args.json)


if __name__ == "__main__":
    sys.exit(main())
