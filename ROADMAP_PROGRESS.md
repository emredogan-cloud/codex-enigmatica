# ROADMAP PROGRESS — Codex Enigmatica

<!-- Faz 1'den itibaren 04_BUILD/update_docs.py tarafından ÜRETİLİR -->

> Kapı: `phase0` · Son güncelleme: **12 Ağustos 2026**
>
> Bu dosya şu an **elle yazılmış bootstrap iskeletidir**. Faz 1'de
> `update_docs.py` devreye girer ve buradaki her sayı **ölçülmüş** olur.

---

## Faz durumu

| Faz | Ad | Durum | Kapı | Dal | Etiket |
|---|---|---|---|---|---|
| **0** | Bootstrap | ✅ **TAMAM** | `phase0` | `main` | — |
| **1** | Bulmaca mimarisi, çözülebilirlik, gizlilik | ⏸ **BAŞLAMADI** | `phase1` | `faz/1-mimari` | v0.1.0 |
| **2** | ⛔ **ÖLDÜRME KAPISI** — 20 bulmaca + 5 çözücü | ⏸ beklemede | `phase2` | `faz/2-pilot` | v0.2.0 |
| **3** | Kapı II · The Menagerie | ⏸ beklemede | `phase3` | `faz/3-kapi-2` | v0.3.0 |
| **4** | Kapı III–V + meta-mister | ⏸ beklemede | `phase4` | `faz/4-kapi-3-5` | v0.4.0 |
| **5** | Yakınsama + levha + doğrulama sayfası | ⏸ beklemede | `phase5` | `faz/5-yakinsama` | v0.5.0 |
| **6** | Nihai üretim + KDP paketi | ⏸ beklemede | `release` | `faz/6-uretim` | v1.0.0 |

---

## Faz 0 · Bootstrap — tamamlanan

- [x] Dizin yapısı (24 dizin)
- [x] `project_config.json` — tek doğruluk kaynağı
- [x] Altı fazlık uygulama yol haritası
- [x] `PROJECT_CONTEXT.md` · `BRIEF.md` · `DECISIONS.md` · `CHANGELOG.md`
- [x] `00_CONTEXT/`: STYLE · **SOLVABILITY_STANDARD** · **CONTENT_PROTECTION** · **HINT_LADDER** · LESSONS_FROM_CODEX
- [x] `01_SOURCE/puzzle.schema.json` — **iki katmanlı** veri şeması
- [x] Test altyapısı: `validate_spec.py` (public katmanda çözüm taraması dahil) ·
      `validate_structure.py` (**dört hatlı çözüm koruması**) · `selftest.py`
- [x] `04_BUILD/qa_all.sh` — CI'ın birebir aynısı
- [x] `.github/workflows/validate.yml` — CI iskeleti
- [x] `.gitignore` + **dört hatlı çözüm koruması**
- [x] `.gate` = `phase0`
- [x] Git deposu ve `main` dalı

---

## Ölçülen ilerleme

| | Ölçülen | Hedef |
|---|---:|---:|
| Aday bulmaca | **0** | ≥130 |
| Doğrulanmış bulmaca | **0** | 100 |
| Yazılmış bulmaca | **0** | 100 |
| Onaylanmış alternatif çözüm | **0** | **0** |
| İpucu (3×100) | **0** | 300 |
| Levha | **0** | ~110 |
| Kelime | **0** | ~34.000 |

---

## Sonraki izinli eylem

> ⛔ **FAZ 1 BAŞLAMADI ve kurucu onayı olmadan başlamaz.**
>
> Onay geldiğinde ilk üç iş:
> 1. `faz/1-mimari` dalını aç
> 2. **Gizlilik katmanını ilk gün kur** — bir çözümü yanlışlıkla public
>    katmana yazmak, git geçmişinden silinmesi gereken bir olaydır
> 3. A1 (çözüm katmanı politikası) kararını kapat
> 4. Bağımlılık grafiğini (DAG) erken kur — Kapı IV'te düzeltmek
>    60 bulmacayı yeniden sıralamak demektir
