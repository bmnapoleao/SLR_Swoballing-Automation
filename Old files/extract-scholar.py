# imports
import os
import time
import re
import csv
import pandas as pd
import requests
import random
import logging
from testfixtures import LogCapture
import io
import urllib.request
from collections import OrderedDict
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from parsel import Selector
from playwright.sync_api import sync_playwright

import traceback


#---CONSTANTS---#
crossref = 'https://search.crossref.org/references'
zotero = 'https://zbib.org/'


## Code credits @https://github.com/akhilanto/GoogleScholar-WebScarping-Using-Free-VPN-in-Python/blob/master/GoogleScholarWebScraping.py
ip = ''
proxies = []
def removeip(ip):
    global proxies
    proxies.pop()
    print(str(len(proxies)) + " Proxies Remaining")

def getip():
    global ip , proxies
    i = len(proxies)-1
    if i > 0:
        ip = proxies[i]
        removeip(proxies[i])
        print("ip=" + ip )
        return True
    else:
        return False


def get_proxies():
    url = 'https://free-proxy-list.net/'
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    response = requests.get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    body = html_soup.find("table").find("tbody").find_all("tr")
    proxies = []
    for i in range(0,len(body)):
        c = 'http://'+body[i].findAll('td')[0].text+":"+body[i].findAll('td')[1].text
        proxies.append(c)
        c = 'https://'+body[i].findAll('td')[0].text+":"+body[i].findAll('td')[1].text
        proxies.append(c)
    return proxies


def init():
    global proxies
    proxies = get_proxies()
    print(str(len(proxies)) + " Proxies")
    getip()


def iplen():
    global proxies
    return (len(proxies))

## End credits ##




def randommouse(page):
    num = random.randint(1,5)
    if num==1:
        page.mouse.move(0, 0)
        page.mouse.down()
    elif num==2:
        page.mouse.wheel(300,900)
        page.mouse.up()
    elif num==3:
        page.mouse.move(0, 100)
        page.mouse.wheel(300,600)
    elif num==4:
        page.mouse.click(0, 100,delay=1000)
        page.mouse.down()
    elif num==5:
        page.mouse.move(100, 0)



## Credits @https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/


def checklog():
    logger = logging.getLogger('basic_logger')
    logger.setLevel(logging.DEBUG)

    ### Setup the console handler with a StringIO object
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.DEBUG)

    logger.addHandler(ch)
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()

    ### Output as lower case to prove it worked.
    print("\n\nyo")
    print(log_contents.lower())
    print("yo\n\n")


def workingproxy():
    getip()
    try:
        proxy = urllib.request.ProxyHandler({'http':ip,'https':ip})
        urllib.request.urlopen("https://zbib.org/")
        print("yo\n\n")
        return ip
    except IOError:
        print("Connection error! (Check proxy)")
        getip()



def extract_scholar(url):
    c = False
    while not c:
        try:
            with sync_playwright() as p:
                #ipw = workingproxy() # sets ip
                #print(ipw)
                browser = p.chromium.launch(headless=False, slow_mo=50)
                #, proxy={
                 #   "server": ipw,
                #}
                headers = ''
                #Source: @https://gist.github.com/pzb/b4b6f57144aea7827ae4
                agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
                         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                         "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"]

               
    ## Credits end ##
                    
                context = browser.new_context(user_agent = random.choice(agent))
                #, extra_http_headers = headers
                page = context.new_page()
                
                

                # Get reference from zotero
                page.goto(zotero,timeout=0)
                
                page.fill('input[type="text"]', url)
                page.locator('button[class="btn btn-lg btn-secondary"]',has_text="Cite").click()
                randommouse(page)            
                time.sleep(5)

                reference = page.locator('div[class="csl-bib-body"]').inner_text()
                print(reference)
                time.sleep(3)
             
                
                # scholar scraping
                if reference:
                    page.goto(f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={reference}&btnG=", timeout=0)
                    page.locator('a',has_text="Cited by").click()
                    randommouse(page)
                    time.sleep(20)
                    
                    try:
                        while True:
                            
                            cites = page.locator('a[class="gs_or_cit gs_or_btn gs_nph"]')
                            c = cites.count()
                            print(cites)
                            print(c)
                            for i in range(1,c):
                                ref = cites.nth(i).click()
                                time.sleep(5)
                                
                                #text = selector.css("div.gs_citr:nth-child(1)::text").get()
                                text = page.locator('div[class="gs_citr"]').nth(1).inner_text()
                                print(text)
                                page.locator('a[id="gs_cit-x"]').click()
                                randommouse(page)
                                time.sleep(3)
                            
                            if page.is_visible('//*[@id="gs_n"]/center/table/tbody/tr/td[4]/a/b'):
                                print("Found next ")
                                page.locator('td[align="left"]',has_text="Next").click()
                            else:
                                break
                            time.sleep(3)
                        
                            
                    except Exception as e:
                        print(e)

                    finally:
                        c = True

                #checklog()
                browser.close()
                #return refs
                
        except Exception as e:
            print(e)
            continue
                            
            

#init()
url = input("Enter url: ")
print(extract_scholar(url))

        
'''

if __name__ == "__main__":
    try:
        text = ''
        filepath = Path('links1.txt')
        # create the file if it doesn't exist
        filepath.touch(exist_ok=True)
        with open('links1.txt', 'r') as f:
            text = f.read()
            f.close()
            
        links = text.split('\n')
        url = input("Enter url: ")
        
        if url not in links:
            refs = []

            df = pd.DataFrame(refs)
            # append the references
            if not os.path.isfile('Citedby.csv'):
               df.to_csv('Citedby.csv', index=False, header=["Citedby"])
            else: 
               df.to_csv('Citedby.csv', mode='a',index=False, header=False)

            # append the link
            with open('links1.txt', 'a') as fd:
                fd.write(url+'\n')  # includes the original url, not redirected one

                
        else:
            print("Link exists! References already extracted.")
        
    except HTTPError as e:
        print("HTTPError. Can't extract references.")
        traceback.print_exc()
'''
