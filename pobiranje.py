import os
import re
import csv
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from roman import fromRoman as rimske
import time

from math import ceil

'''OPOMBA:
Ta skripta bi lahko bila veliko hitrejša. Lahko bi uporabil več niti, da bi hkrati obdeloval več strani.
To bi uporabilo veliko spomina, zato nisem tega naredil od začetka, ker že ta program uporablja precej spomina.
Prav tako bi bilo veliko lažje uporabljati requests in BeautifulSoup, vendar mi je osebno najbolj všeč Selenium, ker se ponaša z načinom, kako bi to naredil človek.'''
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)

rul = "https://repozitorij.uni-lj.si/Iskanje.php?type=napredno&lang=slv"

disertacije = list()

# Torej čakanje s time.sleep ni najboljša praksa, zato definiramo 2 funkciji za css selektorje in xpath selektorje, ki uporabljata WebDriverWait.
def wait_for_css(css_selector, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
def wait_for_xpath(xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))



def pojdi_na_stran_iskanja(stran):
    driver.get(stran)

def RUL_iskanje(leto):
    vnos_leta = wait_for_css("input.IskalniNiz[name='niz3']")
    seznam_vrst_gradiv = driver.find_element(By.CSS_SELECTOR, "#vrsta")
    vnos_leta.send_keys(str(leto))
    select = Select(seznam_vrst_gradiv)
    select.select_by_visible_text("Doktorska disertacija")
    gumb_isci = wait_for_xpath("/html/body/div[3]/section[1]/div/form/table/tbody/tr[7]/td[3]/a")
    gumb_isci.send_keys(Keys.RETURN)

def zadetki():
    st_zadetkov_css = wait_for_css(".StZadetkov")
    st_zadetkov_tekst = st_zadetkov_css.text
    st_zadetkov = int(st_zadetkov_tekst.split(" ")[0])
    return st_zadetkov

def preberi_disertacijo(n, leto):
    naslov = driver.find_element(By.CSS_SELECTOR, f"body > div.platno > section.zadetki > div > table > tbody > tr:nth-child({n}) > td > div > a:nth-child(2)")
    #body > div.platno > section.zadetki > div > table > tbody > tr:nth-child(1) > td > div > a:nth-child(2) je selektor za link do prve disertacije
    #body > div.platno > section.zadetki > div > table > tbody > tr:nth-child(2) > td > div > a:nth-child(2) je selektor za link do druge disertacije
    #sklepamo, da je selektor za n-to disertacijo zgoraj napisan v "naslov"
    naslov_disertacije = str(naslov.text)
    naslov.send_keys(Keys.RETURN)

    jezik_disertacije_element = wait_for_xpath("//tr[th[contains(normalize-space(), 'Jezik:')]]/td[last()]")
    jezik_disertacije = str(jezik_disertacije_element.text)

    organizacija_element = driver.find_element(By.CLASS_NAME, "IzpisOrg")
    organizacija = str(organizacija_element.text)

    st_ogledov_element = driver.find_element(By.XPATH, "//tr[th[contains(normalize-space(), 'Število ogledov:')]]/td[last()]")
    ogledi_text = st_ogledov_element.text.strip()
    st_ogledov = int(ogledi_text) if ogledi_text.isdigit() else 0

    st_prenosov_element = driver.find_element(By.XPATH, "//tr[th[contains(normalize-space(), 'Število prenosov:')]]/td[last()]")
    prenosi_text = st_prenosov_element.text.strip()
    st_prenosov = int(prenosi_text) if prenosi_text.isdigit() else 0

    avtor = driver.find_element(By.XPATH, "//span[contains(normalize-space(),'Avtor')]/preceding-sibling::a[1]")
    avtor = str(avtor.text) if avtor else None
    try:
        mentor = driver.find_element(By.XPATH, "//span[contains(normalize-space(),'Mentor')]/preceding-sibling::a[1]")
        mentor = str(mentor.text)
    except selenium.common.exceptions.NoSuchElementException:
        mentor = None
    try:
        komentorji = driver.find_elements(By.XPATH, "//span[contains(normalize-space(),'Komentor')]/preceding-sibling::a[1]")
        komentorji = [komentor.text.strip() for komentor in komentorji]
    except selenium.common.exceptions.NoSuchElementException:
        komentorji = None
    ključne_besede_element = driver.find_elements(By.XPATH, "//tr[th[contains(normalize-space(), 'Ključne besede:')]]/td[last()]//a")
    ključne_besede = [ključna_beseda.text.strip() for ključna_beseda in ključne_besede_element]

    leto_disertacije = leto
    try:
        dolzina_element = driver.find_element(By.XPATH, "//tr[th[contains(normalize-space(), 'Št. strani:')]]/td[last()]")
        dolzina = str(dolzina_element.text)
    except selenium.common.exceptions.NoSuchElementException:
        dolzina = "0"
    
    #regex za izluščanje dolžino uvoda in dolžino glavnega dela disertacije. Odločil sem se, da dolžina zaključka ni tako zanimiva.
    vzorec = re.compile(r'([IVXLCDM]+),\s(\d+)')
    dolzina_regex = vzorec.match(dolzina)
    if dolzina_regex:
        dolzina_uvoda = rimske(dolzina_regex.group(1)) if dolzina_regex.group(1) else None
        dolzina_glavnega_dela = int(dolzina_regex.group(2)) if dolzina_regex.group(2) else None
    else:
        dolzina_uvoda = None
        dolzina_glavnega_dela = None

    disertacija = {
        "naslov": naslov_disertacije,
        "avtorji": avtor,
        "mentorji": mentor,
        "komentorji": komentorji,
        "kljucne_besede": ključne_besede,
        "leto": leto_disertacije,
        "jezik": jezik_disertacije,
        "organizacija": organizacija,
        "dolzina_uvoda": dolzina_uvoda,
        "dolzina_glavnega_dela": dolzina_glavnega_dela,
        "ogledi" : st_ogledov,
        "prenosi" : st_prenosov
    }
    return disertacija
