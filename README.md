# UFC-DataScraper
I have created a simple web scraper that 
you can use to get some pretty interesting 
comparison stats for ufc fighters heading into battle :). 

The script scrapeSherdogP.py scrapes Data From Sherdog.com and 
tries to quantify the pedigree or experience level of a fighter. The data generated is stored in the "PedigreeData" folder. 

The one dimensional pedigree(example: Andrea-Lee-149037PED.npy) is simply the fighters record.

The two dimensional pedigree(example: Andrea-Lee-149037twoLen.npy) is the combined record of the fighters opponents: this should theoretically should provide information about the quality of opponents the fighter has faced but it is farfrom accurate in practice(you can tweak it to taste).


The script UFC_scrapeS.py scrapes Data From UFC.com and gives you some important stats about the two fighters. The final outputs are .txt files that have been formatted for a quick comparison of the two fighters stats.(They can be foundin the "StaticDataUFC/TXT/" directory) 

# How to Generate Data. 
It is pretty easy to generate data, you simply need to  have to have properly 
formatted inputs and the proper python modules located in requirements.dat. I have put some sample inputs files in the"Input" folder to get you started.

The only pain is that sherdog.com and UFC.com have unique tags 
for the fighters so you need to find those tags and generate the input files("NFightersSHER.txt" and "NFightersUFC.txt"). There are some scripts in the "Input" directory that attempt to get these tags for you from a general input file called "Fighters.txt" but you will have to do some manual editing to get the final output. 

Ps. the input files have to be ordered in a way where the people fighting are directly next to eachother(on the next line).  


Once you have the proper inputs you should be able to get the data by running the following commands

1. pip install -r requirements.dat
2. bash Scrape.sh 
