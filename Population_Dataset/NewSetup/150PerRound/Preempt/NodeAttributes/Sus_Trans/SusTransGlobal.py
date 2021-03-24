# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:48:33 2021

@author: reetb
"""

#import os
#os.chdir('C:/Users/reetb/Desktop/Covasim_PREEMPT/Population_Dataset/')


import pandas as pd
import matplotlib.pyplot as plt
import json
import covasim as cv

columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']

sus = pd.DataFrame(columns=columns)
trans = pd.DataFrame(columns=columns)


for i in range(0,13):
    
    df_sus = []
    df_trans = []
    
#    seedFile = '../../Seeds/Japan_100k_V' + str(i) + '.json'
    simFile = '../../Sims/Japan100kV' + str(i) + '.sim'
    
    sim = cv.load(simFile)
    
    for p in range(len(sim.people)):
        df_sus.append(sim.people.rel_sus[p])
        df_trans.append(sim.people.rel_trans[p])
        
    sus[columns[i]] = df_sus
    trans[columns[i]] = df_trans
    
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(sus['V' + str(idx)])
#        ax[i, j].set_ylim(0, ylim)
        ax[i, j].hist(y)
        
        
fig.suptitle('Global Susceptibility', fontsize=15)
fig.text(0.5, 0.03, 'rel_sus', ha='center')
fig.text(0.04, 0.5, '#Nodes', va='center', rotation='vertical')
        
plt.savefig('SusceptibilityGlobal.png', dpi = 500)


fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(trans['V' + str(idx)])
#        ax[i, j].set_ylim(0, ylim)
        ax[i, j].hist(y)
        
        
fig.suptitle('Global Transmissibility', fontsize=15)
fig.text(0.5, 0.03, 'rel_trans', ha='center')
fig.text(0.04, 0.5, '#Nodes', va='center', rotation='vertical')
        
plt.savefig('TransmissibilityGlobal.png', dpi = 500)
    
    