čas_začetka = time.time()
leta = [2004, 2009, 2014, 2019, 2024] #leta za pobiranje
for leto in leta:
    pojdi_na_stran_iskanja(rul)
    RUL_iskanje(leto)
    st_zadetkov = zadetki()
    st_strani = ceil(st_zadetkov / 10)
    #print(f"Iskanje za leto {leto} je našlo {st_zadetkov} zadetkov, kar je {st_strani} strani.")
    st_obdelanih = 0
    for stran in range(1, st_strani + 1):
        for zadetek in range(1, 11):
            if st_obdelanih < st_zadetkov:
                WebDriverWait(driver, 10).until(lambda x: x.execute_script("return document.readyState") == "complete")
                disertacije.append(preberi_disertacijo(zadetek, leto))
                driver.back()
                st_obdelanih += 1
            else:
                break
        if stran < st_strani:
            search_url = re.sub(r'(&page=\d+)', '', driver.current_url)
            novi_url = f"{search_url}&page={stran + 1}"
            driver.get(novi_url)

#/html/body/div[4]/section/div/form/table[2]/tbody/tr[1]/td
#/html/body/div[3]/section/div/form/table[2]/tbody/tr[1]/td
    
čas_konca = time.time()
čas_trajanja = čas_konca - čas_začetka
print(f"Čas iskanja: {čas_trajanja} sekund")
print(len(disertacije))
with open('podatki.csv', "w", encoding="utf-8") as f:
    pisatelj = csv.writer(f)
    pisatelj.writerow(
        [
            "Naslov",
            "Avtorji",
            "Mentorji",
            "Komentorji",
            "Ključne besede",
            "Leto",
            "Jezik",
            "Organizacija",
            "Dolžina uvoda",
            "Dolžina glavnega dela",
            "Ogledi",
            "Prenosi",
        ]
    )
    for disertacija in disertacije:
        pisatelj.writerow(
            [
                disertacija["naslov"],
                disertacija["avtorji"],
                disertacija["mentorji"],
                "; ".join(disertacija["komentorji"]) if disertacija["komentorji"] else None,
                "; ".join(disertacija["kljucne_besede"]) if disertacija["kljucne_besede"] else None,
                disertacija["leto"],
                disertacija["jezik"],
                disertacija["organizacija"],
                disertacija["dolzina_uvoda"],
                disertacija["dolzina_glavnega_dela"],
                disertacija["ogledi"],
                disertacija["prenosi"],
            ]
        )
driver.quit()