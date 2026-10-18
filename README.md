# READY Linux 0.3 — Vibe Coding First, IA locale CPU

Questo progetto è distribuito con licenza [MIT](LICENSE).

**Descrivi un programma in linguaggio naturale → genera una proposta di file → controlla le differenze → approva → verifica → migliora.**

READY 0.3 è un **prototipo applicativo Linux da terminale**, non una distribuzione Linux avviabile autonoma, non un desktop grafico e non un coding agent completamente autonomo. Riutilizza la modalità programmabile READY 0.2 (Python e programmi numerati), ma mette il *vibe coding* al centro dell'interazione.

**Stato delle verifiche:** test automatici locali contro un server HTTP simulato e test su filesystem reale. **Non è stata verificata qui l'inferenza effettiva di un modello GGUF sulla CPU** né la qualità dei progetti prodotti dall'IA. I file non vengono scaricati da Internet se non avvii esplicitamente gli script di installazione.

## 1. Requisiti

- GNU/Linux, Python 3.10+ e libreria standard Python.
- Opzionale per la generazione: `llama-server` (llama.cpp) e modello locale GGUF compatibile. I normali comandi di progetto funzionano anche senza IA.
- Nessuna GPU necessaria: il servizio opzionale viene compilato CPU-only e avviato con `--n-gpu-layers 0 --device none`.
- Modello scelto nello script opzionale: **Qwen2.5-Coder-1.5B-Instruct Q4_K_M**, file GGUF di circa **1,12 GB**; **RAM totale necessaria maggiore della dimensione del file**. La velocità varia per CPU e parametri.
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
| `BASIC HELP` | Mostra i precedenti comandi READY, programmi numerati inclusi |
| `HELP` | Mostra il nuovo flusso vibe-first |

## 5. Sicurezza e limiti

- Il modello **non può eseguire** comandi attraverso la risposta: genera soltanto JSON con lista dei file. Sono ammessi file di testo e codice con estensioni consentite, sotto la cartella del progetto.
- Percorsi assoluti, `..`, file nascosti e symlink di destinazione vengono rifiutati. Il programma legge un contesto limitato dal progetto attivo e non naviga arbitrariamente nell'intero filesystem.
- Ogni proposta mostra il diff e richiede `APPLICA`. Se un file cambia dopo la proposta, l'applicazione viene rifiutata. Lo storico consente l'ultimo undo, salvo modifiche manuali successive.
- I test automatici controllano validazione dei percorsi, conflitti e il fatto che `VERIFICA` **non** esegua il codice.
- **NON è un sistema blindato per l'esecuzione di codice sconosciuto.** `ESEGUI` usa un normale sottoprocesso Python con i permessi dell'utente e **può accedere a file e rete**; la modalità numerata `RUN` e `PY` sono anch'esse non isolate. Il timeout limita la durata, non i privilegi o le risorse. Per testare output IA non fidato utilizzare una VM/container configurati con restrizioni reali.
- Non sono stati implementati LSP, test unitari generati ed eseguiti automaticamente, sandbox Linux, Git integration, desktop grafico o ISO avviabile.
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
