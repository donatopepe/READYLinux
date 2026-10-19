# Roadmap verificabile

## M0 — Baseline (documentata)

Accettazione: struttura e limiti descritti; comandi di test riproducibili.

## M1 — Classic console e BASIC

Accettazione: parser/runtime effettivo; numeri di riga, variabili, espressioni, IF, loop, input/output, subroutine e file; test deterministici; READY e Python legacy non regressi. Implementazione ridotta presente, con test; compatibilità Commodore completa non dichiarata.

## M2 — Build OS minimo

Scaffolding iniziale `meta-readylinux` aggiunto (layer config, distro, image, runtime recipe, servizio systemd tty1 e test statici). BitBake parse/build e boot QEMU non verificati. WSL Debian 13 preflight osservato: 19/19 comandi host richiesti OK, QEMU disponibile, ma BitBake/bitbake-layers assenti e BUILDDIR non inizializzato (vedi [verification plan](VERIFICATION_PLAN.md)). Accettazione restante: release/MACHINE pin, parse, build x86-64 e boot QEMU su host OE provisionato. Niente ottimizzazioni kernel senza benchmark.

## M3 — READY Stable

Kernel/BSP compatibile e profilo stabile; boot, storage, input, servizi e recovery verificati.

## M4 — Performance e low-latency

Una variabile per esperimento; build identica e benchmark riproducibili, P95/P99 e regressioni documentate. Patch esterne solo con provenienza, licenza e compatibilità.

## M5 — Inferenza CPU reale

llama.cpp e modello importato esplicitamente; inferenza offline su CPU; consumo RAM, latenza e interruzione misurati. Modello selezionabile/catalogo e acquisto hardware richiedono provenance/versione/licenza/checksum, procedure offline e test negativi; see [`AI_HARDWARE.md`](AI_HARDWARE.md). La guida acquisto corrente è stima, non ricerca web o benchmark verificato. Web research hardware richiesta dall'utente: pending; non avviata qui perché non disponibile uno strumento web e le regole repo vietano l'avvio di attività di rete.

## M6 — Coding agent sicuro

Modifiche multi-file, diff/approvazione, test in isolamento reale, limiti CPU/RAM/filesystem/rete, rollback e test negativi.

## M7 — Workbench/AI Studio

Prototipo UI separato dal motore; responsività sotto inferenza; scelta tecnologia supportata da misure.

## M8 — GPU e ARM64

Solo backend e target disponibili; fallback CPU, QEMU ARM64 o BSP specifico verificati.

## M9 — Release

Immagini, manifest SBOM/licenze, installazione/recovery e matrice completa dei test.

## Gate per chiudere gap di verifica

I limiti attuali hanno dipendenze esplicite (host OE/BitBake, immagine, kernel, SSH guest, modello e isolamento). Usare [piano gated di verifica](VERIFICATION_PLAN.md) per prerequisites, comandi, evidenze accettabili e scope no-download; fake tool non chiudono gate runtime.
