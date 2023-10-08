# Popis projektu
Třetí pro ENGETO Python Academy. Poskytuje Pythonový skript pro scrapování dat voleb z roku 2017 z webu https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ a jejich export do CSV tabulky.

## Instalace knihoven
Knihovny použité v kódu jsou uloženy v souboru `requirements.txt.` Pro instalaci spusťte:
```
pip install -r requirements.txt
```

## Spuštění
Pro spuštění skriptu budete potřebovat dva argumenty. Použijte následující příkaz:
```
python scraper.py <URL> <output_file.csv>
```
- **\<URL\>**: odkaz ze kterého chcete vyscrapovat výsledky hlasování pro všechny obce (resp. pomocí `X` ve sloupci `Výběr obce`).

- **<output_file.csv>** název CSV souboru, do kterého budou údaje exportovány.

Výsledky voleb budou exportovány jako soubor CSV.

## Příklad
Výsledky voleb pro Beroun:
- 1. argument: `"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102"`
- 2. argument: `beroun_vysledky.csv`

Spuštění skriptu:
```
python scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102" beroun_vysledky.csv
```

Proces exportu:
```
Export election results from https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102...
CSV file beroun_vysledky.csv has been created.
```
Částečný výstup:
```
code,name,registered,envelopes,valid,...
534421,Bavoryně,239,151,150,18,0,0,6,0,8,7,5,2,4,0,0,16,0,0,11,55,0,2,3,0,0,0,2,11,0
531057,Beroun,14804,9145,9076,1363,16,11,576,1,433,651,140,78,205,8,12,1290,4,6,641,2433,3,13,279,2,61,17,12,800,21
531073,Běštín,262,158,157,27,2,0,21,0,2,11,3,3,3,1,0,12,0,0,2,40,0,0,2,0,1,0,1,26,0
531081,Broumy,743,491,489,62,1,0,35,2,20,54,6,5,8,0,0,76,1,3,22,144,0,4,11,0,3,0,0,32,0
...
```
