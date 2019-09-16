# This program will serve as the data collector and analyser. 
# Aptly named Sharin-Gan this program wil be a template for capturing data and trying to copy human actions.
# Hence the name of the repository copy_cat

import csv
import pandas as pd
from  datetime import datetime

class DataLogger :
    def __init__(self):
        # The name of the data collection file will be set according to the time during which a data logging session is called
        self.filename = "datalog-" + str(datetime.now()) +".csv"
        self.fieldnames = ['position','velocity','angle','input']
        self.csvfile = None
        
        with open (self.filename,'w',newline='') as self.csvfile:
            # Initialising the File to be written in
            self.writer = csv.DictWriter(self.csvfile,fieldnames = self.fieldnames)
            self.writer.writeheader()
        
        print("Sharin Gan !")
        
    def writeData(self,position,velocity,angle,game_input):
        # Not sure if this is right, But I guess the file handle has to be assigned once again

        with open (self.filename,'a',newline='') as self.csvfile:
            self.writer = csv.DictWriter(self.csvfile,fieldnames = self.fieldnames)
            self.writer.writerow({'position':position,'velocity':velocity,'angle':angle,'input':game_input})

        
if __name__=="__main__":
    SharinGan = DataLogger()
    SharinGan.writeData(1,1,20,1)
    SharinGan.writeData(1,2,20,-1)