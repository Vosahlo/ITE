## ITE 2016 zadání semestrální práce

### Zjednodušené zadání

Semetrální práce se skládá ze zpracování **zip** souboru obsahujícího logy z databáze jejich zpracováním, získáním jednoduchých statistik a vytvoření histogramu pro zadané časové období. Berte v potaz, že data obsahují cca 100000 logů (velikost souboru je 44 MB).

### Přesné zadání

Semestrální práce se skládá z několika částí, které jsou samostatně bodovány. Maximální počet bodů je *60* + *5* jako bonus. Semestrální práci vypracujete v týmech. Složení týmů odpovídá složkám (resp. jménům v názvu složek) na SVN.

1. Načtení **zip** souboru a jeho zpracování (realizováno jako Tornado server) - **20 bodů**.

  * vytvořte Tornado server, který bude umět pracovat s daty,
  * data obsahují přibližně 100000 záznamů (JSON souborů), bylo by asi dobré načítat data přímo ze zipu,
  * zvolte vhodnou strukturu k uložení dat v paměti,
  * je na Vás jestli data načtete při prvním spuštění serveru nebo je budete načítat vždy při obdržení požadavku.

2. Vytvoření histogramu - **10 bodů**.

  * pro zadané časové období se vygeneruje histogram,
  * pokud není časové období zadáno vygeneruje se histogram pro všechna data,
  * pro vyzkoušení funkčnosti vytvořte klienta v Pythonu,
  * jak bude histogram realizován (Ascii, obrázek, apod. je na Vás),
  * dobrý nápad bude, použití knihoven pro vykreslování (např. kombinace Scipy + numpy + matplotlib).

3. Vyhledání řetězce - **15 bodů**.

  * zadáte řetězec a jako výsledek získáte všechny logy, které obsahují tento řetězec,
  * pro vyzkoušení funkčnosti vytvořte klienta v Pythonu,
  * realizace prohledávání je na Vás (full text není vyžadován, ale kdo se chce něco naučit, měl by ho minimálně zkuit).

4. Vytvoření klientské části - **15 bodů**.

  * vytvořte webového klienta, který bude umět zobrazit logy (jak, to je na Vás),
  * klient bude umět filtrovat data podle data (od - do) a podle zadaného text,
  * klient bude umět zobrazit histogram načtených logů.

#### Bodový bonus

Při dodržení PEP8 (případně i doporučení pro Javascript) se připočte k výslednému bodovému ohodnocení **5 bodů**. Proto používejte lintery :).

> Iniciativě v rozšíření funkčnosti se meze nekladou a mohou zapříčinit, že v rámci možností přehlédnu nedostatky v jiné části zadání.


### Kde získám data?

Zazipovaná data je možné stáhnout [zde](http://turing.kky.zcu.cz/ite/2016/logs.dump.zip).

> Pokud si nebudete vědět rady neváhejte se zeptat.
