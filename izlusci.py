import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from roman import fromRoman as rimske
from selenium.webdriver.common.keys import Keys

def preberi_disertacijo(n, leto, brskalnik):
    disertacija = dict()
    naslov = brskalnik.find_element(By.CSS_SELECTOR, f"body > div.platno > section.zadetki > div > table > tbody > tr:nth-child({n}) > td > div > a:nth-child(2)")

    #body > div.platno > section.zadetki > div > table > tbody > tr:nth-child(1) > td > div > a:nth-child(2) je selektor za link do prve disertacije
    #body > div.platno > section.zadetki > div > table > tbody > tr:nth-child(2) > td > div > a:nth-child(2) je selektor za link do druge disertacije
    #sklepamo, da je selektor za n-to disertacijo zgoraj napisan v "naslov"
    naslov_disertacije = str(naslov.text)
    disertacija["Naslov"] = naslov_disertacije
    naslov.send_keys(Keys.RETURN)
    disertacija["Leto izida"] = leto
    povezava = brskalnik.current_url
    vzorec_id = re.compile(r'id=([1-9]+)')
    id = vzorec_id.search(povezava).group(1)
    disertacija["ID"] = id
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
        try:
            stvar_element = brskalnik.find_element(By.XPATH, f"//tr[th[contains(normalize-space(), '{stvar}:')]]/td[last()]")
        except NoSuchElementException:
            stvar_element = None
        disertacija[stvar] = stvar_element.text.strip() if stvar_element else None
    for oseba in osebe_za_iskati:
        try:
            oseba_element = brskalnik.find_element(By.XPATH, f"//span[contains(normalize-space(), '{oseba}')]/preceding-sibling::a[1]")
        except NoSuchElementException:
            oseba_element = None
        if oseba_element:
            disertacija[oseba] = str(oseba_element.text.strip())
        else:
            disertacija[oseba] = None
    try:
        komentorji_elementi = brskalnik.find_elements(By.XPATH, "//span[contains(normalize-space(), 'Komentor')]/preceding-sibling::a")
        komentorji = [str(komentor.text.strip()) for komentor in komentorji_elementi]
    except NoSuchElementException:
        komentorji = []
    disertacija["Komentorji"] = komentorji if komentorji else []

    try:
        dolzina_element = brskalnik.find_element(By.XPATH, "//tr[th[contains(normalize-space(), 'Št. strani:')]]/td[last()]")
        dolzina = str(dolzina_element.text)
    except NoSuchElementException:
        dolzina = "0"
    
    #regex za izluščanje dolžino uvoda in dolžino glavnega dela disertacije. Odločil sem se, da dolžina zaključka ni tako zanimiva.
    vzorec = re.compile(r'([IVXLCDM]+),\s(\d+)')
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