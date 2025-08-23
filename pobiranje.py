import re
import shrani
import threading
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from cakalne_funckije import wait_for_css, pocakaj_stran
from iskanje import RUL_iskanje, rul
from math import ceil
from izlusci import preberi_disertacijo

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works

disertacije = list()

def zadetki(brskalnik):
    st_zadetkov_css = wait_for_css(".StZadetkov", brskalnik)
    st_zadetkov_tekst = st_zadetkov_css.text
    st_zadetkov = int(st_zadetkov_tekst.split(" ")[0])
    return st_zadetkov

čas_začetka = time.time()
def poberi(brskalnik, leta_za_pobiranje):
    for leto in leta_za_pobiranje:
        brskalnik.get(rul)
        pocakaj_stran(brskalnik)
        RUL_iskanje(leto, brskalnik)
        st_zadetkov = zadetki(brskalnik)
        st_strani = ceil(st_zadetkov / 10)
        #print(f"Iskanje za leto {leto} je našlo {st_zadetkov} zadetkov, kar je {st_strani} strani.")
        st_obdelanih = 0
        for stran in range(1, st_strani + 1):
            for zadetek in range(1, 11):
                if st_obdelanih < st_zadetkov:
                    pocakaj_stran(brskalnik)
                    try:
                        disertacije.append(preberi_disertacijo(zadetek, leto, brskalnik))
                    except NoSuchElementException:
                        break
                    brskalnik.back()
                    st_obdelanih += 1
                else:
                    break
            if stran < st_strani:
                search_url = re.sub(r'(&page=\d+)', '', brskalnik.current_url)
                novi_url = f"{search_url}&page={stran + 1}"
                brskalnik.get(novi_url)

def delavec(leta_za_pobiranje):
    driver_thread = webdriver.Chrome(options=chrome_options)
    try:
        poberi(driver_thread, leta_za_pobiranje)
    finally:
        driver_thread.quit()

leta1 = [2000, 2001, 2002, 2003, 2004, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013]
leta2 = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

thread1 = threading.Thread(target=delavec, args=(leta1,))
thread2 = threading.Thread(target=delavec, args=(leta2,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()  

#/html/body/div[4]/section/div/form/table[2]/tbody/tr[1]/td
#/html/body/div[3]/section/div/form/table[2]/tbody/tr[1]/td
čas_konca = time.time()
čas_trajanja = čas_konca - čas_začetka
print(f"Čas iskanja: {čas_trajanja} sekund")
print(len(disertacije))
shrani.shrani_disertacije(disertacije)
shrani.shrani_komentorje(disertacije)
