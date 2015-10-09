# data-fileformat-conversions
Python code to convert csv file to ascii file 

csv file source: https://dandelion.eu/datamine/open-big-data/
https://dandelion.eu/datagems/SpazioDati/telecom-sms-call-internet-mi/description/

The ascii file is created following the characteristics of Milano grid: https://dandelion.eu/datagems/SpazioDati/milano-grid/description/

1- create folder grids
2- create folder sources
3- copy the csv file on folder sources
4- open csv-ascii.py and modify the name of the variable csv_file with the name of the csv-file to convert
5- open the command shell go to the folder and run the program:  

$ python csv-ascii.py

if you want to see how much time is going to take write:

$ time python csv-ascii.py
