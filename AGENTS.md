# Istruzioni per Codex — READY Linux

## Missione
Sviluppare READY Linux come ambiente Linux incentrato sul vibe coding, con IA locale su CPU e uso offline dopo il provisioning. Consulta `CONTEXT.md` e `README.md` prima di modificare codice.

## Verifica e veridicità
- Tratta i file nel repository e gli esiti dei test come fonte primaria dello stato; distingue requisiti, implementazione e funzionalità verificate.
- Non dichiarare test completati se non eseguiti davvero. Riporta comandi, risultati ed eventuali limiti dell'ambiente.
- Preferisci modifiche incrementali e riproducibili; non sostituire componenti funzionanti senza motivazione o test di regressione.

## Vincoli
- Kernel Linux, niente riscrittura del kernel.
- CPU-only sempre supportato; niente servizi cloud obbligatori, API a pagamento o telemetria di default.
- Generazione, approvazione ed esecuzione restano fasi distinte. Non eseguire automaticamente codice dell'IA.
- Per codice generato non fidato, non chiamare "sandbox" un normale sottoprocesso; richiedere isolamento reale e verificabile.
- Non avviare download di modelli, modifiche privilegiate, network o pubblicazione senza autorizzazione.
- Quando esiste una proposta di modifica, esporre differenze e consentire il rifiuto e il rollback.

## Test rapidi
```bash
python3 -m compileall -q readylinux.py ai_local.py vibe.py
python3 -m unittest discover -s tests -v
bash -n install.sh setup-ai-cpu.sh
```
