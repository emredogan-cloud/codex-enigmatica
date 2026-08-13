#!/usr/bin/env bash
# =============================================================================
# CODEX ENIGMATICA — BÜTÜN KALİTE KAPILARI
# =============================================================================
# CI'ın çalıştırdığı komutların BİREBİR AYNISI. Push etmeden önce yerelde
# koşturun; yeşilse CI de yeşil olur.
#
#   ./04_BUILD/qa_all.sh              mevcut kapı seviyesiyle (.gate)
#   ./04_BUILD/qa_all.sh phase1       kapıyı yükselterek dene
#   ./04_BUILD/qa_all.sh --fix        üretilen belgeleri tazeleyerek
#
# Hafif kapıların hiçbiri venv gerektirmez; hepsi Python standart
# kütüphanesiyle koşar. Görsel/dizgi işleri Pillow ve reportlab ister ve
# yoksa ATLANIR (çıkış 2) — bu bir kalite düşüşü DEĞİLDİR.
# =============================================================================
set -uo pipefail

BUILD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$BUILD")"
TESTS="$ROOT/05_TESTS"
cd "$ROOT"

GATE=""
FIX=0
for arg in "$@"; do
  case "$arg" in
    --fix) FIX=1 ;;
    phase0|phase1|phase2|phase3|phase4|phase5|release) GATE="$arg" ;;
    *) echo "bilinmeyen argüman: $arg" >&2; exit 2 ;;
  esac
done

# Kapı seviyesi .gate dosyasındadır; yalnızca AÇIKÇA verilirse o kazanır.
# (Bestiarium'da --fix kapıyı draft'a düşürüyordu — yani belgeleri tazeleyen
# koşu açılmış kapıları HİÇ denetlemiyordu.)
if [ -z "$GATE" ]; then
  GATE="$( [ -f .gate ] && tr -d '[:space:]' < .gate || echo phase0 )"
fi

PY="${PYTHON:-python3}"
VENV_PY="$PY"
[ -x "$BUILD/.venv/bin/python" ] && VENV_PY="$BUILD/.venv/bin/python"

FAILED=()
SKIPPED=()

run () {
  local name="$1"; shift
  echo
  echo "──────────────────────────────────────────────────────────────────────"
  echo "▸ $name"
  echo "──────────────────────────────────────────────────────────────────────"
  if "$@"; then return 0; else FAILED+=("$name"); return 1; fi
}

run_optional () {
  local name="$1"; shift
  echo
  echo "──────────────────────────────────────────────────────────────────────"
  echo "▸ $name"
  echo "──────────────────────────────────────────────────────────────────────"
  "$@"
  case $? in
    0) ;;
    2) echo "ATLANDI: bağımlılık yok — pip install -r 04_BUILD/requirements.txt"
       SKIPPED+=("$name") ;;
    *) FAILED+=("$name") ;;
  esac
}

echo "════════════════════════════════════════════════════════════════════════"
echo "  CODEX ENIGMATICA · KALİTE KAPILARI · kapı: $GATE"
echo "════════════════════════════════════════════════════════════════════════"

if [ "$FIX" = "1" ]; then
  echo "▸ üretilen belgeler tazeleniyor…"
  [ -f 04_BUILD/update_docs.py ] && $PY 04_BUILD/update_docs.py >/dev/null || true
fi

# ── YAPILANDIRMA VE VERİ ────────────────────────────────────────────────────
run "veri bütünlüğü ve kapsam"  $PY 04_BUILD/validate_spec.py --gate "$GATE" \
                                   --json 06_REPORTS/tracked/spec-validation.json
run "depo ve belge bütünlüğü"   $PY 04_BUILD/validate_structure.py \
                                   --json 06_REPORTS/tracked/structure.json

# ── KAPILARIN KENDİ TESTİ — en önemlisi ────────────────────────────────────
run "KAPILARIN KENDİ TESTİ"     $PY 05_TESTS/selftest.py

# ── FAZ 1'DE DOĞACAK KAPILAR ───────────────────────────────────────────────
# Bu betikler henüz yok. Var olduklarında bu satırlar canlanır.
# Bir kapının VARLIĞI yetmez, KOŞMASI gerekir (World Myths K18).
[ -f 04_BUILD/validate_research.py ] && \
  run "araştırma kayıtları"     $PY 04_BUILD/validate_research.py --gate "$GATE" \
                                   --json 06_REPORTS/research.json
[ -f 04_BUILD/qa_dependency.py ] && \
  run "BAĞIMLILIK GRAFİĞİ (DAG)" $PY 04_BUILD/qa_dependency.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-dependency.json
[ -f 04_BUILD/qa_taxonomy.py ] && \
  run "MEKANİZMA ÇEŞİTLİLİĞİ"    $PY 04_BUILD/qa_taxonomy.py \
                                   --json 06_REPORTS/qa-taxonomy.json
# ⭑ Kanarya: alan adı değil CEVABIN KENDİSİ aranır. Faz 2'den itibaren
# koşmaması KIRMIZIDIR (sessizce yeşil yanan bir kanarya kanarya değildir).
[ -f 04_BUILD/qa_solution_leak.py ] && \
  run "⭑ ÇÖZÜM KANARYASI ⭑"      $PY 04_BUILD/qa_solution_leak.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-solution-leak.json

