import pandas as pd 
import numpy as np 


def compte_reg(base,seuil):
    dic={}
    for id,row in base.iterrows():
        case=base.loc[id, 'Région']
        if case not in dic.keys():
            dic[case]=1
        elif case in dic.keys():
            dic[case]+=1
    autre=0  
    n=len(dic)
    values= list(dic.values())
    keys=list(dic.keys() )     
                
    for i in range(n):
        
        if values[i]< seuil :
            autre+= values[i]
            del dic[keys[i]]
    dic['autre']=autre
    
    return dic

def region_maximale (base):
    dic=compte_reg (base,0)
    inverse=[(value,key) for key, value in dic.items()]
    rm=max(inverse)[1]
    return rm

def moyenne_festivals (base) :
    dic=compte_reg (base,0)
    l=list(dic.values ())
    n= len (l)
    s=0
    for i in range(n):
        s+=l[i]
    moy= s/n
    return moy    


