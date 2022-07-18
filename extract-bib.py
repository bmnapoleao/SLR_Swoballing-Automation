# imports
import os
import time
import sys
import pandas as pd
import pyperclip
import traceback

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

import requests
import urllib.request
from urllib.error import HTTPError

from parsel import Selector
from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException



#---CONSTANTS---#
crossref = 'https://search.crossref.org/references'
doi2bib = 'https://www.doi2bib.org/'
BASE_URL = 'http://dx.doi.org/'
researchgate = 'https://www.researchgate.net/login'

# dummy login creds - institutional account
USERNAME = 'rsarkar@etu.uqac.ca'
PASSWORD = 'rK.p)z_=Gs2Y6e6'

##---CONSTANTS END---##



#-----Part 1------#

def extract_dois():

    #options = webdriver.ChromeOptions() #### uncomment at the end
    #options.add_argument('--headless')  #### uncomment at the end

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(crossref)                                          
    time.sleep(3)                                            

    #read csv file for references
    ref = pd.read_csv("References.csv")
    ref['Status'] = ""
    refs = ref['References'] 
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
    # goes to results page
    mytable = driver.find_element(By.CLASS_NAME,'table.table-striped')
    for i,row in enumerate(mytable.find_elements(By.TAG_NAME,'tr')):
        elecell = row.find_elements(By.TAG_NAME,'td')
        if len(elecell)==1:
            for cell in elecell:
                try:
                    a = cell.find_element(By.TAG_NAME, 'a')
                    dois.append(a.text) # dois [16:] - to remove the url part
                except NoSuchElementException:
                    print("Element not found")
        else:
            dois.append("No doi") # non-dois
            ref.loc[i-1,'Status'] = "DOI not found" # i-1 because 1st element(the heading) is skipped

    driver.quit()
    ref.to_csv('References.csv',index=False)

    return dois

##----Part 1 END----##



#----Part 1.1----#
# Extract bibtex having abstract from websites

def runieee(doi,page):
    page.goto(doi,timeout=0)
    page.click('button[class="layout-btn-white cite-this-btn"]')
    time.sleep(3)
    try:
        page.locator('div[class="browse-pub-tab"]', has_text="BibTeX").click()
        page.locator('input[type="checkbox"]').click()
        time.sleep(3)
        page.locator('a[class="stats-Cite_This_Doc_Details_Copy"]', has_text="Copy").click() # copying clipboard
        time.sleep(3)
        b = pyperclip.paste() # pasting clipboard
        return b
    except Exception:
        #print("No bib in ieee page")
        return "No bib"

def runacm(doi,page):
    page.goto(doi,timeout=0)
    try:
        page.click('a[data-title="Export Citation"]')
        time.sleep(3)
        page.select_option('select#citation-format', label='BibTeX')
        page.locator('a[title="Copy citation"]', has_text="Copy citation").click() # copying clipboard
        time.sleep(3)
        b = pyperclip.paste() # pasting clipboard
    except Exception:
        #print("No bib in acm page")
        return "No bib"


def runspringer(doi,page):
    page.goto(doi,timeout=0)
    # Below code credits @https://github.com/microsoft/playwright-python/issues/528 #
    try:
        with page.expect_download() as download_info:
            page.locator('a[data-test="citation-link"]', has_text=".BIB").click()

        download = download_info.value
        path = download.path()
    ## Credits end ##
    
        if os.path.exists(path):
            with open(path, 'r') as f:
                b = f.read()
                return b
        else:
            return "No bib"
    except Exception:
        #print("No bib in springer page")
        return "No bib"


def runsciencedirect(doi,page):
    page.goto(doi,timeout=0)
    try:
        page.locator('button[class="button button-anchor"]', has_text="Cite").click()
        time.sleep(3)
        with page.expect_download() as download_info:
            page.locator('button[class="button button-anchor u-padding-0"]', has_text="Export citation to BibTeX").click()

        download = download_info.value
        path = download.path()
       
        if os.path.exists(path):
            with open(path, 'r') as f:
                b = f.read()
                return b
        else:
            return "No bib"
    except Exception:
        #print("No bib in elsevier page")
        return "No bib"




