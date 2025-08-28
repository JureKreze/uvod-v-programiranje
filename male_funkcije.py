import csv

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver


RUL = "https://repozitorij.uni-lj.si/Iskanje.php?type=napredno&lang=slv"
DKUM = "https://dk.um.si/Iskanje.php?type=napredno&lang=slv"


def wait_for_css(
    css_selector: str,
    brskalnik: webdriver,
    timeout: int = 10
) -> WebElement | None:
    '''Čaka, da se element z določenim CSS selektorjem pojavi na strani, potem ga vrne.'''
    try:
        return WebDriverWait(brskalnik, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except selenium.common.exceptions.TimeoutException:
        return None


def wait_for_xpath(
    xpath: str,
    brskalnik: webdriver,
    timeout: int = 10
) -> WebElement | None:
    '''Čaka, da se element z določenim XPATH selektorjem pojavi na strani, potem ga vrne.'''
    try:
        return WebDriverWait(brskalnik, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except selenium.common.exceptions.TimeoutException:
        return None


def pocakaj_stran(
    brskalnik: webdriver,
    timeout: int = 10
) -> None:
    '''Počaka, da se stran naloži.'''
    WebDriverWait(brskalnik, timeout).until(lambda x: x.execute_script("return document.readyState") == "complete")


def RUL_iskanje(
    leto: int,
    brskalnik: webdriver
) -> None:
    '''Na strani za RUL vpiše leto iskanja in poišče.'''
    vnos_leta = wait_for_css("input.IskalniNiz[name='niz3']", brskalnik)
    seznam_vrst_gradiv = brskalnik.find_element(By.CSS_SELECTOR, "#vrsta")
    vnos_leta.clear()
    vnos_leta.send_keys(str(leto))
    select = Select(seznam_vrst_gradiv)
    select.select_by_visible_text("Doktorska disertacija")
    gumb_isci = brskalnik.find_element(By.XPATH, "/html/body/div[3]/section[1]/div/form/table/tbody/tr[7]/td[3]/a")
    gumb_isci.send_keys(Keys.RETURN)

def DKUM_iskanje(
    leto: int,
    brskalnik: webdriver
) -> None:
    '''Na strani za DKUM vpiše leto iskanja in poišče.'''
    vnos_leta = wait_for_css("input.IskalniNiz[name='niz3']", brskalnik)
    seznam_vrst_gradiv = brskalnik.find_element(By.CSS_SELECTOR, "#vrsta")
    vnos_leta.send_keys(str(leto))
    select = Select(seznam_vrst_gradiv)
    select.select_by_visible_text("Doktorska disertacija * (dok)")
    gumb_isci = brskalnik.find_element(
        By.CSS_SELECTOR, "body > div.platno.tex2jax_ignore >\
        section > form > div > table > tbody > tr:nth-child(9)\
        > td:nth-child(2) > input:nth-child(1)"
    )
    gumb_isci.send_keys(Keys.RETURN)


def shrani_disertacije(disertacije: list[dict]) -> None:
    '''Shrani podatke o disertacijah iz RUL v disertacije_lj.csv.'''
    with open("disertacije_lj.csv", "w", newline='', encoding="utf-8") as f:
        pisatelj = csv.writer(f, delimiter="|")
        pisatelj.writerow(
            [
                "ID",
                "Naslov",
                "Avtor",
                "Mentor",
                "Ključne besede",
                "Leto",
                "Jezik",
                "Organizacija",
                "Kraj",
                "Dolžina uvoda",
                "Dolžina glavnega dela",
                "Ogledi",
                "Prenosi",
            ]
        )
        for disertacija in disertacije:
            pisatelj.writerow(
                [
                    disertacija["ID"],
                    disertacija["Naslov"],
                    disertacija["Avtor"],
                    disertacija["Mentor"],
                    disertacija["Ključne besede"],
                    disertacija["Leto izida"],
                    disertacija["Jezik"],
                    disertacija["Organizacija"],
                    disertacija["Kraj izida"],
                    disertacija["dolzina_uvoda"],
                    disertacija["dolzina_glavnega_dela"],
                    disertacija["Število ogledov"],
                    disertacija["Število prenosov"],
                ]
            )


def shrani_disertacije_maribor(disertacije: list[dict]) -> None:
    '''Shrani podatke o disertacijah iz Maribora v disertacije_mb.csv.'''
    with open("disertacije_mb.csv", "w", newline='', encoding="utf-8") as f:
        pisatelj = csv.writer(f, delimiter="|")
        pisatelj.writerow(
            [
                "ID",
                "Naslov",
                "Avtor",
                "Mentor",
                "Ključne besede",
                "Leto",
                "Jezik",
                "Organizacija",
                "Kraj",
                "Ogledi",
                "Prenosi",
            ]
        )
        for disertacija in disertacije:
            pisatelj.writerow(
                [
                    disertacija["ID"],
                    disertacija["Naslov"],
                    disertacija["Avtor"],
                    disertacija["Mentor"],
                    disertacija["Ključne besede"],
                    disertacija["Leto izida"],
                    disertacija["Jezik"],
                    disertacija["Organizacija"],
                    disertacija["Kraj izida"],
                    disertacija["Število ogledov"],
                    disertacija["Število prenosov"],
                ]
            )


def shrani_komentorje(
    disertacije: list[dict],
    stran: int
) -> None:
    '''Shrani podatke o komentorjih disertacij v disertacije_komentorji_{stran}.csv.'''
    with open(f"disertacije_osebe_{stran}.csv", "w", newline='', encoding="utf-8") as f:
        pisatelj = csv.writer(f, delimiter="|")
        pisatelj.writerow(
            [
                "Ime in priimek", #tu bi bilo bolje imeti ID, ker imata 2 osebi lahko enako ime in priimek
            ]
        )
        ze_videni = set()
        for disertacija in disertacije:
            for oseba in disertacija["Komentorji"]:
                if oseba in ze_videni or oseba == "Več o mentorju..." or oseba == "ID":
                    continue
                ze_videni.add(oseba)
                pisatelj.writerow(
                    [
                        oseba,
                    ]
                )
