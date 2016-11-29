#!/bin/bash
rm -r tmp/
python3 GenerateCSV.py
java -jar ../jgaap-6.0.0.jar -ee run1.run
java -jar ../jgaap-6.0.0.jar -ee run2.run
java -jar ../jgaap-6.0.0.jar -ee run_syn.run
java -jar ../jgaap-6.0.0.jar -ee run_stop.run
java -jar ../jgaap-6.0.0.jar -ee run_combine_sent.run