# ── FAZ 2'DE DOĞACAK KAPILAR ───────────────────────────────────────────────
# ⭑ CEVAP UZAYI önce koşar: tekillik ispatının TABANIDIR. Alternatif çözüm
# analizi (qa_uniqueness) yazarın YAZDIĞINI denetler; cevap uzayı yazarın
# YAZMADIĞINI arar. İkincisi başarısızsa birincisinin yeşili anlamsızdır.
[ -f 04_BUILD/qa_answerspace.py ] && \
  run "⭑ CEVAP UZAYI ⭑"          $PY 04_BUILD/qa_answerspace.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-answerspace.json
[ -f 04_BUILD/qa_handoff.py ] && \
  run "DEVİR VE HATA DAVRANIŞI"  $PY 04_BUILD/qa_handoff.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-handoff.json
[ -f 04_BUILD/qa_solvability.py ] && \
  run "ÇÖZÜLEBİLİRLİK"          $PY 04_BUILD/qa_solvability.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-solvability.json
[ -f 04_BUILD/qa_uniqueness.py ] && \
  run "ALTERNATİF ÇÖZÜM"        $PY 04_BUILD/qa_uniqueness.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-uniqueness.json
[ -f 04_BUILD/qa_hints.py ] && \
  run "ipucu bütünlüğü"         $PY 04_BUILD/qa_hints.py --gate "$GATE" \
                                   --json 06_REPORTS/qa-hints.json
[ -f 04_BUILD/qa_length.py ] && \
  run "kelime bandı"            $PY 04_BUILD/qa_length.py \
                                   --json 06_REPORTS/qa-length.json
[ -f 04_BUILD/qa_voice.py ] && \
  run "ses ve yasak kalıp"      $PY 04_BUILD/qa_voice.py \
                                   --json 06_REPORTS/qa-voice.json
[ -f 04_BUILD/qa_echo.py ] && \
  run "tekrar taraması"         $PY 04_BUILD/qa_echo.py \
                                   --json 06_REPORTS/qa-echo.json
[ -f 04_BUILD/qa_drift.py ] && \
  run "üslup sürüklenmesi"      $PY 04_BUILD/qa_drift.py \
                                   --json 06_REPORTS/qa-drift.json

# ── FAZ 3+ KAPILARI ────────────────────────────────────────────────────────
[ -f 04_BUILD/qa_crossref.py ] && \
  run "çapraz referans"         $PY 04_BUILD/qa_crossref.py \
                                   --json 06_REPORTS/qa-crossref.json
[ -f 04_BUILD/qa_meta.py ] && \
  run "meta-mister bütünlüğü"   $PY 04_BUILD/qa_meta.py \
                                   --json 06_REPORTS/qa-meta.json
[ -f 04_BUILD/qa_plate_readability.py ] && \
  run_optional "levha okunabilirliği" $VENV_PY 04_BUILD/qa_plate_readability.py --check

# ── ÜRETİM MODELİ ──────────────────────────────────────────────────────────
[ -f 04_BUILD/page_budget.py ] && \
  run "sayfa bütçesi"           $PY 04_BUILD/page_budget.py \
                                   --json 06_REPORTS/page-budget.json
[ -f 04_BUILD/editions.py ] && \
  run "sürüm ve telif modeli"   $PY 04_BUILD/editions.py \
                                   --json 06_REPORTS/editions.json

# ── GÖRSEL VE ÜRETİM HATTI (Pillow / reportlab ister) ──────────────────────
[ -f 04_BUILD/asset_inventory.py ] && \
  run_optional "ham varlık envanteri"   $VENV_PY 04_BUILD/asset_inventory.py --check
[ -f 04_BUILD/interior.py ] && \
  run_optional "iç blok güncel"         $VENV_PY 04_BUILD/interior.py --check
[ -f 04_BUILD/epub.py ] && \
  run_optional "Kindle EPUB güncel"     $VENV_PY 04_BUILD/epub.py --check
[ -f 04_BUILD/covers.py ] && \
  run_optional "kapak üretimi güncel"   $VENV_PY 04_BUILD/covers.py --check
[ -f 04_BUILD/metadata.py ] && \
  run "KDP metadata paketi"     $PY 04_BUILD/metadata.py --check

# ── ÜRETİLEN BELGELER BAYAT MI ─────────────────────────────────────────────
[ -f 04_BUILD/update_docs.py ] && \
  run "üretilen belgeler güncel" $PY 04_BUILD/update_docs.py --check

# ── ÖZET ───────────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════════════"
if [ ${#SKIPPED[@]} -gt 0 ]; then
  echo "  ⊘ ${#SKIPPED[@]} kapı atlandı (bağımlılık yok):"
  for s in "${SKIPPED[@]}"; do echo "     · $s"; done
fi
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "  ✅ BÜTÜN KAPILAR YEŞİL · kapı seviyesi: $GATE"
  echo "════════════════════════════════════════════════════════════════════════"
  exit 0
fi
echo "  ⛔ ${#FAILED[@]} KAPI KIRMIZI"
for f in "${FAILED[@]}"; do echo "     · $f"; done
echo "════════════════════════════════════════════════════════════════════════"
echo
echo "  Kalite düştü. Düzeltilmeden ilerleme yok."
exit 1
