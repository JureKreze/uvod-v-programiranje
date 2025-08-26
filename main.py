import time
import sys

from male_funkcije import shrani_disertacije, shrani_komentorje, shrani_disertacije_maribor
from pobiranje import delaj
from pobiranje_mb import delaj_mb

if __name__ == "__main__":
    if len(sys.argv) < 2:
        '''Standardna nastavitev za uporabnika, pridobi podatke najprej iz RUL, potem iz DKUM'''
        čas_začetka = time.time()
        disertacije = delaj()
        disertacije_mb = delaj_mb()
        shrani_disertacije(disertacije)
        shrani_disertacije_maribor(disertacije_mb)
        shrani_komentorje(disertacije, "Ljubljana")
        shrani_komentorje(disertacije, "Maribor")
        čas_konca = time.time()
    else:
        target = sys.argv[1].lower()
        if target == "ljubljana":
            '''Pridobi od RUL'''
            čas_začetka = time.time()
            disertacije = delaj()
            shrani_disertacije(disertacije)
            shrani_komentorje(disertacije, "Ljubljana")
            čas_konca = time.time()
        elif target == "maribor":
            '''Pridobi od DKUM'''
            čas_začetka = time.time()
            disertacije_mb = delaj_mb()
            shrani_disertacije_maribor(disertacije_mb)
            shrani_komentorje(disertacije_mb, "Maribor")
            čas_konca = time.time()
        else:
            print("Vpišite python main.py [ljubljana|maribor|(nič)], če ne vpišete ničesar, se oboje izvede")
            print("Možno je tudi v dveh ločenih ukaznih vrsticah zagnati oboje hkrati.")
    čas_trajanja = čas_konca - čas_začetka
    print(f"Čas iskanja: {čas_trajanja} sekund")