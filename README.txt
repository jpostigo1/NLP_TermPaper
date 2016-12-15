Style Obfuscation
by Justin Postigo and Logan Williams
CPE 582, Foaad Khosmood
Fall 2016

--- SETUP ---
Before running, you need to have the following installed:
 - Python3
 - NLTK 3
 - JGAAP [https://github.com/evllabs/JGAAP] in the root project directory.
 - Stanford Parser (full) [http://nlp.stanford.edu/software/stanford-parser-full-2016-10-31.zip]
   Manually install it as outlined by the TL;DR in this StackOverflow answer: http://stackoverflow.com/a/34112695/.
Also, make sure that the data is unzipped and in a directory named 15auths in the root project directory (15auths is the first 15 authors of the Drexel-AMT Corpus, downloadable at http://psal.cs.drexel.edu/download/psal_corpora.zip.

--- HOW TO RUN ---
Our project has several different stages, each with their own file to run. The following outlines our pipeline and how to run each step.

--- Generate CSV ---
This step generates obfuscated versions of the documents and CSV files for running the JGAAP command-line tool. From the root project directory, run: 
   python3 GenerateCSV.py

--- JGAAP Baseline ---
This step runs JGAAP to determine a baseline accuracy. From the root project directory, run: 
   java -jar jgaap-6.0.0.jar -ee run1.run
To retrieve the results, run:
   python3 ParseResults.py
This will print out the accuracies of the tests that were run. 

--- JGAAP Experiment ---
This step runs JGAAP to determine the accuracy on our obfuscated versions of the documents. From the root project directory, run: 
   java -jar jgaap-6.0.0.jar -ee run_combine_sent.run
To retrieve the results, run:
   python3 ParseResults.py
This will print out the accuracies of all tests that have been run so far. If you only want to see the most recent run of tests, delete the tmp directory and run JGAAP again. 

--- Grammar/Meaning Preservation ---
This step measures how much grammar/meaning is preserved by using the Stanford Parser's parse scores. From the root project directory, run:
   python3 CheckGrammar.py
Note: This program takes a while (a few minutes). 
