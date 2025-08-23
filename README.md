# uvod-v-programiranje
# Analiza podatkov o diplomskih, magistrskih in doktorskih nalogah

V tem projektu gledamo doktorske disertacije po Univerzi v Ljubljani in Univerzi v Mariboru. Prvi interes je pogledati teorijo, da se sčasoma več in več doktorskih nalog piše v angleščini in manj v slovenščini. Poleg tega bomo analizirali še distribucijo predmetov, spremembe v deležu populacije, ki pridobi doktorat in še kaj drugega.

Za bolj zanimivo in zahtevno analizo bomo naredili zemljevid krajev skozi čas, ki kaže popularnost disertacij, objavljenih v tistih krajih.

## Viri podatkov

Podatke pobiramo iz javnega repozitorija RUL za Univerzo v Ljubljani ter DKUM (Digitalna Knjižnica Univerze v Mariboru) za Univerzo v Mariboru.

## Navodila za uporabo

Vse potrebne knjižnice lahko naložite z uporabo ukaza
```
pip install -r requirements.txt,
```
ko imate repozitorij naložen na računalniku. Morda morate narediti in aktivirati virtualno okolje.

Za pobiranje podatkov zaženite program main.py in dovolite, da nekaj časa deluje. Ker sem uporabil dva Selenium driverja brez requests, je proces dokaj počasen, realističen čas čakanja pa je okoli 20-40 minut. Za uporabo morate imeti naložen brskalnik Google Chrome ali pa spremeniti brskalnik na enega izmed Selenium podprtih brskalnikov Edge, Firefox, Internet Explorer ali Safari. **Opozarjam, da sem zajem podatkov storil z Google Chrome, torej ne morem zagotoviti, da bo program deloval z drugimi brskalniki.**

Ko so podatki naloženi, se nahaja analiza podatkov v Jupyter zvezku v istem okolju.

## Znani problemi in opombe

### 1. Čas izvajanja in nastavitve porabe energije

Ker program traja dolgo (25+ minut) za pobiranje podatkov, je naravno, da uporabnik želi nekam oditi in nekaj drugega početi vmes. To deluje, ampak lahko tudi nastane problem. Namreč, če gre računalnik v sleep ali hibernate mode, program neha delovati in se ukine. Temu se uporabnik lahko izogne preko nastavitev
```
(windows)
Options -> System -> Power & battery
```

Pomembno pa je, da uporabnik na laptopu ne zapre svojega laptopa, ker to tudi ukine program. Lahko pa zaklene svoj ekran, kar se na windowsu naredi s pritiskom gumba Windows in L.

### 2. Internetna povezava

Potrebna je neprekinjena internetna povezava. V posebnem primeru, če ste z računalnikom povezani na mobilne podatke preko hotspota na telefonu, bodite previdni, da ne zapustite prostora s telefonom.

### 3. Zahtevnost programa

Program uporabi precej spomina (zna uporabiti 5.5 GB). To je tudi razlog, da ni hitrejši - lahko bi uporabljal več driverjev in bil hitrejši, ampak bi predvidoma s tem uporabljal več virov. Načeloma 5.5 GB ni prekomerno za modernejše naprave, ampak morda je problem za uporabnike na opremi z manj RAMa in za uporabnike, ki imajo veliko odprtih zavitkov na brskalniku ali delajo kaj drugega v ozadju. 

### 4. Možna nekompatibilnost
Žal je bil program preizkušen le na enem sistemu, zato ne morem zagotoviti zanesljivosti programa na drugih napravah, lahko pa zagotovim, da so podatki vključeni v repozitoriju v .csv datotekah pridobljeni z natanko to kodo, ki je v repozitoriju.

## Uporaba umetne inteligence

V procesu pisanja naloge sem v zmernih količinah uporabljal umetno inteligenco. Uporabil sem jo za namene razhroščevanja, ugotavljanja težavnosti, potrebnih knjižnic, primernih metod in kritiziranje kode.

Z izjemo github copilot code completions sem napisal vso kodo sam (oz. jo prekopiral iz uradne dokumentacije in spletnih forumov), ta pa je pomagal le pri naštevanju in ponavljanju podobnih, že vgrajenih funkcij (nisem ga uporabljal za implementacijo logike).