#!/bin/bash
rm -r tmp/
python3 GenerateCSV.py
java -jar ./jgaap-6.0.0.jar -ee leaveOneOut.run
java -jar ./jgaap-6.0.0.jar -ee run_sent_split.run
java -jar ./jgaap-6.0.0.jar -ee run_syn.run
java -jar ./jgaap-6.0.0.jar -ee run_stop.run
java -jar ./jgaap-6.0.0.jar -ee run_combine_sent.run
java -jar ./jgaap-6.0.0.jar -ee run_repl_stop.run
echo
echo "******* CALCULATING RESULTS *******"
echo
python3 ParseResults.py
echo
echo "******* CHECKING MEANING AND GRAMMAR *******"
echo
python3 CheckGrammar.py
