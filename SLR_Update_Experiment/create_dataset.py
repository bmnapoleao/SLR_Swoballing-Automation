# Importing Bibtex handler libraries
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
import pandas as pd


#-----------------------------------------TRAINING BIB------------------------------------------------#

## Training-excluded studies
db = ''
parser = BibTexParser(common_strings = True)

# Loading the bib file
with open('Training_Excluded.bib', encoding = "utf-8") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)

# Extracting abstract and title
abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    if 'title' in db.entries[i]:
        title.append(db.entries[i]['title'])
    else:
        title.append("")

inc_exc = [0]*len(db.entries) # class 0 for excluding

# Writing to dataframe
df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Training.csv',index=False)

    
#-----------------------------------------------------------------------------------------#


## Training-included studies
db = ''
parser = BibTexParser(common_strings = True)

# Loading the bib file
with open('Training_Included.bib', encoding = "Windows-1252") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)

# Extracting abstract and title
abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    title.append(db.entries[i]['title'])

inc_exc = [1]*len(db.entries) # class 1 for including

# Writing to dataframe
df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Training.csv',mode='a',index=False,header=False)


#------------------------------------------TESTING BIB-----------------------------------------------#


## Testing-included studies
db = ''
parser = BibTexParser(common_strings = True)

# Loading the bib file
with open('Testing_Included.bib', encoding = "Windows-1252") as bibtex_file:
    db = bibtexparser.load(bibtex_file,parser)

# Extracting abstract and title
abst = []
title = []
for i in range(len(db.entries)):
    if 'abstract' in db.entries[i]:
        abst.append(db.entries[i]['abstract'])
    else:
        abst.append("")
    title.append(db.entries[i]['title'])

inc_exc = [1]*len(db.entries) # class 1 for including

# Writing to dataframe
df = pd.DataFrame(list(zip(title, abst, inc_exc)), columns=['Title','Abstract','Relevance'])

df.to_csv('Testing.csv',index=False)

