# Searching and Selecting studies for Systematic Literature Reviews Updates in Software Engineering

- The project automates the activity of searching and selecting studies for Systematic Literature Review (SLR) updates in Software Engineering. It implements the two types of Snowballing: **Backward Snowballing**, which uses the outgoing references from a paper to identify new potential papers; and **Forward Snowballing**, which identifies new papers using incoming references or citations to a paper. Also, it automates the inicial selection of studies for SLR updates using Machine Learning models which identify the new potential relevant studies for an ongoing SLR update. Here, the paper containing the Author names, Title, Publisher name, Year are extracted along with the bibtex of the papers containing the Abstracts.


### A. Organization of the repository:
The details of the main folders are as follows:
1. Datasets:
   - Dataset_SLR_Replication-Search_Snowballing_Backward_Forward : It is the dataset used for the SLR Replication. It contains the seed sets for the different rounds of Backward and Forward Snowballing.
   - Dataset_SLR_Update-Search_Snowballing_Forward - It is the dataset used for 1 Round of Forward Snowballing in SLR Update process. 
   - Dataset_SLR_Update-Selection -  It is the dataset used for the selection of studies using Machine Learning in SLR Update process.
   
2. Codes: 
   - SLR Replication - _Search_SLR_Snowballing.py_ is the code to be run after placing _links.txt_ as mentioned in section B. It implements the Snowballing tool. The _extract_X.py_ files are helper code to _Search_SLR_Snowballing.py_ . 
   - SLR Update - _create_dataset.py_ and _Selection_SLR_update.ipynb_ perform the SLR Update process.

3. Evaluation:
   - SLR Replication - They contain the Input and Output files of the Replication. The actual input are the DOI links from Crossref which must be put inside the links.txt file to perform the experiment. The output files contain the bibtex of the extracted papers and the Csv with the status of extraction.
   - SLR Update Evaluation - They contain the Input and Output files of the SLR Update. Here there are 2 inputs:
        - For Round 1 Forward Snowballing: The actual input are the DOI links from Crossref which must be put inside the _links.txt_ file to perform the experiment. The output files contain the bibtex of the extracted papers and the Csv with the status of extraction.
        - For the SLR selection process: The training bib files were from the paper /ref , and the testing bib files were from the result of round 1 forward snowballing. The output is the relevant studies identified by the model from the testing set.


### B. How to run the code:
1. Clone this repository.
2. To run the SLR Replication and put the seed set in the file _links.txt_ (in the form of doi urls of the papers separated by newlines)
3. Place _links.txt_ in the same directory as _./Codes_ and run the following:
  ```
  $ python Search_SLR_Snowballing.py
  ```
4. Enter the inputs asked like number of iterations, and type of snowballing.
5. The files _References-(type).csv_ and _allbibs-(type).bib_ will be created in the _./Codes_ directory.
Note: User must have an institutional account on Researchgate and fill the constants in _extract_bib.py_ for username and password.
6. To perform the SLR Update, first create the testing set by running 1 round of forward snowballing by following steps 2 to 4. Use the bib file for the testing. 
7. Put the training and testing bibs in the same directory as _./Codes_ and after modifying the _create_dataset.py_ according to the file name of the bibs, run:
  ```
  $ python create_dataset.py
  ```
8. The CSV files will be generated. Use them for step 9.
9. The selection process is done using Machine Learning. Open the _Selection_SLR_update.ipynb_ notebook in Google Colab or as Jupyter Notebook (for Colab, upload the _Training.csv_ and _Testing.csv_ files created in step 8).
10. Train and evaluate the classifiers on the dataset. You can finetune the hyperparameters as needed.
11. The output is the relevant studies to update the SLR.


### C. Requirements
The libraries and modules required to be imported before running section B are given in _requirements.txt_ .
To start, open up a terminal or a command prompt and navigate to the _./Codes_ directory of the project. Once you are there, type the following command:
  ```
  $ pip install -r requirements.txt
  ``` 
  
 
NOTE: Every directory of the 3 main folders contains a _helpdoc.txt_ with further details about the files.
