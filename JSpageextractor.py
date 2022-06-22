from requests_html import HTMLSession
import requests
import os

## Scopus: springer works
'''
url = 'https://link.springer.com/article/10.1007/s11696-022-02290-1'
sess = HTMLSession()
r = sess.get(url)

r.html.render()
refer = r.html.xpath('//*[@id="Bib1-content"]/div',first=True)
print(refer.text)


## Google -> arxiv -> Semantic Scholar -> pdf needed , tho it works only till status code. Can't extract refer without pdf
url2 = 'https://www.semanticscholar.org/paper/Secondary-Studies-in-the-Academic-Context%3A-A-and-Felizardo-Souza/c4ed69120d4169f292559316c687db17d276d9dd'
sess = HTMLSession()
r2 = sess.get(url2)

r2.html.render(timeout=20)
print(r2.status_code)
#refer2 = r2.html.xpath('',first=True)
#print(refer2.text)



## PDF: arxiv
url = 'https://arxiv.org/pdf/2007.07751.pdf'
r = requests.get(url, stream = True)
with open('metadata.pdf', 'wb') as f:
    f.write(r.content)
'''

if os.path.exists("2007.07751.pdf"):
    from pdfminer.high_level import extract_text, extract_pages
    import fitz
    with fitz.open('2007.07751.pdf') as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    print(text)
    '''
    text = extract_text('2007.07751.pdf')
    tlow  = text.lower()
    index = tlow.rfind('references')
    if (index != -1):
        text1 = text[index:]
        print(text1)
    #os.remove('metadata.pdf')



## IEEE - doesn't work. Need to use Selenium
url = 'https://ieeexplore.ieee.org/document/7750588'
sess = HTMLSession()
r = sess.get(url)

r.html.render(timeout=20)
refer = r.html.xpath('//*[@id="references-section-container"]/div[2]',first=True)
print(refer)
'''

