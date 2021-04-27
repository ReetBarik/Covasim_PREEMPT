# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 15:10:46 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import networkx as nx

columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
probMean = pd.DataFrame(columns=columns)
probStdDev = pd.DataFrame(columns=columns)

for i in range(0,13):
    
    edgelist = 'EdgelistPREEMPT/Seattle_100k_PREEMPT_V' + str(i) + '.edgelist'
    seedFile = 'Seeds/Seattle_100k_V' + str(i) + '.json'
    
    with open(seedFile) as json_file: 
        data = json.load(json_file)
    
    seeds = list(data[0]['Seeds'])
    
    G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)  
    
    avg = []
    std = []
    
    for seed in seeds:
        l1 = []
        for n in G[seed]:
            l1.append(G[seed][n]['weight'])
        avg.append(np.mean(l1))
        std.append(np.std(l1))
        
        
    probMean[columns[i]] = avg
    probStdDev[columns[i]] = std
    
    
################################### Error Bar ######################################
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
#        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_ylim(0, 0.4)
#        ax[i, j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
#        ax[i, j].set_xticklabels(['0','','','','','5','','','','','10',''])
        
        ax[i, j].errorbar(list(range(0,1000)), probMean['V' + str(idx)], probStdDev['V' + str(idx)], capsize=0.5, elinewidth=0.2, markeredgewidth=0.002)
        
        
        
fig.suptitle('Nbhd prob mean/stddev (PREEMPT)', fontsize=15)
fig.text(0.5, 0.03, 'Seeds (in order of selection)', ha='center')
fig.text(0.04, 0.5, 'Mean nbhd Probability', va='center', c='black', rotation='vertical')
#fig.text(0.96, 0.5, 'Fraction of new cases in Comm v total (%) ', va='center', c='red', rotation='vertical')
        
plt.savefig('NbhdProb.png', dpi = 500)
    

################################### Histogram #######################################

fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
#        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_xlim(0, 0.2)
#        ax[i, j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
#        ax[i, j].set_xticklabels(['0','','','','','5','','','','','10',''])
        
        ax[i, j].hist(probMean['V' + str(idx)])
        
        
        
fig.suptitle('Nbhd prob Histogram (PREEMPT)', fontsize=15)
fig.text(0.5, 0.03, 'Mean nbhd Probability', ha='center')
fig.text(0.04, 0.5, '#Seeds', va='center', c='black', rotation='vertical')
#fig.text(0.96, 0.5, 'Fraction of new cases in Comm v total (%) ', va='center', c='red', rotation='vertical')
        
plt.savefig('NbhdProbHist.png', dpi = 500)


