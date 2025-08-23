from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from cakalne_funckije import wait_for_css
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=chrome_options)

rul = "https://repozitorij.uni-lj.si/Iskanje.php?type=napredno&lang=slv"
dkum = "https://dk.um.si/Iskanje.php?type=napredno&lang=slv"

def RUL_iskanje(leto, brskalnik):
    vnos_leta = wait_for_css("input.IskalniNiz[name='niz3']", brskalnik)
    seznam_vrst_gradiv = brskalnik.find_element(By.CSS_SELECTOR, "#vrsta")
    vnos_leta.send_keys(str(leto))
    select = Select(seznam_vrst_gradiv)
    select.select_by_visible_text("Doktorska disertacija")
    gumb_isci = brskalnik.find_element(By.XPATH, "/html/body/div[3]/section[1]/div/form/table/tbody/tr[7]/td[3]/a")
    gumb_isci.send_keys(Keys.RETURN)

def DKUM_iskanje(leto, brskalnik):
    vnos_leta = wait_for_css("input.IskalniNiz[name='niz3']", brskalnik)
    seznam_vrst_gradiv = brskalnik.find_element(By.CSS_SELECTOR, "#vrsta")
    vnos_leta.send_keys(str(leto))
    select = Select(seznam_vrst_gradiv)
    select.select_by_visible_text("Doktorska disertacija")
    gumb_isci = brskalnik.find_element(By.XPATH, "/html/body/div[2]/section/form/div/table/tbody/tr[9]/td[2]/input[1]")
    gumb_isci.send_keys(Keys.RETURN)

driver.get(dkum)
DKUM_iskanje(2010, driver)