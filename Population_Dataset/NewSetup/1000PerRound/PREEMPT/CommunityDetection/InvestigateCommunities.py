# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:04:44 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT\\CommunityDetection')

import pandas as pd
import json
import matplotlib.pyplot as plt
from collections import Counter

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]
    
comm = read_integers('Seattle100kTopology.edgelist_clustInfo')
comm_size = Counter(comm)
size = []
for i in range(0,12):
    size.append(comm_size[i] / 1000)

columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
probs = pd.DataFrame(columns=columns)

for i in range(0,12):
    
    seedfile = '../Seeds/Seattle_100k_V' + str(i) + '.json'
    
    with open(seedfile) as json_file: 
        data = json.load(json_file)
        
    seeds = list(data[0]['Seeds'])
    
    l = []
    for s in seeds:
        l.append(comm[s])
        
    probs[columns[i]] = l
    
#ylim = max(max(probs['V0']), max(probs['V1']), max(probs['V2']), max(probs['V3']), max(probs['V4']), max(probs['V5']), max(probs['V6']), max(probs['V8']), max(probs['V9']), max(probs['V10']), max(probs['V11']), max(probs['V12']))    

fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
#        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_ylim(0, 150)
        ax[i, j].hist(probs['V' + str(idx)], edgecolor='black', bins = 12, color = 'blue')
        ax2 = ax[i, j].twinx()
        ax2.set_ylim(0, 100)
        if (j < 3):
            ax2.axes.yaxis.set_visible(False)
        ax2.plot(size, color = 'red')
        
        
        
fig.suptitle('Seed Community Histogram (PREEMPT)', fontsize=15)
fig.text(0.5, 0.03, 'Communities (total = 12)', ha='center')
fig.text(0.04, 0.5, '#Seeds', va='center', c='blue', rotation='vertical')
fig.text(0.96, 0.5, 'Comm Size (%)', va='center', c='red', rotation='vertical')
        
plt.savefig('CommD.png', dpi = 500)