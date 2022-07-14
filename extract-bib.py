import time
import sys
import json
import urllib.request
from urllib.error import HTTPError
import requests
import pandas as pd

from parsel import Selector
from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


crossref = 'https://search.crossref.org/references'
doi2bib = 'https://www.doi2bib.org/'
BASE_URL = 'http://dx.doi.org/'
researchgate = 'https://www.researchgate.net/login'

# dummy login creds - institutional account
USERNAME = 'rsarkar@etu.uqac.ca'
PASSWORD = 'rK.p)z_=Gs2Y6e6'


#options = webdriver.ChromeOptions()
#options.add_argument('--headless') 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


#-----Part 1------#

driver.get(crossref)                                          
time.sleep(3)                                            

#read csv file for references
ieee = pd.read_csv("springer.csv")
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
                dois.append(a.text) # dois [16:] - to remove the url part
            except NoSuchElementException:
                print("Element not found")
    else:
        dois.append("No doi") # non-dois
print(dois)

driver.quit() ####remove in the end

'''
#----Part 1.1----#
# Extract abstract from bibtex of websites

def runieee(doi,page):
    page.goto(researchgate,timeout=0)
    page.click('button[class="layout-btn-white cite-this-btn"]')        
    

def runacm(doi,page):
    


def runspringer(doi,page):
    


def runsciencedirect(doi,page):
    


### httperror 503 wiley (not in researchgate)





with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

    for doi in dois:
        if not (doi=="No doi"):
            try:
                res = urllib.request.urlopen(url)
                nurl = res.geturl()
                if ("ieee" in nurl):
                    runieee(doi,page)
                elif ("acm" in nurl):
                    runacm(doi,page)
                elif ("springer" in nurl):
                    runspringer(doi,page)
                #elif ("wiley" in nurl):
                #    runwiley(doi)
                elif ("elsevier" in nurl):
                    runsciencedirect(doi,page)

        except HTTPError:
            continue
            

'''



#----Part 2------#

# Below code Credits: @ https://scipython.com/blog/doi-to-bibtex/                                          
# fetch bib of each doi
# "No doi found" - for papers wothout doi, add a column
for doi in dois:
    if not (doi ==  "No doi"):
        url = BASE_URL + doi
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        try:
            with urllib.request.urlopen(req) as f:
                bibtex = f.read().decode()
            print(bibtex)
        except HTTPError as e:
            if e.code == 404:
                print('BIB not found.')
            else:
                print('Service unavailable.')
            

# Credits end
driver.quit()



#----Part 3------#
# Get abstract from researchgate


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")

    page.goto(researchgate,timeout=0)
    #page.click('text=Login')
    page.fill('input[name="login"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type=submit]')

 
    for doi in dois:
        if not (doi=="No doi"):
            page.goto(f"https://www.researchgate.net/search.Search.html?type=publication&query={doi}", timeout=0)
            #https://www.mendeley.com/search/?page=1&query=10.1049/el:20000242&sortBy=relevance
            #https://www.researchgate.net/search.Search.html?type=publication&query=10.1049/el:20000242
            selector = Selector(text=page.content())
            
            print(selector.css(".nova-legacy-e-expandable-text__container div::text").get())
            print(selector.css(".ArticleCardTitle__TitleButton-sc-1jkrcs4-2 span::text").get())
            
            #page.click(".ArticleCard__StyledArticleCard-sc-7btn0d-0")
            #print(selector.css(".ArticleCardTitle__TitleLink-sc-1jkrcs4-1::text").get())
            #print(selector.css(".ArtiscleCardAbstract__Abstract-sc-8nze5h-0 jlJEmQ ArticleAbstract__Abstract-sc-1gl3y52-0 hLUoOT qe-abstract::text").get())
            
            #print(selector.css(".nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-xs nova-legacy-e-text--color-inherit::text").get())
            
            #nova-legacy-e-expandable-text__container
            for author in selector.css(".nova-legacy-c-card__body--spacing-inherit"):
                name = author.css(".nova-legacy-v-person-item__title a::text").get()
                thumbnail = author.css(".nova-legacy-v-person-item__image img::attr(src)").get()
                profile_page = f'https://www.researchgate.net/{author.css("a.nova-legacy-c-button::attr(href)").get()}'
                institution = author.css(".nova-legacy-v-person-item__stack-item:nth-child(3) span::text").get()
                department = author.css(".nova-legacy-v-person-item__stack-item:nth-child(4) span").xpath("normalize-space()").get()
                skills = author.css(".nova-legacy-v-person-item__stack-item:nth-child(5) span").xpath("normalize-space()").getall()
                last_publication = author.css(".nova-legacy-v-person-item__info-section-list-item .nova-legacy-e-link--theme-bare::text").get()
                last_publication_link = f'https://www.researchgate.net{author.css(".nova-legacy-v-person-item__info-section-list-item .nova-legacy-e-link--theme-bare::attr(href)").get()}'
                '''
                authors.append({
                    "name": name,
                    "profile_page": profile_page,
                    "institution": institution,
                    "department": department,
                    "thumbnail": thumbnail,
                    "last_publication": {
                        "title": last_publication,
                        "link": last_publication_link
                    },
                    "skills": skills,
                })
                '''

    browser.close()


#----Part 4------#

#save the doi and bib and abstract in json
#https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file


