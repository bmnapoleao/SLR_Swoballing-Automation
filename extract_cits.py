import requests

import os
import time

import pandas as pd
from semanticscholar import SemanticScholar
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException



##---CONSTANTS---##
BASE_URL = 'http://dx.doi.org/'
crossref = 'https://search.crossref.org/references'
zotero = 'https://zbib.org/'



# extract dois for websites
def doi_helper(refs):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(crossref)                                          
    time.sleep(3)
    
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
                    dois.append(a.text) 
                except NoSuchElementException:
                    print("Element not found")
        else:
            dois.append("No doi") # non-dois  

    driver.quit()
    return dois


def search_sscholar(doi):
    sch = SemanticScholar(timeout=2)
    length = 16
    
    if "http://dx.doi.org" in doi:
        length = 18
    elif "https://dx.doi.org" in doi:
        length = 19
    elif "https://doi.org" in doi:
        length = 16
    elif "http://doi.org" in doi:
        length = 15
    paper = sch.paper(doi[length:]) # to remove the url part
    return paper


# get the citations to the papers
def search_cites(paper):
    citations = []
    refs = []
    all_refs = []
    
    papers = paper['citations']
    for i in range(len(papers)):
        reference = ''
        aut = papers[i]['authors']
        for j in range(len(aut)):
            reference += aut[j]['name']
            reference += ', '
        reference += '"' + papers[i]['title'] + '", ' + papers[i]['venue'] + ', ' + str(papers[i]['year']) + '.'
        all_refs.append(reference)
        
        if papers[i]['doi']:
            citations.append(BASE_URL + papers[i]['doi'])
            
        else:
            refs.append(reference)
            
    # search for doi if not there
    if refs:
        new_dois = doi_helper(refs)
        citations = citations + new_dois
    #print(len(citations),len(all_refs))
    return citations, all_refs




# get the reference of a paper
def get_refs(paper):
    #refs = []
    
    reference = ''
    aut = paper['authors']
    for j in range(len(aut)):
        reference += aut[j]['name']
        reference += ', '
    reference += '"' + paper['title'] + '", ' + paper['venue'] + ', ' + str(paper['year']) + '.'
    
    time.sleep(3)
    #refs.append(reference)
        
    return reference


