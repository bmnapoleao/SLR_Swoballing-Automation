import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
import pandas as pd


# Training-exc
db = ''
parser = BibTexParser(common_strings = True)

with open('Training_Excluded.bib', encoding = "utf-8") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)

abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    title.append(db.entries[i]['title'])

inc_exc = [0]*len(db.entries) #0 for excluding

df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Training.csv',index=False)

    
#Training-inc
db = ''
parser = BibTexParser(common_strings = True)

with open('Training_Included.bib', encoding = "utf-8") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)

abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    title.append(db.entries[i]['title'])

inc_exc = [1]*len(db.entries) #1 for including

df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Training.csv',mode='a',index=False,header=False)





#Testing-exc
db = ''
parser = BibTexParser(common_strings = True)

with open('Testing_Excluded.bib', encoding = "utf-8") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)
abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    title.append(db.entries[i]['title'])

inc_exc = [0]*len(db.entries) #0 for excluding

df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Testing.csv',index=False)


#Testing-inc
db = ''
parser = BibTexParser(common_strings = True)

with open('Testing_Included.bib', encoding = "utf-8") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)

abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    title.append(db.entries[i]['title'])

inc_exc = [1]*len(db.entries) #1 for including

df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Testing.csv',mode='a',index=False,header=False)

