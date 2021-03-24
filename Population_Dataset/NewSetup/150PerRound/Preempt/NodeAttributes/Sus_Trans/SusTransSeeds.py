# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 15:19:31 2021

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
    
    seedFile = '../../Seeds/Japan_100k_V' + str(i) + '.json'
    simFile = '../../Sims/Japan100kV' + str(i) + '.sim'
    
    with open(seedFile) as json_file: 
        data = json.load(json_file)

    seeds = list(data[0]['Seeds'])
    sim = cv.load(simFile)
    
    for seed in seeds:
        df_sus.append(sim.people.rel_sus[seed])
        df_trans.append(sim.people.rel_trans[seed])
        
    sus[columns[i]] = df_sus
    trans[columns[i]] = df_trans
    
ylim = max(max(sus['V0']), max(sus['V1']), max(sus['V2']), max(sus['V3']), max(sus['V4']), max(sus['V5']), max(sus['V6']), max(sus['V8']), max(sus['V9']), max(sus['V10']), max(sus['V11']), max(sus['V12']))
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(sus['V' + str(idx)])
        x = sus.index
        ax[i, j].set_ylim(0, ylim)
        ax[i, j].scatter(x,y,s=0.1)
        
        
fig.suptitle('Seed Susceptibility', fontsize=15)
fig.text(0.5, 0.03, 'Seeds', ha='center')
fig.text(0.04, 0.5, 'rel_sus', va='center', rotation='vertical')
        
plt.savefig('Susceptibility.png', dpi = 500)


ylim = max(max(trans['V0']), max(trans['V1']), max(trans['V2']), max(trans['V3']), max(trans['V4']), max(trans['V5']), max(trans['V6']), max(trans['V8']), max(trans['V9']), max(trans['V10']), max(trans['V11']), max(trans['V12']))

fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(trans['V' + str(idx)])
        x = sus.index
        ax[i, j].set_ylim(0, ylim)
        ax[i, j].scatter(x,y,s=5)
        
        
fig.suptitle('Seed Transmissibility', fontsize=15)
fig.text(0.5, 0.03, 'Seeds', ha='center')
fig.text(0.04, 0.5, 'rel_trans', va='center', rotation='vertical')
        
plt.savefig('Transmissibility.png', dpi = 500)
    
    