# ROADMAP PROGRESS — Codex Enigmatica

<!-- ⚠ ÜRETİLEN BELGE — 04_BUILD/update_docs.py. ELLE DÜZENLEMEYİN. -->

> Kapı: `phase4`

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
| **0** | Bootstrap | ✅ **TAMAM** | `phase0` | `main` | — |
| **1** | Bulmaca mimarisi, çözülebilirlik, gizlilik | ✅ **TAMAM** | `phase1` | `faz/1-mimari` | v0.1.0 |
| **2** | ⛔ **ÖLDÜRME KAPISI** — 20 bulmaca + 5 çözücü | ⚑ **KURUCU KARARIYLA** — doğrulama bekliyor | `phase2` | `faz/2-pilot` | v0.2.0 |
| **3** | Kapı II · The Menagerie | ⚑ **KURUCU KARARIYLA** — doğrulama bekliyor | `phase3` | `faz/3-kapi-2` | v0.3.0 |
| **4** | Kapı III–V + meta-mister | ⚑ **KURUCU KARARIYLA** — doğrulama bekliyor | `phase4` | `faz/4-kapi-3-5` | v0.4.0 |
| **5** | Yakınsama + levha + doğrulama sayfası | ⏸ **SIRADA** | `phase5` | `faz/5-yakinsama` | v0.5.0 |
| **6** | Nihai üretim + KDP paketi | ⏸ beklemede | `release` | `faz/6-uretim` | v1.0.0 |

> ## ⚠ EXTERNAL HUMAN VALIDATION REMAINS PENDING
>
> Ölçülen öldürme kapısı: ⛔ **HARD-STOP** (1/5) — **değişmedi**.
> Yapılan harici oturum: **0** · İnsan doğrulaması geçti mi: **HAYIR**
>
> Faz 2 ve sonrası **kurucu geçersiz kılmasıyla** ilerledi (`DECISIONS.md § A13`). Hiçbir faz *harici olarak doğrulanmış* değildir.

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday bulmaca | **151** | ≥130 |
| Mekanizma ailesi | **17** | ≥10 |
| Pilot kohort (Kapı I) | **20** | 20 |
| **Yazılmış taslak** | **101** | — |
| Doğrulanmış bulmaca | **0** | 100 |
| Yazılmış bulmaca (nihai) | **0** | 100 |
| Onaylanmış alternatif çözüm | **0** | **0** |
| İpucu (3 kademe) | **303** | 300 |
| Levha | **0** üretildi / 103 planlandı | ~110 |
| Kelime (ölçülen) | **17.551** | ~34.000 |
| Künye | **15** (0 doğrulanmış) | — |

---

## Sonraki izinli eylem

> ### ⛔ FAZ 4 · KAPI III–V + META — ÖLÇÜLEN KARAR: **HARD-STOP**
>
> Bu fazın ajan tarafından yapılabilir bütün işi **tamamlandı**: Kapı III, IV ve V yazıldı, meta-mister kuruldu ve `qa_meta.py` ile doğrulandı, dokuz yeni mekanizmanın ısınma örneği yazıldı, aha politikası ölçüye bağlandı (K36) ve sayfa modeli gerçek metinle yeniden ölçüldü.
>
> **Ama öldürme kapısı ölçemediği bir şeyi geçmiş sayamaz.**
> Harici çözücü oturumu: **0 / 5**.
>
> Kalan iş **kurucuya aittir** ve ajan onu yapamaz:
> 1. **A12b** — harici çözücü oturumlarını yürüt
>    → `00_CONTEXT/EXTERNAL_SOLVER_PACKAGE.md`
> 2. sonuçları `06_REPORTS/solver/` altına yaz, sayaçları güncelle
> 3. `./04_BUILD/qa_all.sh phase4` koştur ve kararı **oku**
>
> Ayrıca açık: **A9** (levha provası — paket hazır) · **A2** · **A4** ·
> **A5** · **A6** · **A7** · **A10**
>
> Ayrıntı: `DECISIONS.md § AÇIK KARARLAR`
