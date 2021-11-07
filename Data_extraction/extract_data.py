#Ce programme utilise la programmation objet pour, à partir d'un fichier excel ou pkl, obtenir une base de données (dataframe) contenant les mêmes informations.
#On l'a utilisé pour créer les bases de données sur les musées, les festivals, la population française.

import os.path
from pathlib import Path 
scriptpath = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

import pandas as pd 

class load_data:
    """ 
    This class will be used to extract data from databases 
    """
    #initialize the class object
    #init flag determines whether this is the first load of the database or not
    #test flag determines wether to get a small sample size or not
    def __init__(self, filename, test=False, init=False):
        self.filename = filename
        if init:
            self.first_load(filename)
            self.load_into_pickle(filename) 
        self.data = self.load_from_pickle(filename) 
        if test:
            self.test_data = self.data.loc[:10,:]
        self.count_museums = len(self.data)
    
    def __help__(self):
        print('filename should be without the extension')

    def load_from_pickle(self, filename):
        # loading data from pickle
        data_path = os.path.join(scriptpath, 'data', self.filename+'.pkl')
        data = pd.read_pickle(str(data_path))
        return data

    def load_into_pickle(self, filename):
        # loading data into pickle to save processing time
        
        data_path = os.path.join(scriptpath, 'data', self.filename+'.xlsx')
        data = pd.read_excel(io = str(data_path))
        
        pickle_data_path = os.path.join(scriptpath, 'data', self.filename+'.pkl')
        pd.to_pickle(data, str(pickle_data_path))
        
    def first_load(self, filename):
        # loading data from the excel file directly
        data_path = os.path.join(scriptpath, 'data', self.filename+'.xlsx')
        data = pd.read_excel(io=str(data_path))
        return data
    
    
