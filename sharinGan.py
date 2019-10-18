# This program will serve as the data collector and analyser. 
# Aptly named Sharin-Gan this program wil be a template for capturing data and trying to copy human actions.
# Hence the name of the repository copy_cat

import csv
import pandas as pd
from  datetime import datetime
import glob
from sklearn import linear_model
import time

class DataLogger :
    def __init__(self):
        # The name of the data collection file will be set according to the time during which a data logging session is called
        self.filename = "train_data/datalog-" + str(datetime.now()) +".csv"
        self.fieldnames = ['position','velocity','acceleration','input','time_interval']
        self.csvfile = None
        self.writer = None
        self.input_time = None
        self.input_time_previous = 0
        
    
    def initDataLogger(self):
        with open (self.filename,'w',newline='') as self.csvfile:
            # Initialising the File to be written in
            
            self.writer = csv.DictWriter(self.csvfile,fieldnames = self.fieldnames)
            self.writer.writeheader()
            print("Sharin Gan !")
        
    def writeData(self,position,velocity,acceleration,game_input):
        # Not sure if this is right, But I guess the file handle has to be assigned once again
        self.input_time = time.clock()
        time_interval = self.input_time - self.input_time_previous

        with open (self.filename,'a',newline='') as self.csvfile:
            self.writer = csv.DictWriter(self.csvfile,fieldnames = self.fieldnames)
            self.writer.writerow({'position':position,'velocity':velocity,'acceleration':acceleration,'input':game_input,'time_interval':time_interval})
        
        self.input_time_previous = self.input_time


class DataAnalyser :
    def __init__(self):
        #self.data_path = r'/home/darshit/project_propeller/src/copy_cat/'
        self.data_frame = None
        self.sharin_gan = None
        self.data_available = False

    def genDataFrame(self):

        data_files = glob.glob("train_data/datalog-*.csv")
        #print(self.data_path)
        df = []
        print("Reading Data Files")
        if len(data_files) == 0 :
            print("No Data Files to analyse")
            return
        else :
            for filename in data_files:
                print("Gathering data from %s" %(filename))
                data_frame = pd.read_csv(filename,index_col=None,header=0)
                df.append(data_frame)
            print("Generating Data Frame")
            self.data_frame = pd.concat(df,axis = 0,ignore_index = True)
            self.data_available = True
        

    def normDataFrame(self):
        # Using Mean Normalisation
        # Since values are all within range of each other, we simply express position around the central value of 804
        # This remains specific only to the application of copy cat as a ball plate, and this function would have to be generalised later
        self.data_frame['position'] = self.data_frame['position'] - 804
        
    def copyCatJutsu(self):
        print("Studying Moves")
        self.sharin_gan = linear_model.LinearRegression()
        Y = self.data_frame[['input','time_interval']]
        X = self.data_frame[['position','acceleration','velocity']]

        self.sharin_gan.fit(X,Y)
        print("Analysis Complete")
        
        """
        new_position = 0.10
        new_angle = 0.15
        new_velocity = 0.1
        new_input = self.sharin_gan.predict([[new_position,new_angle,new_velocity]])
        print(new_input)
        """

        
if __name__=="__main__":
    SharinGan = DataAnalyser()
    #SharinGan.writeData(1,1,20,1)
    #SharinGan.writeData(1,2,20,-1)
    SharinGan.genDataFrame()
    SharinGan.normDataFrame()
    SharinGan.copyCatJutsu()