import os.path
from pathlib import Path 
scriptpath = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as pyplot

class load_data:
    """ 
    This class will be used to extract useful data from the database, clean it
    and divide it into smaller dataframes for future use  
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
            self.test_data = self.data.loc[10,:]
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

if __name__ == '__main__':
    #primary_test
    museums = load_data(filename='festivals',test=True)
    df = museums.data
    test_df = museums.test_data
    print(df)

def compte_dep(base):
    dic={}
    for i in range(len(base)):
        row=base.loc[i]
        case=row["Nom Département"]
        if case not in dic.keys():
            dic[case]=1
        elif case in dic.keys():
            dic[case]+=1
    return dic
print(compte_dep(df))

di={"entre 0 et 5":0, "entre 5 et 10":0, "entre 10 et 20":0, "entre 20 et 50":0, "entre 50 et 100":0, "plus de 100":0}
for cle in compte_dep(df).keys():
    if compte_dep(df)[cle]<=5:
        di["entre 0 et 5"]+=1
    elif compte_dep(df)[cle]>5 and compte_dep(df)[cle]<=10:
        di["entre 5 et 10"]+=1
    elif compte_dep(df)[cle]>10 and compte_dep(df)[cle]<=20:
        di["entre 10 et 20"]+=1
    elif compte_dep(df)[cle]>20 and compte_dep(df)[cle]<=50:
        di["entre 20 et 50"]+=1
    elif compte_dep(df)[cle]>50 and compte_dep(df)[cle]<=100:
        di["entre 50 et 100"]+=1
    elif compte_dep(df)[cle]>100:
        di["plus de 100"]+=1
#print(di)
di = {'de 0 à 5': 7, 'de 5 à 10': 13, 'de 10 à 20': 27, 'de 20 à 50': 40, 'de 50 à 100': 14, 'plus de 100': 2}
legendes=list(di.keys())
valeurs=list(di.values())
pyplot.figure(figsize = (12, 6))
x=valeurs
pyplot.bar(legendes, x, width=0.8, color=['aqua', 'skyblue', 'cornflowerblue', 'dodgerblue', 'blue', 'navy'])
pyplot.title("Nombre de départements accueillant entre x et y festivals")
pyplot.show()