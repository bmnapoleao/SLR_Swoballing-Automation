import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


crossref = 'https://search.crossref.org/references'

#options = webdriver.ChromeOptions()
#options.add_argument('--headless') 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(crossref)                                          # load the web page from the URL
time.sleep(3)                                            # wait for the web page to load

#read csv file for references
ieee = pd.read_csv("ieee.csv")
refs = ieee['References']
refstring = ''
for i in refs:
    refstring += i.replace('\n',' ')
    refstring += '\n'

#input refstring in text area
textarea = driver.find_element(By.NAME, "references")
textarea.send_keys(refstring)
button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/form/div/div/button")
button.click()

# goes to results page
mytable = driver.find_element(By.CLASS_NAME,'table.table-striped')
for row in mytable.find_elements(By.TAG_NAME,'tr'):
    elecell = row.find_elements(By.TAG_NAME,'td')
    if len(elecell)==1:
        for cell in elecell:
            try:
                a = cell.find_element(By.TAG_NAME, 'a')
                print(a.text)
            except NoSuchElementException:
                print("Element not found")
    else:
        print("Doesn't have doi")



'''
resgate = 'https://www.researchgate.net/search.Search.html?type=publication&query='

req = requests.get(resgate + )
soup = BeautifulSoup(req.text,'html.parser')

'''



#driver.quit()




