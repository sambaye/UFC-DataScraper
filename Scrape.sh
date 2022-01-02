#!/bin/bash

# Remove previous files
rm PedigreeData/*.npy
rm StaticDataUFC/TXT/*.txt
rm StaticDataUFC/PKL/*.pkl

# Scrape Data From Sherdog.com
python scrapeSherdogP.py
mv *.npy PedigreeData/

# Scrape Data From UFC.com
python UFC_scrapeS.py 
mv *.txt StaticDataUFC/TXT/
mv *.pkl StaticDataUFC/PKL/
