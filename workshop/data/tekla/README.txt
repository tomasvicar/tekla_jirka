DATA Z TEKLY - SYNTETICKA CVICNA DATA
=====================================
Vse je vymyslene (generator tools/make_tekla_data.py, deterministicky).
Ocelova hala 24 x 48 m, 9 ramu po 6 m, vyska okapu 6 m.

hala_revA_assembly_list.csv  seznam sestav, revize A (12. 10. 2026)
hala_revA_part_list.csv      seznam dilu,   revize A
hala_revB_assembly_list.csv  seznam sestav, revize B (27. 10. 2026)
hala_revB_part_list.csv      seznam dilu,   revize B
cenik.xlsx                   cenik oceli, povrchove upravy a prace
nc_dstv/                     DSTV (NC1) soubory pro dilenske stroje + dstv_nc.log

Format CSV: kodovani UTF-8, oddelovac strednik, desetinna carka.
Nad tabulkou je 6 radku hlavicky reportu, pod tabulkou prazdny radek a radek CELKEM.
WEIGHT a AREA jsou na 1 kus. QTY je pocet kusu v celem modelu.
Fáze (PHASE): 1 = hlavni ramy, 2 = strecha, 3 = steny.
CLASS: 2 sloupy, 3 nosniky, 4 ztuzidla, 5 vaznice, 6 pazdiky, 9 plechy.
UDA_VYKRES = cislo dilenskeho vykresu, UDA_DODAVKA = kdo dodava.
