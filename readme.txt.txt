############################## PRACA S APLIKACIOU ##########################
Skript bol testovany na interprete Python vo verzii 3.4.3

spustenie programu pre vypis napovedy:

  python3 main.py -h+
  
spustenie programu pre testovanie databayz DB-IP:

  python3 main.py -d DB-IP -i tab -v -o space input.dat

Po spusteni suboru sa vysledky vygeneruju do priecinku "/results"
Program generuje vystupne subory "<Database>_<Date>.dat"
a z tychto suborov sa generuje adresar "Maps" v ktorom sa nachadzaju mapy (html subory)
pre kazdy riadok tychto dokumentov sa vyegeneruje jeden html subor ktory obsahuje vysledne body vsetkych databaz.

Program generuje subory "Graph_results.pdf" ktory obsahuje CDF pre vsetky vysledne subory a subor "table.tex" ktory obsahuje tabulku kvantilov pre jednotlive databazy