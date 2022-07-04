import time
import sys
import urllib.request
from urllib.error import HTTPError
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


crossref = 'https://search.crossref.org/references'
doi2bib = 'https://www.doi2bib.org/'
BASE_URL = 'http://dx.doi.org/'

#options = webdriver.ChromeOptions()
#options.add_argument('--headless') 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


#-----Part 1------#

driver.get(crossref)                                          
time.sleep(3)                                            

#read csv file for references
ieee = pd.read_csv("ieee.csv")
refs = ieee['References'][:5] # references
refstring = ''
for i in refs:
    refstring += i.replace('\n',' ')
    refstring += '\n'

#input refstring in text area
textarea = driver.find_element(By.NAME, "references")
textarea.send_keys(refstring)
button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/form/div/div/button")
button.click()


dois = []
bibs = []
# goes to results page
mytable = driver.find_element(By.CLASS_NAME,'table.table-striped')
for row in mytable.find_elements(By.TAG_NAME,'tr'):
    elecell = row.find_elements(By.TAG_NAME,'td')
    if len(elecell)==1:
        for cell in elecell:
            try:
                a = cell.find_element(By.TAG_NAME, 'a')
                dois.append(a.text[16:]) # dois
            except NoSuchElementException:
                print("Element not found")
    else:
        dois.append("Doesn't have doi") # non-dois
print(dois)

#----Part 2------#

# Below code Credits: @ https://scipython.com/blog/doi-to-bibtex/                                          
# fetch bib of each doi
for doi in dois:
    if not (doi ==  "Doesn't have doi"):
        url = BASE_URL + doi
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        try:
            with urllib.request.urlopen(req) as f:
                bibtex = f.read().decode()
            print(bibtex)
        except HTTPError as e:
            if e.code == 404:
                print('DOI not found.')
            else:
                print('Service unavailable.')
            sys.exit(1)

'''

#get abstract
resgate = 'https://www.researchgate.net/search.Search.html?type=publication&query='

for i,doi in enumerate(dois):
    
    req = requests.get(resgate + doi)
    soup = BeautifulSoup(req.text,'html.parser')

<div class="nova-legacy-e-expandable-text__container">
'''
driver.quit()




