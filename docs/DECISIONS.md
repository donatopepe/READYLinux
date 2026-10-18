# Decision log

## D001 — Preservare READY 0.3

La base ZIP resta preservata; nuova funzionalità va aggiunta incrementando, senza sostituire l'app funzionante.

## D002 — BASIC separato dal runtime Python

Il requisito richiede BASIC reale, ma READY 0.3 è Python numerato. L'interprete BASIC sarà modulo autonomo, per evitare semantiche ambigue o regressioni; integrazione console successiva a test.

## D003 — Nessuna pretesa di sandbox

Verifica statica/esecuzione esplicita attuali non equivalgono a isolamento. Non eseguire automaticamente output AI.

## D005 — BASIC in modalità esplicita

BASIC si attiva con `BASIC`; righe numerate Python legacy restano nella modalità READY predefinita. Questo evita ambiguità tra linguaggi e regressioni.

## D004 — Niente tuning kernel senza misure

Non aggiungere patch CachyOS o profili performance finché release kernel/target non siano scelti e benchmark baseline disponibili.