def extract_bib_abs(dois):
    bibs = []
    ref = pd.read_csv("References.csv")
    b = ""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

        for i,doi in enumerate(dois):
            if not (doi=="No doi"):
                try:
                    res = urllib.request.urlopen(doi)
                    nurl = res.geturl()
                    if ("ieee" in nurl):
                        b = runieee(doi,page)
                            
                    elif ("springer" in nurl):
                        b = runspringer(doi,page)
                            
                    elif ("elsevier" in nurl):
                        b = runsciencedirect(doi,page)
                        
                    else:
                        b = extract_only_bib(doi,ref,i)

                        
                    if b == "No bib":
                        bibs.append(extract_only_bib(doi,ref,i))
                    else:
                        bibs.append(b)
                        ref.loc[i,'Status'] = "Extraction successful" 
                        
                    time.sleep(1)

                except HTTPError as e:
                    if e.code == 403:
                        b = runacm(doi,page)
                        
                        if b == "No bib":
                            bibs.append(extract_only_bib(doi,ref,i))
                        else:
                            bibs.append(b)
                            ref.loc[i,'Status'] = "Extraction successful" 
                    else:
                        print("HTTPError")
                        bibs.append(extract_only_bib(doi,ref,i))
                        #traceback.print_exc()
                    continue
            else:
                bibs.append("No doi")
                
        browser.close()
        ref.to_csv('References.csv',index=False)
        return bibs


##----Part 1.1 END----##



#----Part 2------#

# Below code Credits: @ https://scipython.com/blog/doi-to-bibtex/
# fetch bib of each doi
def extract_only_bib(doi,ref,i):
    
    if not (doi ==  "No doi"):
        url = doi
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        try:
            with urllib.request.urlopen(req) as f:
                bibtex = f.read().decode()
                return bibtex
            
        except HTTPError as e:
            if e.code == 404:
                ref.loc[i,'Status'] = "BIB not found" 
                return "No bib"
            else:
                print('Service unavailable.')
                return "No bib"
            
# Credits end
##---Part 2 END---##



#----Part 3------#
# Get abstract from researchgate
def extract_abs_also(dois, bibs):
    ref = pd.read_csv("References.csv")
    abstract = ""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

        # Login to researchgate
        page.goto(researchgate,timeout=0)
        page.fill('input[name="login"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('button[type=submit]')

        db = BibDatabase()
        bib = ''
        
        for i,doi in enumerate(dois):
            stat = ref.loc[i,'Status']
            #print(stat)
            if stat not in ["DOI not found","Extraction successful","BIB not found"]:
                page.goto(f"https://www.researchgate.net/search.Search.html?type=publication&query={doi}", timeout=0)
                
                selector = Selector(text=page.content())
                abstract = selector.css(".nova-legacy-e-expandable-text__container div::text").get() # extract abstract

                bib = bibtexparser.loads(bibs[i])
                #print(bib.entries)
                if abstract:
                    bib.entries[0]['abstract'] = abstract # update in bib
                    ref.loc[i,'Status'] = "Extraction successful"
                    
                else:
                    bib.entries[0]['abstract'] = "" # update in bib
                    ref.loc[i,'Status'] = "Abstract not found"
                db.entries += bib.entries  # update db

            elif stat == "Extraction successful":
                bib = bibtexparser.loads(bibs[i])
                db.entries += bib.entries  # update db
                
            

        browser.close()
        ref.to_csv('References.csv',index=False)

        # store all bibtex in 1 bib file
        with open('allbibs.bib', 'w+', encoding = "utf-8") as bibtex_file:
            bibtexparser.dump(db, bibtex_file)
    
##---Part 3 END---##




if __name__ == "__main__":

    dois = extract_dois()
    #print(dois)
    bibs = extract_bib_abs(dois)
    print(len(bibs),len(dois))
    extract_abs_also(dois,bibs) 
    
    # Rename References.csv
    try:
        os.rename("References.csv", "References-updated.csv")
    except OSError as exc:
        print(f'WARNING: could not rename References : {exc}')
    
