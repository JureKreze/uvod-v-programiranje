# uvod-v-programiranje

# Analiza podatkov o diplomskih, magistrskih in doktorskih nalogah

V tem projektu gledamo doktorske disertacije po Univerzi v Ljubljani in Univerzi v Mariboru. Prvi interes je pogledati teorijo, da se sčasoma več in več doktorskih nalog piše v angleščini in manj v slovenščini. Poleg tega bomo analizirali še distribucijo predmetov, spremembe v deležu populacije, ki pridobi doktorat in še kaj drugega.

## Viri podatkov

Podatke pobiramo iz javnega repozitorija RUL za Univerzo v Ljubljani ter DKUM (Digitalna Knjižnica Univerze v Mariboru) za Univerzo v Mariboru.

## Navodila za uporabo

Vse potrebne knjižnice lahko naložite z uporabo ukaza
```
pip install -r requirements.txt
```
v ukazni vrstici, ko imate repozitorij naložen na računalniku.

Za pobiranje podatkov zaženite program main.py in dovolite, da nekaj časa deluje. Ker sem uporabil dva Selenium driverja brez requests, je proces dokaj počasen, realističen čas čakanja pa je okoli 20+ minut (poskusil sem na 2 računalnikih. Na enem je trajalo 20 minut, na drugem pa 45). Za uporabo morate imeti naložen brskalnik Google Chrome ali pa spremeniti brskalnik na enega izmed Selenium podprtih brskalnikov Edge, Firefox, Internet Explorer ali Safari. **Opozarjam, da sem zajem podatkov storil z Google Chrome, torej ne morem zagotoviti, da bo program deloval z drugimi brskalniki.**

Za zagon programa, se navigirajte v ukazni vrstici do repozitorija in zaženite pridobivanje podatkov z enim od naslednjih načinov:

### 1. Pridobivanje podatkov z RUL in DKUM hkrati (hitrejše, uporabi več RAM-a)

V eno ukazno vrstico vpištite
```
python main.py ljubljana
```
V drugo pa
```
python main.py maribor
```

### 2. Pridobivanje podatkov z RUL, potem pa iz DKUM (počasneje, uporabi manj RAM-a)

V ukazno vrstico vpišite
```
python main.py
```

Ko so podatki naloženi, se nahaja analiza podatkov v Jupyter zvezku v istem okolju.

## Znani problemi in opombe

### 1. Čas izvajanja in nastavitve porabe energije

Ker program traja dolgo (25+ minut) za pobiranje podatkov, je naravno, da uporabnik želi nekam oditi in nekaj drugega početi vmes. To deluje, ampak lahko tudi nastane problem. Namreč, če gre računalnik v sleep ali hibernate mode, program neha delovati in se ukine. Temu se uporabnik lahko izogne preko nastavitev
```
(Windows)
Options -> System -> Power & battery.
```

Pomembno pa je, da uporabnik na prenosnem računalniku ne zapre svojega prenosnega računalnika, ker to tudi ukine program. Lahko pa zaklene svoj ekran, kar se na Windowsih naredi s pritiskom gumba Windows in L.

### 2. Internetna povezava

Potrebna je neprekinjena internetna povezava. V posebnem primeru, če ste z računalnikom povezani na mobilne podatke preko hotspota na telefonu, bodite previdni, da ne zapustite prostora s telefonom.

### 3. Zahtevnost programa

Program uporabi precej spomina (zna uporabiti 5.5 GB). To je tudi razlog, da ni hitrejši - lahko bi uporabljal več driverjev in bil hitrejši, ampak bi predvidoma s tem uporabljal več virov. Načeloma 5.5 GB ni prekomerno za modernejše naprave, ampak morda je problem za uporabnike na opremi z manj RAMa in za uporabnike, ki imajo veliko odprtih zavitkov na brskalniku ali delajo kaj drugega v ozadju. 

### 4. Možna nekompatibilnost

Program je bil preizkušen na dveh napravah. Obe sta uporabljali operacijski sistem Windows, na obeh je deloval. Ne morem zagotoviti kompatibilnosti z drugimi operacijskimi sistemi.

## Uporaba umetne inteligence

V procesu pisanja naloge sem v zmernih količinah uporabljal umetno inteligenco. Uporabil sem jo za namene razhroščevanja, ugotavljanja težavnosti, potrebnih knjižnic, primernih metod in kritiziranje kode.

Z izjemo GitHub Copilot code completions sem napisal vso kodo sam (oz. jo prekopiral iz uradne dokumentacije in spletnih forumov), ta pa je pomagal le pri naštevanju in ponavljanju podobnih, že vgrajenih funkcij (nisem ga uporabljal za implementacijo logike).