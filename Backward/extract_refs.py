# imports
import os
import time
import re
import csv
import pandas as pd
import requests
import urllib.request
from pathlib import Path
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from parsel import Selector
from playwright.sync_api import sync_playwright

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import fitz # for pdf extraction

import traceback


# extraction functions
def rendering(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)                                         
    time.sleep(3)                                            
    render = driver.page_source                              
    driver.quit()                                            
    return render                                            


def ieee(url):
    #url = 'https://ieeexplore.ieee.org/document/7750588'
    page = rendering(url)
    soup = BeautifulSoup(page, 'html.parser')
    res = soup.find(id='references-section-container')
    res_data = res.find_all('div', class_='col u-px-1')
    refs = []

    for num, i in enumerate(res_data):
        d = i.text
        refs.append(d)

    return refs


def elsevier(url):
    #url = 'https://www.sciencedirect.com/science/article/pii/S0360319921039422'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50) #doesn't work if headless
        page = browser.new_page()

        page.goto(url)
        time.sleep(3)
        r = page.locator('dd[class="reference"]')
        c = r.count()
        #print(c)
        refs = []
        
        for i in range(c):
             text = r.nth(i).inner_text()
             refs.append(text)

        return refs

    

def pdfextract(url):
    #url = 'https://arxiv.org/pdf/2007.07751.pdf'
    #url = 'http://ksiresearchorg.ipage.com/seke/seke17paper/seke17paper_69.pdf' 
    r = requests.get(url, stream = True)
    with open('metadata.pdf', 'wb') as f:
        f.write(r.content)

    if os.path.exists("metadata.pdf"):
        text = ""
        with fitz.open('metadata.pdf') as doc:
            for page in doc:
                text += page.get_text()
        
        tlow  = text.lower()
        index = tlow.rfind('references')
        
        refs = []
        if (index != -1):
            text1 = text[index+11:]
            s1 = "\[\d+"
            result = [_.start() for _ in re.finditer(s1, text1)]
            strlist = [text1[i:j] for i,j in zip(result, result[1:]+[None])]
            for j in strlist:
                j = j.replace('-\n','')
                j = j.split('\n')
                j = " ".join(j)    
                index1 = j.rfind(".")
                refs.append(j[:index1+1])
        
        os.remove('metadata.pdf')
        return refs



def springer(url):
    #url = 'https://link.springer.com/article/10.1007/s11696-022-02290-1'
    sess = HTMLSession()
    r = sess.get(url)

    r.html.render()
    refer = r.html.find('.c-article-references__text')
    refs = []

    for num, i in enumerate(refer):
        d = i.text
        refs.append(d)

    return refs    
      



def acm(url):
    # url = 'https://dl.acm.org/doi/10.1109/34.824822'
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'html.parser')
    tlow  = req.text.lower()
    if tlow.rfind('references')!=-1:
        res_data = soup.find_all("span", class_="references__note")
        refs = []

        for num, i in enumerate(res_data):
            d = i.text
            refs.append(d)

        return refs

