# READY Linux 0.3 — Vibe Coding First, IA locale CPU

Questo progetto è distribuito con licenza [MIT](LICENSE).

**Descrivi un programma in linguaggio naturale → genera una proposta di file → controlla le differenze → approva → verifica → migliora.**

READY 0.3 è un **prototipo applicativo Linux da terminale**, non una distribuzione Linux avviabile autonoma, non un desktop grafico e non un coding agent completamente autonomo. Riutilizza la modalità programmabile READY 0.2 (Python e programmi numerati), ma mette il *vibe coding* al centro dell'interazione.

**Stato delle verifiche:** test automatici locali contro un server HTTP simulato e test su filesystem reale. **Non è stata verificata qui l'inferenza effettiva di un modello GGUF sulla CPU** né la qualità dei progetti prodotti dall'IA. I file non vengono scaricati da Internet se non avvii esplicitamente gli script di installazione.

## 1. Requisiti

- GNU/Linux, Python 3.10+ e libreria standard Python.
- Opzionale per la generazione: `llama-server` (llama.cpp) e modello locale GGUF compatibile. I normali comandi di progetto funzionano anche senza IA.
- Nessuna GPU necessaria: il servizio opzionale viene compilato CPU-only e avviato con `--n-gpu-layers 0 --device none`.
- Modello di default nello script opzionale: **Qwen2.5-Coder-1.5B-Instruct Q4_K_M**, GGUF circa **1,12 GB**; il consumo RAM totale supera la dimensione del file e cresce con il contesto. La velocità dipende da CPU, RAM, build e prompt; provare con pochi file.

### Hardware consigliato (stima, non lista d'acquisto verificata)

Data revisione: 2026-10-18. Stime conservative di capacità per il modello attuale, non requisiti misurati. Il modello non è stato scaricato né benchmarkato; prezzi, stock e SKU non sono verificati. In questo firing non è stata svolta ricerca web: non è disponibile uno strumento browser/search e le regole del repository vietano di avviare operazioni di rete.

| Uso | Configurazione da cercare | Motivazione/limite |
|---|---|---|
| Console senza AI | Qualsiasi x86-64 supportato dalla distro, 4 GB RAM | Python/BASIC non richiedono GGUF; storage per progetti separato |
| AI CPU, prove brevi | CPU x86-64 recente, 4+ core, 16 GB RAM, SSD con almeno 10 GB liberi | Margine per OS, modello e contesto breve; latenza non garantita |
| AI CPU, uso quotidiano | 6–8 core moderni, 32 GB RAM, SSD NVMe 256+ GB | Più margine per contesto e altri processi; più core non garantiscono scala lineare |
| Modelli più grandi/contesto lungo futuri | 64 GB RAM o più; valutare GPU solo dopo benchmark del modello scelto | Fuori dal profilo testato; non acquistare GPU sulla base di questa roadmap |

Prima dell'acquisto confrontare benchmark CPU aggiornati, RAM dual-channel espandibile, storage, rumorosità, consumi, supporto Linux/driver e garanzia. Nessun marchio/SKU/prezzo/rivenditore è raccomandato; verificare compatibilità e resi. Aggiornare solo con fonti datate e benchmark riproducibili. Vedere la [policy modello/hardware](docs/AI_HARDWARE.it.md) e la versione [English](docs/AI_HARDWARE.en.md). Il piano gated per chiudere le verifiche aperte è in [docs/VERIFICATION_PLAN.md](docs/VERIFICATION_PLAN.md).
- Modelli piccoli possono fallire nella produzione del JSON richiesto o scrivere codice errato. Usare compiti brevi, pochi file e revisionare sempre.

## 2. Avvio rapido

Estrai l'archivio ZIP e nella directory `readylinux_mvp` esegui:

```bash
python3 readylinux.py
```

Installazione senza permessi amministrativi:

```bash
bash install.sh
~/.local/bin/readylinux
```

Per scaricare/compilare **su richiesta** il motore IA e il modello (richiede Internet per il setup):

```bash
bash setup-ai-cpu.sh
~/.local/bin/readylinux
```

Per usare il runtime BASIC sperimentale, digita `BASIC`; usa `HELP` per i comandi e `STOP` per tornare a READY. La modalità numerata Python resta il flusso legacy. Vedi [`docs/BASIC.md`](docs/BASIC.md) (IT) e [`docs/BASIC.en.md`](docs/BASIC.en.md) (EN).

In READY digita `AI START`, quindi verifica con `AI STATUS` quando il modello è pronto. `AI STOP` arresta soltanto il processo avviato dalla sessione corrente, non un server esterno già esistente.

L'applicazione può usare un modello installato manualmente:

```bash
python3 readylinux.py \
    --ai-model /percorso/modello.gguf \
    --ai-server /percorso/llama-server \
    --ai-threads 4 \
    --ai-port 18080
```

`llama-server` risponde solo su `127.0.0.1`: READY non usa servizi remoti o API cloud. Il client HTTP disabilita l'utilizzo dei proxy HTTP dell'ambiente.

## 3. Esempio di sessione (illustrativo: non è output reale di un GGUF)

```text
READY LINUX 0.3 | VIBE-FIRST + LOCAL CPU AI
> AI START
> AI STATUS
> PROGETTO NUOVO giochi
> CREA Scrivi un gioco Python che faccia indovinare un numero da 1 a 10
[ANTEPRIMA JSON / DIFF — NESSUN FILE MODIFICATO]
> DIFFERENZE
[MODIFICHE PROPOSTE]
> APPLICA
Modifica applicata...
> FILE PROGETTO
main.py
> VERIFICA
Analisi statica: ... NESSUN codice eseguito.
> ESEGUI main.py CONFERMO
[Esecuzione esplicita, NON isolata; solo codice fidato]
> CORREGGI Gestisci anche il caso in cui inserisco testo non numerico
[ANTEPRIMA MODIFICHE]
> APPLICA
> INDIETRO
Ultima modifica ripristinata.
```

