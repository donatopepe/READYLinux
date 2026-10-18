# CONTEXT.md — Passaggio dalla conversazione ChatGPT a Codex

## Scopo di questo documento
Riepilogo operativo delle scelte progettuali maturate nella chat relativa a Commodore, Linux e READY Linux. **Non è una trascrizione integrale della conversazione**. Le informazioni sullo stato del software vanno confermate ispezionando e testando il repository incluso.

## Origine e visione
- L'idea nasce dal confronto con Commodore 64 (programmazione immediatamente accessibile all'accensione) e con AmigaOS/Workbench (personalizzazione, leggerezza e forte integrazione tra applicazioni).
- Reinterpretazione moderna: computer che, una volta avviato, apre direttamente un ambiente orientato a creare software, senza richiedere all'utente di predisporre IDE e tool separati.
- Si **riutilizza il kernel Linux**: non bisogna scrivere un nuovo kernel. Il prodotto finale dovrà essere una distribuzione o immagine Linux avviabile autonomamente.
- L'utente ha richiesto poi un assistente IA completamente locale, fruibile anche su sola CPU, e infine di rendere l'esperienza **vibe-coding-centric**: l'utente descrive ciò che vuole, l'IA prepara modifiche verificabili e l'utente può approvarle.

## Requisiti di prodotto concordati
1. Avvio del sistema verso un ambiente READY che metta l'input in linguaggio naturale al centro dell'interazione, pur mantenendo accesso al codice, terminale ed editor.
2. Creazione/modifica di progetti tramite IA; generazione in file, anteprima diff, conferma prima della scrittura, verifica, iterazione e ripristino.
3. IA locale e offline **dopo l'installazione** del modello; funzionamento anche senza GPU. Non imporre account cloud, API a pagamento o connessioni remote.
4. CPU-only tramite llama.cpp/llama-server e GGUF; piccolo modello coding quantizzato come punto di partenza. Gestire in modo trasparente limiti di RAM, velocità e qualità.
5. Sicurezza: modello non autorizzato a eseguire o modificare file arbitrari; proposte revisionabili, percorsi consentiti, isolamento effettivo per codice generato non fidato.
6. Evoluzione verso GUI minimale, supporto progetti multipli, controlli IA, test e gestione versioni.

## Stato incluso nel pacchetto
- Versione: READY Linux 0.3; prototipo Python/terminale per Linux, **NON** distribuzione avviabile, GUI o coding agent autonomo completo.
- `readylinux.py`: ambiente READY e comandi storici; `vibe.py`: progetti, generazione di proposte, diff, applicazione, undo e verifica; `ai_local.py`: integrazione localhost con llama-server; script install e setup IA CPU.
- Esempi dei comandi: `AI START`, `PROGETTO NUOVO demo`, `CREA ...`, `DIFFERENZE`, `APPLICA`, `VERIFICA`, `CORREGGI ...`, `INDIETRO`.
- La proposta resta separata dalla scrittura; `ESEGUI file.py CONFERMO` esegue codice con i permessi dell'utente e **non** è una sandbox.
- Lo script `setup-ai-cpu.sh` usa llama.cpp e un modello Qwen2.5-Coder-1.5B-Instruct GGUF Q4_K_M; verificare URL, compatibilità delle versioni e disponibilità prima di installare.
- Verifiche al momento di questo handoff: **26 test automatici passati** in locale il 18/10/2026. Test HTTP con server simulato; nessuna prova qui di inferenza GGUF reale su CPU. Consultare README per requisiti e limiti.

## Comandi di verifica
```bash
python3 -m compileall -q readylinux.py ai_local.py vibe.py
python3 -m unittest discover -s tests -v
bash -n install.sh setup-ai-cpu.sh
```

## Evoluzione desiderata e ordine suggerito
1. Audit del codice e dei test già presenti, con elenco dei limiti reali; evitare riscritture ingiustificate.
2. Progettare l'interfaccia vibe-first del sistema (interazione naturale, file, diff, log, spiegazione, pulsanti di approvazione), preferibilmente modulare e compatibile con poca RAM.
3. Aggiungere pipeline agente in piccoli passi: pianifica → patch → verifica statica → test isolati → review → applica. Privilegi e confini sempre espliciti.
4. Integrare isolamento dei processi/risorse, permessi di accesso ai file e alla rete, riproducibilità e Git/versionamento.
5. Validare modello e prestazioni su hardware CPU-only reale, con benchmark riproducibili e fallback se il modello non è disponibile.
6. Creare una distribuzione Linux riproducibile e avviabile (valutare Buildroot rispetto a Yocto; non decidere senza motivazione). Avvio diretto nella sessione READY, con recovery e aggiornamenti.

## Limiti e punti da NON assumere
- Non affermare che la generazione AI funzioni bene senza test con il modello reale.
- Non descrivere la 0.3 come un OS completo o un sistema grafico pronto.
- Non fare eseguire automaticamente codice suggerito dall'IA; distinguere verifica statica da esecuzione.
- Non applicare download di modelli, modifiche al sistema o operazioni privilegiate senza richiesta esplicita.
- Non inventare caratteristiche hardware dell'utente o misure di prestazione.

## Primo incarico da affidare a Codex
Leggi `README.md`, `CONTEXT.md` e `AGENTS.md`. Esamina il codice della versione 0.3 e lancia i test presenti. Confronta implementazione e requisiti, individua rischi e limiti, poi proponi una roadmap tecnica verificabile per passare da prototipo terminale a distribuzione Linux vibe-coding-first. Non iniziare grandi refactoring né scaricare modelli senza esplicita approvazione.
