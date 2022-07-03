import os
import time
import re
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import fitz



def rendering(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)                                          # load the web page from the URL
    time.sleep(3)                                            # wait for the web page to load
    render = driver.page_source                              # get the page source HTML
    driver.quit()                                            # quit ChromeDriver
    return render                                            # return the page source HTML


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

    df = pd.DataFrame(refs)
    df.to_csv('ieee.csv',index=False, header=["References"])


def pdfextract(url):
    #url = 'https://arxiv.org/pdf/2007.07751.pdf'
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
            s1 = "\["
            result = [_.start() for _ in re.finditer(s1, text1)]
            strlist = [text1[i:j] for i,j in zip(result, result[1:]+[None])]
            for j in strlist:
                j = j.replace('-\n','')
                j = j.split('\n')
                j = " ".join(j)    
                index1 = j.rfind(".")
                refs.append(j[:index1+1])
                #print(j[:index1+1])
        
        df = pd.DataFrame(refs)
        df.to_csv('pdf.csv',index=False, header=["References"])
        os.remove('metadata.pdf')
        



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
        
    df = pd.DataFrame(refs)
    df.to_csv('springer.csv',index=False, header=["References"])   



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

        df = pd.DataFrame(refs)
        df.to_csv('acm.csv',index=False, header=["References"])




if __name__ == "__main__":
    url = input("Enter url: ")
    if (url.find('ieee')!=-1):
        ieee(url)
    elif (url.find('.pdf')!=-1): # better than before
        pdfextract(url)
    elif (url.find('springer')!=-1): 
        springer(url)
    elif (url.find('acm')!=-1):
        acm(url)

