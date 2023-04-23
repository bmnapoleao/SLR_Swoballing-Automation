# Snowballing_Automation

The project automates **Snowballing** - a method of conducting Systematic Literature Reviews. It implements the two types of Snowballing: **Backward Snowballing**, which uses the outgoing references from a paper to identify new potential papers; and **Forward Snowballing**, which identifies new papers using incoming references or citations to a paper. Here, the Reference string containing the Author names, Title, Publisher name, Year are extracted along with the bibtex of the papers containing the Abstracts. It is proposed that the Machine Learning model will identify which papers are relevant to the study. 


  
### A. How to run the code:
1. Clone this repository and put the seed set in the file links.txt (in the form of doi urls of the papers separated by newlines)
2. Run the following in the root directory
  ```
  $ python main.py
  ```
3. Enter the inputs asked like number of iterations, and type of snowballing.
4. The files References-(type).csv and allbibs-(type).bib will be created in the root directory.
Note: User must have an institutional account on Researchgate and fill the constants in extract_bib.py for username and password.

### B. To train the Machine Learning model:
1. Take the allbibs-(type).bib files and turn them into Training and Testing sets by partitioning them into Training_Excluded.bib, Training_Included.bib, Testing_Excluded.bib, Testing_Included.bib. Training set should include the bibs extracted from the seed set while Testing set should include the potentially relevant papers identified.
2. Place the newly created bibs into their root directory and run 
  ```
  $ python create_dataset.py
  ```
3. Open the SLR_update_ML.ipynb notebook in Google Colab or as Jupyter Notebook (for Colab, upload the Training.csv and Testing.csv files created in step 2).
4. Train and evaluate the classifier on the dataset. You can finetune the hyperparameters as needed.


### C. Requirements
The libraries and modules required to be imported before running part A. are given in requirements.txt
To start, open up a terminal or a command prompt and navigate to the root directory of the project. Once you are there, type the following command:
  ```
  $pip install -r requirements.txt
  ```
