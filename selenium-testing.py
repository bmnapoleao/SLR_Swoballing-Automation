import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def rendering(url):
    
        # change '/usr/local/bin/chromedriver' to the path from you got when you ran 'which chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        #driver = webdriver.Chrome('C:\Program Files\Chromedriver\chromedriver.exe') # run ChromeDriver
        driver.get(url)                                          # load the web page from the URL
        time.sleep(3)                                            # wait for the web page to load
        render = driver.page_source                              # get the page source HTML
        driver.quit()                                            # quit ChromeDriver
        return render                                            # return the page source HTML



### IEEE works
url = 'https://ieeexplore.ieee.org/document/7750588'

page = rendering(url)
soup = BeautifulSoup(page, 'html.parser')
res = soup.find(id='references-section-container')
res_data = res.find_all('div', class_='col u-px-1')

for num, i in enumerate(res_data):
    d = i.text.strip(' ')
    print(num, d)

#print(res.prettify())
