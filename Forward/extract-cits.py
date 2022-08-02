import requests
import sys
import os
from pathlib import Path
import pandas as pd
import traceback
sys.path.append('E:\Mitacs-project\Swoballing_Backward_-Automation\Backward')
from extract_bib import *

BASE_URL = 'http://dx.doi.org/'


if __name__ == "__main__":
    try:
        doi = input("Enter doi: ") # not url
        # modify if not doi
        # extract citations as doi of papers from OpenCitations
        res = requests.get(f'https://w3id.org/oc/index/coci/api/v1/citations/{doi}')
        data = res.json()
        cit_count = len(data)

        citations = []
        for i in range(cit_count):
            citations.append(BASE_URL + data[i]['citing'])
        
        text = ''
        filepath = Path('links.txt')
        # create the file if it doesn't exist
        filepath.touch(exist_ok=True)
        with open('links.txt', 'r') as f:
            text = f.read()
            f.close()
            
        links = text.split('\n')
        
        if doi not in links: # checks redundancy
            df = pd.DataFrame(citations)
            # append the citations
            if not os.path.isfile('References.csv'):
               df.to_csv('References.csv', index=False, header=["References"])
            else: 
               df.to_csv('References.csv', mode='a',index=False, header=False)

            # append the link
            with open('links.txt', 'a') as fd:
                fd.write(doi+'\n')  # includes the original url, not redirected one

            dois = citations
            print(dois)
            bibs = extract_bib_abs(dois)
            print(len(bibs),len(dois))
            extract_abs_also(dois,bibs) 
            
            # Rename References.csv
            try:
                os.rename("References.csv", "References-updated.csv")
            except OSError as exc:
                print(f'WARNING: could not rename References : {exc}')
            

        
                
        else:
            print("Link exists! Citations already extracted.")
        
    except Exception as e:
        traceback.print_exc()
