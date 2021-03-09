# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:36:04 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/Covasim_PREEMPT/Population_Dataset/Edgelists/')

import pandas as pd

df = []

for i in range(0,13):
    filename = 'Japan_100k_V' + str(i) + '.edgelist'
    
    df.append(pd.read_csv(filename, sep = ' ', header = None))
    
    
columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']

probs = pd.DataFrame(columns=columns)


for i in range(0,13):
    probs[columns[i]] = df[i][2]
    
    
for i in range(1,13):
    print(probs['V0'].equals(probs[columns[i]]))
    

    
    
