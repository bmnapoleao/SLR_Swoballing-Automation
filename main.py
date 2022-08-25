import pathlib
import sys
import os
import requests
import urllib.request
import traceback
import pandas as pd


p = str(pathlib.Path(__file__))
ROOT = p[:p.find('main')]


from extract_bib import *
from extract_cits import *

BASE_URL = 'https://doi.org/'


def forward(links, num_iter, seed_papers):
    try:
        # links must be doi
        for i in range(num_iter): #for iterations
            papers = []
            if i>0:
                links = list(filter(("No doi").__ne__, all_dois))
                #print(len(links))
                for doi in links:
                    paper = search_sscholar(doi)
                    papers.append(paper)
            else:
                papers = seed_papers

            all_dois = []
            for paper in papers:
                dois = []
                citations, refs = search_cites(paper)
                all_dois = all_dois + citations
                
                # append the citations
                direc = 'References-forw.csv'
                if not os.path.isfile(direc):
                    df = pd.DataFrame(refs)
                    df.to_csv(direc, index=False, header=["References"])
                    ref = pd.read_csv(direc)
                    ref['DOIS']=""
                    ref['Iteration']=0
                    ref['Status'] = ""
                    ref.to_csv(direc,index=False)
                else: 
                    ref = pd.read_csv(direc)
                    inde = all_indices[len(all_indices)-1]+1
                    for k,val in enumerate(refs):
                        ref.loc[inde+k,'References'] = val
                    print(ref.tail())
                    with open(direc,'w', encoding = "utf-8",newline='') as f:
                        ref.to_csv(f, index=False)
                
                
                ref = pd.read_csv(direc)
                    
                dois = citations # dois in a variable

                all_indices = []
                for j, s in enumerate(refs):
                    last = ref.loc[ref['References'] == refs[j]].index.values
                    cell_index = last[len(last)-1]
                    all_indices.append(cell_index)
                
                # insert code for checking
                completed = ''
                if i==1:
                    completed = links
                else:
                    completed = ref['DOIS']
                    
                n_dois = []
                cell_indices = []
                for j, s in enumerate(dois):
                    last = ref.loc[ref['References'] == refs[j]].index.values
                    cell_index = last[len(last)-1]
                    if not (s=="No doi"):
                        print(f'\nIndex of doi: {s} = {cell_index}')
                        if s in completed:
                            # mark done already in reference
                            ref.loc[cell_index,'Iteration'] = i+1
                            iteration = ref.loc[last[0],'Iteration']
                            ref.loc[cell_index,'Status'] = "Done already in " +str(iteration)
                        else:
                            n_dois.append(s)
                            cell_indices.append(cell_index)
                    else:
                        ref.loc[cell_index,'Iteration'] = i+1
                        ref.loc[cell_index,'Status'] = "DOI not found"

                for k,val in enumerate(dois):
                    ind = all_indices[k]
                    ref.loc[ind,'DOIS'] = val
                with open(direc,'w', encoding = "utf-8",newline='') as f:
                    ref.to_csv(f, index=False)

                
                bibs = extract_bib_abs(n_dois, direc, cell_indices)
                extract_abs_also(n_dois, bibs, direc, i+1, cell_indices,'forw')

                

         
                  
    except Exception:
        traceback.print_exc()
        




def seed_iter(links):
    refs = []
    papers = []
    for doi in links:
        paper = search_sscholar(doi)
        reference = get_refs(paper)
        refs.append(reference)
        papers.append(paper)
        
    df = pd.DataFrame(refs)
    direc = os.path.join(ROOT, 'References.csv')
    # append the references
    if not os.path.isfile('References.csv'): 
        df.to_csv('References.csv', index=False, header=["References"])
        ref = pd.read_csv(direc)
        ref['Status'] = ""
        ref['Iteration']=0
        ref.to_csv(direc,index=False)
    

    ref = pd.read_csv(direc)
    all_indices = []
    for j, s in enumerate(refs):
        cell_index = ref.loc[ref['References'] == refs[j]].index.values[0]
        all_indices.append(cell_index)
        
    #print(all_indices)
    bibs = extract_bib_abs(links, direc, all_indices)
    extract_abs_also(links,bibs, direc, 0, all_indices,'seed')
    return papers
    
    




