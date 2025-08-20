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

Za pobiranje podatkov zaženite program main.py in dovolite, da nekaj časa deluje. Ker sem uporabil samo en Selenium driver brez requests, je proces dokaj počasen, realističen čas čakanja pa je okoli 20-40 minut. Za uporabo morate imeti naložen brskalnik Google Chrome ali pa spremeniti brskalnik na enega izmed Selenium podprtih brskalnikov Edge, Firefox, Internet Explorer ali Safari. **Opozarjam, da sem zajem podatkov storil z Google Chrome, torej ne morem zagotoviti, da bo program deloval z drugimi brskalniki.**

Ko so podatki naloženi, se nahaja analiza podatkov v Jupyter zvezku v istem okolju.