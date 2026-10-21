# READY BASIC (Italiano)

READY BASIC è una modalità opzionale esplicita; la modalità esistente di righe numerate Python resta invariata. Entra con `BASIC`; torna a READY con `STOP` (o `QUIT`/`EXIT` dentro BASIC).

## Comandi

- `10 PRINT "CIAO"` — inserisce/sostituisce una riga numerata.
- `10` — elimina riga 10.
- `LIST`, `RUN`, `NEW`, `HELP`, `STOP`.
- `SAVE nome`, `LOAD nome` — file `.bas` nel workspace; nomi ammessi: lettere, numeri, `_`, `-`.
- `EDIT n` — mostra la riga numerata.

## Linguaggio implementato

I risultati booleani vengono stampati come `True`/`False`, non come 1/0.

`LET`/assegnazione, `PRINT`, `INPUT`, aritmetica, confronti, booleani `AND`/`OR`/`NOT`, `IF condizione THEN riga`, `GOTO`, `GOSUB`/`RETURN`, `FOR`/`NEXT` con `STEP` opzionale, `REM`, `END`, `STOP`.

Le espressioni usano un valutatore AST con allowlist; chiamate/attributi Python e sintassi non supportata vengono rifiutati. L'esecuzione ha un limite configurabile di istruzioni. Questa restrizione **non** è una sandbox per altro codice generato.

Esempio:

```basic
10 FOR I=1 TO 3
20 PRINT I
30 NEXT I
40 END
```

I test verificano aritmetica, salti, cicli, input, subroutine, persistenza, input malformato, chiamate rifiutate e limite di esecuzione. Dialetto BASIC ridotto: non garantisce compatibilità completa con Commodore BASIC.
