# Roadmap verificabile

## M0 — Baseline (documentata)

Accettazione: struttura e limiti descritti; comandi di test riproducibili.

## M1 — Classic console e BASIC

Accettazione: parser/runtime effettivo; numeri di riga, variabili, espressioni, IF, loop, input/output, subroutine e file; test deterministici; READY e Python legacy non regressi. Stato: interprete autonomo `basic.py` con 9 test dedicati; integrazione console, persistenza e documentazione bilingue ancora incomplete. Suite attuale ha un test d'integrazione fallito; milestone NON chiusa.

## M2 — Build OS minimo

Spike Yocto su host Linux; layer meta-readylinux; immagine x86-64 avviabile QEMU; autostart console. Niente ottimizzazioni kernel senza benchmark.

## M3 — READY Stable

Kernel/BSP compatibile e profilo stabile; boot, storage, input, servizi e recovery verificati.

## M4 — Performance e low-latency

Una variabile per esperimento; build identica e benchmark riproducibili, P95/P99 e regressioni documentate. Patch esterne solo con provenienza, licenza e compatibilità.

## M5 — Inferenza CPU reale

llama.cpp e modello importato esplicitamente; inferenza offline su CPU; consumo RAM, latenza e interruzione misurati.

## M6 — Coding agent sicuro

Modifiche multi-file, diff/approvazione, test in isolamento reale, limiti CPU/RAM/filesystem/rete, rollback e test negativi.

## M7 — Workbench/AI Studio

Prototipo UI separato dal motore; responsività sotto inferenza; scelta tecnologia supportata da misure.

## M8 — GPU e ARM64

Solo backend e target disponibili; fallback CPU, QEMU ARM64 o BSP specifico verificati.

## M9 — Release

Immagini, manifest SBOM/licenze, installazione/recovery e matrice completa dei test.