def backward(links, num_iter, seed_papers):
   
    for i in range(num_iter): #for iterations
        papers = []
        if i>0:
            links = list(filter(("No doi").__ne__, all_dois))
            print(len(links))
            for doi in links:
                paper = search_sscholar(doi)
                papers.append(paper)
        else:
            papers = seed_papers
        all_dois = []
        for paper in papers:
            dois = []
            refs = []
            ref_nodoi = []
            rs = paper['references']
            for p in range(len(rs)):
                reference = get_refs(rs[p])
                
                if rs[p]['doi']:
                    dois.append(BASE_URL + rs[p]['doi'])
                    refs.append(reference)
                else:
                    ref_nodoi.append(reference)

            if ref_nodoi:
                new_dois = doi_helper(ref_nodoi) # search for doi if not already there
                refs = refs + ref_nodoi
                dois = dois + new_dois
            #print(len(refs),len(dois))
            all_dois = all_dois + dois
            
            if refs:
                
                # append the references whatever is extracted
                #os.path.join(ROOT, )
                direc = 'References-back.csv'
                
                
                if not os.path.isfile(direc):
                    df = pd.DataFrame(refs)
                    df.to_csv(direc, index=False, header=["References"])
                    ref = pd.read_csv(direc)
                    ref['DOIS']=""
                    ref['Iteration']=0
                    ref['Status'] = ""
                    ref.to_csv(direc,index=False)
                    
                else:
                    ref = pd.read_csv(direc)
                    
                    
                    inde = all_indices[len(all_indices)-1]+1
                    for k,val in enumerate(refs):
                        ref.loc[inde+k,'References'] = val
                    print(ref.tail())
        
                    with open(direc,'w', encoding = "utf-8",newline='') as f:
                        ref.to_csv(f, index=False)
                
                
                ref = pd.read_csv(direc)

                all_indices = []
                for j, s in enumerate(refs):
                    last = ref.loc[ref['References'] == refs[j]].index.values
                    cell_index = last[len(last)-1]
                    all_indices.append(cell_index)
                
                #print(all_indices) 
                # insert code for checking
                completed = ''
                if i==1:
                    completed = links
                else:
                    completed = ref['DOIS'] 

                n_dois = []
                cell_indices = []
                for j, s in enumerate(dois):
                    last = ref.loc[ref['References'] == refs[j]].index.values
                    cell_index = last[len(last)-1]
                    if not (s=="No doi"):                        
                        print(f'\nIndex of doi: {s} = {cell_index}')
                        if s in completed:
                            # mark done already in reference
                            ref.loc[cell_index,'Iteration'] = i+1
                            iteration = ref.loc[last[0],'Iteration']
                            ref.loc[cell_index,'Status'] = "Done already in " +str(iteration)
                        else:
                            n_dois.append(s)
                            cell_indices.append(cell_index)
                    else:
                        ref.loc[cell_index,'Iteration'] = i+1
                        ref.loc[cell_index,'Status'] = "DOI not found"

                for k,val in enumerate(dois):
                    ind = all_indices[k]
                    ref.loc[ind,'DOIS'] = val
                with open(direc,'w', encoding = "utf-8",newline='') as f:
                    ref.to_csv(f, index=False)
                
                bibs = extract_bib_abs(n_dois, direc, cell_indices)
                #print(len(n_dois),len(dois),len(bibs))
                extract_abs_also(n_dois, bibs, direc, i+1, cell_indices,'back')








if __name__ == "__main__":
    try: 
        num_iter = int(input('Enter Number of iterations of Snowballing(integer): '))
        stype = int(input('Enter choice for Type of Snowballing (integer) \n 1. Backward 2.Forward 3.Both \nChoice: '))

        text = ''
        #----file must contain the links to the seed papers as dois----#
        with open('links.txt', 'r') as f:
            text = f.read()
            f.close()          
        links = text.split('\n')
        
        if stype==1:
            print('\n__Backward Snowballing__\n')
            papers = seed_iter(links)
            backward(links, num_iter, papers)
            
        elif stype==2:
            print('\n__Forward Snowballing__\n')
            papers = seed_iter(links)
            forward(links, num_iter, papers)
        else:
            print('\n__Backward and Forward Snowballing__\n')
            papers = seed_iter(links)
            backward(links, num_iter, papers)
            forward(links, num_iter, papers)

        
    except Exception:
        print("Enter data of correct data type, and Ensure the file links.txt has the seed set!!")
        traceback.print_exc()
        
