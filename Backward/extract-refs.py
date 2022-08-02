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
    page = rendering(url)
    soup = BeautifulSoup(page, 'html.parser')
    #### complete code
    '''
    res = soup.find(id='references-section-container')
    res_data = res.find_all('div', class_='col u-px-1')
    refs = []

    for num, i in enumerate(res_data):
        d = i.text
        refs.append(d)

    return refs
    '''

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





if __name__ == "__main__":
    try:
        text = ''
        filepath = Path('links.txt')
        # create the file if it doesn't exist
        filepath.touch(exist_ok=True)
        with open('links.txt', 'r') as f:
            text = f.read()
            f.close()
            
        links = text.split('\n')
        url = input("Enter url: ")
        res =''; nurl=''
        if "acm" not in url:
            res = urllib.request.urlopen(url)
            nurl = res.geturl()
        
        if url not in links:
            refs = []
            if (nurl.find('ieee')!=-1):
                refs = ieee(url)
            elif (nurl.find('.pdf')!=-1): # better than before
                refs = pdfextract(url)
            elif (nurl.find('springer')!=-1): 
                refs = springer(url)
            elif (url.find('acm')!=-1):
                refs = acm(url)
            elif (url.find('elsevier')!=-1):
                refs = elsevier(url)

            df = pd.DataFrame(refs)
            # append the references
            if not os.path.isfile('References.csv'):
               df.to_csv('References.csv', index=False, header=["References"])
            else: 
               df.to_csv('References.csv', mode='a',index=False, header=False)

            # append the link
            with open('links.txt', 'a') as fd:
                fd.write(url+'\n')  # includes the original url, not redirected one

                
        else:
            print("Link exists! References already extracted.")
        
    except HTTPError as e:
        print("HTTPError. Can't extract references.")
        traceback.print_exc()

