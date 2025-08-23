from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium

def wait_for_css(css_selector, brskalnik, timeout=10):
    try:
        return WebDriverWait(brskalnik, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except selenium.common.exceptions.TimeoutException:
        return None
#def wait_for_xpath(xpath, brskalnik, timeout=10):
#    try:
#        return WebDriverWait(brskalnik, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
#    except selenium.common.exceptions.TimeoutException:
#        return None
def pocakaj_stran(brskalnik, timeout=10):
    WebDriverWait(brskalnik, 10).until(lambda x: x.execute_script("return document.readyState") == "complete")