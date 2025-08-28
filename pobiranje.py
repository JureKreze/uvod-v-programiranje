import re
import threading
from math import ceil

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from roman import fromRoman as rimske

from male_funkcije import wait_for_css, pocakaj_stran, RUL_iskanje, RUL


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.page_load_strategy = 'eager'
# Nastavitve za hitrejše delovanje Seleniuma. OPOMBA: Headless način včasih povzroča nestabilnost programa.


def zadetki(brskalnik) -> int:
    '''Pridobi število zadetkov iz iskalnika za RUL. Uporabimo kasneje, da vemo, kdaj nehati.'''
    st_zadetkov_css = wait_for_css(".StZadetkov", brskalnik)
    st_zadetkov_tekst = st_zadetkov_css.text
    st_zadetkov = int(st_zadetkov_tekst.split(" ")[0])
    return st_zadetkov

def preberi_disertacijo(
    n: int,
    leto: int,
    brskalnik: webdriver
) -> dict:
    '''Ko je driver že na strani disertacije, se uporabi ta funkcija, da pridobi
    podatke o disertaciji in jih shrani v slovar.'''
    disertacija = dict()
    naslov = brskalnik.find_element(
        By.CSS_SELECTOR, f"body > div.platno >\
         section.zadetki > div > table > tbody\
        > tr:nth-child({n}) > td > div > a:nth-child(2)"
    )
    naslov_disertacije = str(naslov.text)
    disertacija["Naslov"] = naslov_disertacije
    naslov.send_keys(Keys.RETURN)
    disertacija["Leto izida"] = leto
    povezava = brskalnik.current_url
    vzorec_id = re.compile(r'id=([0-9]+)')
    id = vzorec_id.search(povezava).group(1)
    disertacija["ID"] = id
    # Ker pridobivamo podatke iz tabele, lahko uporabimo zanko za večino podatkov. Izjeme so ročno izluščene.
    stvari_za_iskati = [
        "Jezik",
        "Organizacija",
        "Kraj izida",
        "Število ogledov",
        "Število prenosov",
        "Ključne besede"
    ]
    osebe_za_iskati = [
        "Avtor",
        "Mentor"
    ]
    for stvar in stvari_za_iskati:
        # Stvari iščemo po relativnem XPATH-u, specifično vrstica, ki ima naslov, ki vsebuje podatek, ki ga iščemo.
        try:
            stvar_element = brskalnik.find_element(By.XPATH,
    f"//tr[th[contains(normalize-space(), '{stvar}:')]]\
    /td[last()]"
    )
        except NoSuchElementException:
            stvar_element = None
        disertacija[stvar] = stvar_element.text.strip() if stvar_element else None
    for oseba in osebe_za_iskati:
        # Podobno naredimo za osebe, tokrat iščemo po spanu, ime osebe pa je pred nazivom.
        try:
            oseba_element = brskalnik.find_element(
                By.XPATH, f"//span[contains(normalize-space(), '{oseba}')]/preceding-sibling::a[1]"
            )
        except NoSuchElementException:
            oseba_element = None
        if oseba_element:
            disertacija[oseba] = str(oseba_element.text.strip())
        else:
            disertacija[oseba] = None
    try:
        komentorji_elementi = brskalnik.find_elements(
            By.XPATH, "//span[contains(normalize-space(), 'Komentor')]/preceding-sibling::a"
        )

        komentorji = [str(komentor.text.strip()) for komentor in komentorji_elementi]
    except NoSuchElementException:
        komentorji = []
    disertacija["Komentorji"] = komentorji if komentorji else []

    try:
        dolzina_element = brskalnik.find_element(
            By.XPATH, "//tr[th[contains(normalize-space(), 'Št. strani:')]]/td[last()]"
        )
        dolzina = str(dolzina_element.text)
    except NoSuchElementException:
        dolzina = "0"

    # Regex za izluščanje dolžine uvoda in dolžine glavnega dela disertacije.
    vzorec = re.compile(r'([IVXLCDM]+)?,?\s?([0-9]+)?')
    dolzina_regex = vzorec.match(dolzina)
    if dolzina_regex:
        dolzina_uvoda = rimske(dolzina_regex.group(1)) if dolzina_regex.group(1) else 0
        dolzina_glavnega_dela = int(dolzina_regex.group(2)) if dolzina_regex.group(2) else 0
    else:
        dolzina_uvoda = 0
        dolzina_glavnega_dela = 0

    disertacija["dolzina_uvoda"] = dolzina_uvoda
    disertacija["dolzina_glavnega_dela"] = dolzina_glavnega_dela
    return disertacija


def poberi(
    brskalnik: webdriver,
    leta_za_pobiranje: list[int],
    rezultat: list[dict]
) -> None:
    '''Združi iskanje in izluščanje rezultatov, jih shrani v rezultate od posamezne niti.'''
    for leto in leta_za_pobiranje:
        brskalnik.get(RUL)
        pocakaj_stran(brskalnik)
        RUL_iskanje(leto, brskalnik)
        st_zadetkov = zadetki(brskalnik)
        st_strani = ceil(st_zadetkov / 10)
        st_obdelanih = 0
        for stran in range(1, st_strani + 1):
            for zadetek in range(1, 11):
                if st_obdelanih < st_zadetkov:
                    pocakaj_stran(brskalnik)
                    try:
                        rezultat.append(preberi_disertacijo(zadetek, leto, brskalnik))
                    except NoSuchElementException:
                        continue
                    brskalnik.back()
                    st_obdelanih += 1
                else:
                    break
            if stran < st_strani:
                search_url = re.sub(r'(&page=\d+)', '', brskalnik.current_url)
                novi_url = f"{search_url}&page={stran + 1}"
                brskalnik.get(novi_url)


def delavec(
    leta_za_pobiranje: list[int],
    rezultat: list[dict]
) -> None:
    '''Naredi delavca (nit) in zažene postopek pobiranja.'''
    driver_thread = webdriver.Chrome(options=chrome_options)
    try:
        poberi(driver_thread, leta_za_pobiranje, rezultat)
    finally:
        driver_thread.quit()


leta1 = [2000 + _ for _ in range(16)]
leta2 = [2016 + _ for _ in range(9)]
# Leta1 so leta od 2000 do 2015, ki jih pridobi prvi delavec. Drugi delavec pridobi ostale do 2024.
# Ta števila sem zbral tako, ker je več disertacij v drugi polovici let in želimo, da končata približno istočasno.


def delaj() -> list[dict]:
    '''Ustvari in zažene niti za pobiranje podatkov.'''
    rezultat1 = list()
    rezultat2 = list()
    thread1 = threading.Thread(target=delavec, args=(leta1, rezultat1,))
    thread2 = threading.Thread(target=delavec, args=(leta2, rezultat2,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    return rezultat1 + rezultat2