Puoi anche digitare direttamente una richiesta naturale con più parole, per esempio `crea un calendario da terminale`. Se riconosciuta come descrizione anziché come comando Python, viene inviata al generatore locale. Per il comportamento meno ambiguo usa `CREA ...` o `MODIFICA ...`. `PY print(2+2)` consente l'esecuzione Python immediata.

## 4. Comandi principali

| Comando | Operazione |
|---|---|
| `PROGETTO NUOVO nome` | Crea e seleziona un progetto |
| `PROGETTO USA nome` | Attiva un progetto esistente |
| `PROGETTI` / `FILE PROGETTO` | Elenca progetti e file |
| `CREA descrizione` | Propone file nuovi o modificati tramite il modello |
| `MODIFICA descrizione` | Propone aggiornamenti ai file del progetto |
| `CORREGGI descrizione` | Include anche l'ultimo output di esecuzione per suggerire correzioni |
| `DIFFERENZE` | Visualizza il diff ancora non applicato |
| `APPLICA` / `ANNULLA` | Approva o scarta una proposta |
| `INDIETRO` | Ripristina l'ultima modifica applicata se i file non sono cambiati nel frattempo |
| `VERIFICA` | Verifica la sintassi Python e JSON, senza eseguire alcun codice |
| `ESEGUI file.py CONFERMO` | Esegue esplicitamente Python **senza sandbox**, timeout di 10 secondi |
| `AI START`, `AI STATUS`, `AI STOP` | Gestisce il processo di IA locale |
| `BASIC` | Entra nella modalità BASIC sperimentale; `STOP` torna a READY |
| `BASIC HELP` | Mostra i precedenti comandi READY, programmi numerati inclusi |
| `HELP` | Mostra il nuovo flusso vibe-first |

## 5. Build Linux embedded (scaffolding sperimentale)

È presente il layer Yocto minimo `meta-readylinux/`. La ricetta installa l'app READY da sorgenti locali, senza scaricare pesi IA. Non è ancora stata eseguita una build BitBake: serve un host Linux con release Yocto e machine selezionate. Dettagli in [`meta-readylinux/README.md`](meta-readylinux/README.md) (IT) e [`meta-readylinux/README.en.md`](meta-readylinux/README.en.md) (EN). Non considerare il layer un'immagine verificata o bootabile.

## 6. Sicurezza e limiti

- Il modello **non può eseguire** comandi attraverso la risposta: genera soltanto JSON con lista dei file. Sono ammessi file di testo e codice con estensioni consentite, sotto la cartella del progetto.
- Percorsi assoluti, `..`, file nascosti e symlink di destinazione vengono rifiutati. Il programma legge un contesto limitato dal progetto attivo e non naviga arbitrariamente nell'intero filesystem.
- Ogni proposta mostra il diff e richiede `APPLICA`. Se un file cambia dopo la proposta, l'applicazione viene rifiutata. Lo storico consente l'ultimo undo, salvo modifiche manuali successive.
- I test automatici controllano validazione dei percorsi, conflitti e il fatto che `VERIFICA` **non** esegua il codice.
- **NON è un sistema blindato per l'esecuzione di codice sconosciuto.** `ESEGUI` usa un normale sottoprocesso Python con i permessi dell'utente e **può accedere a file e rete**; la modalità numerata `RUN` e `PY` sono anch'esse non isolate. Il timeout limita la durata, non i privilegi o le risorse. Per testare output IA non fidato utilizzare una VM/container configurati con restrizioni reali.
- Non sono stati implementati LSP, test unitari generati ed eseguiti automaticamente, sandbox Linux, desktop grafico o ISO avviabile. Il runtime BASIC è sperimentale e non garantisce compatibilità completa Commodore.
- Gli input inclusi nei file e i log sono trattati come non attendibili nelle istruzioni al modello; questo **non garantisce immunità** dagli attacchi di prompt injection.
- La generazione è limitata a 5 file per richiesta, 14.000 caratteri per file e 28.000 caratteri complessivi. Contesto attuale massimo 5 file. Nella pratica, un modello 1.5B e il contesto disponibile possono imporre limiti ben inferiori.

## 6. Test ripetibili

```bash
python3 -m compileall -q readylinux.py ai_local.py vibe.py
python3 -m unittest discover -s tests -v
bash -n install.sh setup-ai-cpu.sh
```

L'integrazione HTTP in test usa `ThreadingHTTPServer` simulato: verifica la richiesta `response_format=json_object` e il ciclo proposta/applicazione/controllo/ripristino, **non** la capacità del modello vero di generare JSON corretto.

## 7. Verso un sistema operativo veramente vibe-first

1. Creare una distribuzione Linux x86-64 avviabile (Yocto o Buildroot) con account utente, sessione READY di default e aggiornamenti verificati.
2. Integrare un launcher grafico minimale con input naturale principale, vista file, diff, output, controlli per il modello e terminale.
3. Gestire contesto e qualità con una pipeline pianificazione → modifiche piccole → compilazione/analisi statica → test isolati → revisione, sempre con permessi espliciti.
4. Aggiungere sandbox (namespace, seccomp/cgroup, filesystem e rete ristretti), Git per snapshot/versionamento, IDE/LSP e selezione dei modelli in base a CPU/RAM.
5. Misurare su hardware reale consumi, memoria, latenza/token, qualità delle modifiche, tassi di errore e tempi di avvio.

Riferimenti dei componenti: [llama.cpp server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md), [Qwen2.5-Coder-1.5B GGUF](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF).
