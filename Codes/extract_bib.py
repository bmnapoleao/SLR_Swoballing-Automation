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




#---CONSTANTS---#
crossref = 'https://search.crossref.org/references'
BASE_URL = 'http://dx.doi.org/'
researchgate = 'https://www.researchgate.net/login'

# dummy login creds - institutional account
USERNAME = 'rsarkar@etu.uqac.ca'
PASSWORD = 'rK.p)z_=Gs2Y6e6'

##---CONSTANTS END---##



#----Part 1----#
# Extract bibtex having abstract from websites

def runieee(doi,page):
    page.goto(doi,timeout=0)
    
    try:
        page.click('button[class="layout-btn-white cite-this-btn"]', timeout=15000)
        time.sleep(2)
        page.locator('div[class="browse-pub-tab"]', has_text="BibTeX").click()
        page.locator('input[type="checkbox"]').click()
        time.sleep(3)
        page.locator('a[class="stats-Cite_This_Doc_Details_Copy"]', has_text="Copy").click() # copying clipboard
        time.sleep(3)
        b = pyperclip.paste() # pasting clipboard
        return b
    
    except Exception:
        return "No bib"


'''
# doesn't reach this function because of 403 error
def runacm(doi,page):
    page.goto(doi,timeout=0)
    try:
        page.click('a[data-title="Export Citation"]', timeout=15000)
        time.sleep(3)
        page.select_option('select#citation-format', label='BibTeX')
        page.locator('a[title="Copy citation"]', has_text="Copy citation").click() # copying clipboard
        time.sleep(3)
        b = pyperclip.paste() # pasting clipboard
        return b
    
    except Exception:
        return "No bib"
'''


def runspringer(doi,page):
    page.goto(doi,timeout=0)
    # Below code credits @https://github.com/microsoft/playwright-python/issues/528 #
    try:
        with page.expect_download() as download_info:
            page.locator('a[data-test="citation-link"]', has_text=".BIB", timeout=15000).click()

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
        return "No bib"

'''
# doesn't reach this function because of 403 error
def runsciencedirect(doi,page):
    page.goto(doi,timeout=0)
    try:
        page.locator('button[class="button button-anchor"]', has_text="Cite", timeout=0).click()
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
        return "No bib"

'''


def extract_bib_abs(dois, direc, cell_indices):
    bibs = []
    ref = pd.read_csv(direc)
    b = ""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

        for j,doi in enumerate(dois):
            i = cell_indices[j]
            if not (doi=="No doi"):
                try:
                    
                    #print(i,doi)
                    res = urllib.request.urlopen(doi)
                    nurl = res.geturl()
                    if ("pdf" in nurl):
                        b = extract_only_bib(doi,ref,i)
                        
                    #elif ("ieee" in nurl):
                     #   b = runieee(doi,page)
                            
                    #elif ("springer" in nurl):
                     #   b = runspringer(doi,page)
                            
                    #elif ("elsevier" in nurl):
                     #   b = runsciencedirect(doi,page)
                        
                    else:
                        b = "Not standard"



                        
                    if b == "No bib":
                        bibs.append(extract_only_bib(doi,ref,i))
                        
                    elif b == "Not standard":
                        bibs.append(extract_only_bib(doi,ref,i))
                        
                    else:
                        bibs.append(b)
                        ref.loc[i,'Status'] = "Extraction successful" 
                        
                    time.sleep(7)
                    #print(bibs[i]+"\n")

                except:
                    bibs.append(extract_only_bib(doi,ref,i))
                    #traceback.print_exc()

                finally:
                    continue
            else:
                bibs.append("No doi")
                

        with open(direc,'w', encoding = "utf-8",newline='') as f:
            ref.to_csv(f, index=False)     
        browser.close()
       
        return bibs


##----Part 1 END----##




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
                print('bibtex found: ',doi)
                return bibtex
            
        except:
            ref.loc[i,'Status'] = "BIB not found" 
            return "No bib"
        
        finally:
            time.sleep(3)
            
# Credits end
##---Part 2 END---##



#----Part 3------#
# Get abstract from researchgate
def extract_abs_also(dois, bibs, direc, n_iter, cell_indices,snowtype):
    ref = pd.read_csv(direc)
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
        
        for j,doi in enumerate(dois):
            i = cell_indices[j]
            #print(i,doi)
            stat = ref.loc[i,'Status']
            #print(stat)
            if stat not in ["DOI not found","Extraction successful","BIB not found"]:
                page.goto(f"https://www.researchgate.net/search.Search.html?type=publication&query={doi}", timeout=0)
                
                selector = Selector(text=page.content())
                abstract = selector.css(".nova-legacy-e-expandable-text__container div::text").get() # extract abstract

                bib = bibtexparser.loads(bibs[j])
                #print(bib.entries)
                try:
                    if abstract and len(abstract)>3:
                        bib.entries[0]['abstract'] = abstract # update in bib
                        ref.loc[i,'Status'] = "Extraction successful"
                        
                    else:
                        bib.entries[0]['abstract'] = "" # update in bib
                        ref.loc[i,'Status'] = "Abstract not found"
                except:
                    print("Cannot parse bibtex")
                    ref.loc[i,'Status'] = "Cannot parse bibtex"
                db.entries += bib.entries  # update db

            elif stat == "Extraction successful":
                #print(bibs)
                bib = bibtexparser.loads(bibs[j])
                db.entries += bib.entries  # update db
                
            ref.loc[i,'Iteration'] = n_iter
            time.sleep(3)
            
        with open(direc,'w', encoding = "utf-8",newline='') as f:
            ref.to_csv(f, index=False)
        browser.close()
        

        filename = 'allbibs-'+snowtype+'.bib'
        # append all bibtex in 1 bib file
        if not os.path.isfile(filename):
            with open(filename, 'w+', encoding = "utf-8") as bibtex_file:
                bibtexparser.dump(db, bibtex_file)
        else: 
            with open(filename, 'a', encoding = "utf-8") as bibtex_file:
                bibtexparser.dump(db, bibtex_file)


                
##---Part 3 END---##


