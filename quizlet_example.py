from sys import argv as argv
import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time

pyautogui.FAILSAFE = True


if len(argv) == 2:
    set_code = argv[1]
else:
    set_code = "248827408"

# read through terms and get info
def parse_for_data():
    term_child_lines = [x.children for x in vocab_html.find_all("div", class_="SetPageTerm-wordText")]
    terms = []
    for children in term_child_lines:
        for child in children:
            terms.append(child.text.replace("'",""))
    definition_child_lines = [x.children for x in vocab_html.find_all("div", class_="SetPageTerm-definitionText")]
    definitions = []
    for children in definition_child_lines:
        for child in children:
            definitions.append(child.text.replace("'",""))

    term_def = []

    for index in range(len(terms)):
        term_def.append((terms[index], definitions[index]))
    return term_def

vocab_html = soup(requests.get("https://quizlet.com/" + set_code).content, "lxml")

term_def_list = parse_for_data()

#### at this point ALL term def info is connected as tuples in term_def_list




#initialize selenium chrome web
chrome_options = Options()
chrome_options.add_argument("--window-size=980,1080")
browser = webdriver.Chrome(chrome_options=chrome_options)

def log_in():
    pass

def parse_match_space(source):
    tile_html = soup(source.replace("'",""), "lxml")
    tiles = [x.text for x in tile_html.find_all("div", style="display: block;")]
    return tiles

def find_related_tile(original):
    for pair in term_def_list:
        if pair[0] == original:
            term_def_list.remove(pair)
            return pair[1]
        elif pair[1] == original:
            term_def_list.remove(pair)
            return pair[0]





def match_tiles():
    browser.get("https://quizlet.com/" + set_code + "/match")
    browser.find_element_by_css_selector('.UIButton.UIButton--hero').click()

    time.sleep(0.1)
    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[style="display: block;"]')))

    tiles = parse_match_space(browser.page_source)
    for element in browser.find_elements_by_css_selector('div[style="display: block;"]'):
        browser.execute_script("arguments[0].innerHTML = arguments[0].innerHTML.replace(\"'\", \"\");" , element)

    for pair_index in range(len(tiles) // 2):

        first_tile = tiles[0]
        wait = WebDriverWait(browser, 10)
        first_x_path = "//*[contains(text(), \"" + first_tile + "\")]"
        wait.until(EC.presence_of_element_located((By.XPATH, first_x_path))).click()


        second_tile = find_related_tile(first_tile)
        wait = WebDriverWait(browser, 10)
        second_x_path = "//*[contains(text(), \"" + second_tile + "\")]"
        wait.until(EC.presence_of_element_located((By.XPATH, second_x_path))).click()


        #browser.execute_script("document.evaluate('arguments[0]', document, null, XPathResult.ANY_TYPE, null).single_node.remove();", first_x_path)
        #browser.execute_script("document.evaluate('arguments[0]', document, null, XPathResult.ANY_TYPE, null).remove();", second_x_path)
        tiles.remove(first_tile)
        tiles.remove(second_tile)






    time.sleep(4)
    browser.quit()


match_tiles()
