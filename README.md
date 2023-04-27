# Snowballing_Automation

- The project automates **Snowballing** - a method of conducting Systematic Literature Reviews. It implements the two types of Snowballing: **Backward Snowballing**, which uses the outgoing references from a paper to identify new potential papers; and **Forward Snowballing**, which identifies new papers using incoming references or citations to a paper. Here, the paper containing the Author names, Title, Publisher name, Year are extracted along with the bibtex of the papers containing the Abstracts. 

- **Updating the SLR** is done using Machine Learning models which identify the new papers which are relevant to the study. 


### A. Organization of the repository:
The details of the main folders are as follows:
1. Datasets:
   - Dataset_SLR_Replication-Search_Snowballing_Backward_Forward : It is the dataset used for the SLR Replication. It contains the seed sets for the different rounds of Backward and Forward Snowballing.
   - Dataset_SLR_Update-Search_Snowballing_Forward - It is the dataset used for 1 Round of Forward Snowballing in SLR Update process. 
   - Dataset_SLR_Update-Selection -  It is the dataset used for the selection of studies using Machine Learning in SLR Update process.
   
2. Codes: 
   - SLR Replication - main.py is the code to be run after placing links.txt as mentioned in section B. It implements the Snowballing tool. The extract_X.py files are helper code to main.py . 
   - SLR Update - create_dataset.py and SLR_update_ML.ipynb perform the SLR Update process.

3. Evaluation:
   - SLR Replication - They contain the Input and Output files of the Replication. The actual input are the DOI links from Crossref which must be put inside the links.txt file to perform the experiment. The output files contain the bibtex of the extracted papers and the Csv with the status of extraction.
   - SLR Update Evaluation - They contain the Input and Output files of the SLR Update. Here there are 2 inputs:
        - For Round 1 Forward Snowballing: The actual input are the DOI links from Crossref which must be put inside the links.txt file to perform the experiment. The output files contain the bibtex of the extracted papers and the Csv with the status of extraction.
        - For the SLR selection process: The training bib files were from the paper /ref , and the testing bib files were from the result of round 1 forward snowballing. The output is given as performance metrics of the evaluation of relevant studies identified by the model from the testing set.


### B. How to run the code:
1. Clone this repository.
2. To run the SLR Replication and put the seed set in the file links.txt (in the form of doi urls of the papers separated by newlines)
3. Place links.txt in the same directory as ./Codes and run the following:
  ```
  $ python main.py
  ```
4. Enter the inputs asked like number of iterations, and type of snowballing.
5. The files References-(type).csv and allbibs-(type).bib will be created in the ./Codes directory.
Note: User must have an institutional account on Researchgate and fill the constants in extract_bib.py for username and password.
6. To perform the SLR Update, first create the testing set by running 1 round of forward snowballing by following steps 2 to 4. Use the bib file for the testing. 
7. Put the training and testing bibs in the same directory as ./Codes and after modifying the create_dataset.py according to the file name of the bibs, run:
  ```
  $ python create_dataset.py
  ```
8. The CSV files will be generated. Use them for step 9.
9. The selection process is done using Machine Learning. Open the SLR_update_ML.ipynb notebook in Google Colab or as Jupyter Notebook (for Colab, upload the Training.csv and Testing.csv files created in step 8).
10. Train and evaluate the classifiers on the dataset. You can finetune the hyperparameters as needed.
11. The output is the relevant studies to update the SLR.


### C. Requirements
The libraries and modules required to be imported before running section B are given in requirements.txt
To start, open up a terminal or a command prompt and navigate to the ./Codes directory of the project. Once you are there, type the following command:
  ```
  $ pip install -r requirements.txt
  ``` 
  
 
NOTE: Every directory of the 3 main folders contains a helpdoc with further details about the files.
