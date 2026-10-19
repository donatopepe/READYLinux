# Scelta modello AI e hardware (policy MVP)

Ultima revisione: 2026-10-18. È una policy di manutenzione e una stima prudenziale per capacità, non un'indagine live di mercato. In questo firing non è stata fatta ricerca web: non è disponibile uno strumento browser/search e le istruzioni del repository vietano di avviare operazioni di rete/download. Prezzi, disponibilità e ranking di prodotto non sono quindi attuali né verificati.

## Fatti sul prototipo corrente

- Lo script di setup opt-in seleziona `Qwen2.5-Coder-1.5B-Instruct Q4_K_M`, file GGUF di circa 1,12 GB.
- `setup-ai-cpu.sh` clona llama.cpp e scarica il file solo quando viene lanciato esplicitamente; controlla SHA-256 fissato prima di spostare il modello al nome definitivo.
- Download effettivo, inferenza, picco RAM, throughput e qualità non sono verificati dalla suite automatica corrente. I test AI usano un server HTTP simulato.
- READY funziona senza modello. AI è opzionale. Generazione/proposta, revisione/approvazione ed esecuzione esplicita restano separate.

## Guida d'acquisto basata sulla capacità

Soglie provvisorie per il piccolo modello CPU corrente; non sono requisiti universali:

| Profilo | Configurazione indicativa | Motivo/limite |
|---|---|---|
| Console senza AI | x86-64 supportata dalla distro, 4 GB RAM | BASIC/Python non richiedono GGUF; storage progetti separato |
| Prove AI CPU brevi | CPU x86-64 recente, almeno 4 core, 16 GB RAM, SSD con 10+ GB liberi | Margine per OS, modello e contesto breve; latenza non garantita |
| Uso CPU AI più confortevole | CPU moderna 6–8 core, 32 GB RAM, SSD 256+ GB | Più margine per contesto e multitasking; scaling non lineare garantito |
| Modelli più grandi/contesto lungo futuri | Rivalutare da 64 GB RAM; GPU solo dopo benchmark del modello scelto | Fuori dal profilo testato; nessuna raccomandazione attuale verificata |

Prima dell'acquisto controllare benchmark CPU single/multi-thread correnti, RAM dual-channel espandibile, storage, rumorosità, consumo, supporto Linux/driver e garanzia. Non si raccomandano marchi, SKU, prezzi o rivenditori. Verificare compatibilità e condizioni di reso con il venditore. Aggiornare solo con fonti datate e benchmark riproducibili. La dimensione del GGUF non è il fabbisogno RAM: runtime e contesto richiedono memoria aggiuntiva.

## Requisiti per un catalogo di modelli selezionabili

Per ogni voce registrare modello/repository esatto e revisione immutabile, quantizzazione, licenza e redistribuzione, dimensione/digest verificato, runtime compatibile, RAM attesa per contesto dichiarato, CPU/GPU, URL sorgente, data ricerca, metodo di download, import offline e istruzioni di rollback/rimozione. La selezione deve essere opt-in: niente download all'avvio. Validare l'artefatto prima di attivarlo; se download o checksum falliscono, conservare i modelli esistenti verificati.

## Piano di validazione (non eseguito)

1. Testare schema/catalogo con fixture locali; niente rete.
2. Testare selezione, modello non disponibile, digest errato, staging interrotto e rollback con directory temporanea e server HTTP fake.
3. Su host Linux consenziente, provisionare esplicitamente il modello fissato, verificare digest e annotare revisione/build flag llama.cpp.
4. Benchmark con prompt, token e contesto fissati, warm-up e ripetizioni: tokens/s, time-to-first-token, picco RSS, CPU/temperature. Distinguere mock test da inferenza reale.
5. Aggiornare la guida hardware solo con ricerca datata e misure; indicare regione/data ed evitare prezzi non supportati.
