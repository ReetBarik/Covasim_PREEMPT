# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:41:30 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
import networkx as nx

columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
probMean = pd.DataFrame(columns=columns)
probStdDev = pd.DataFrame(columns=columns)

probMean = []

for i in range(0,13):
    
    edgelist = 'EdgelistPREEMPT/Seattle_100k_PREEMPT_V' + str(i) + '.edgelist'
        
#    seeds = list(range(0,100000))
    
    G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)  
    
    avg = []
    std = []
    
    for seed in G.nodes():
        l1 = []
        for n in G[seed]:
            l1.append(G[seed][n]['weight'])
        avg.append(np.mean(l1))
        std.append(np.std(l1))
        
        
    probMean.append(avg)
#    probStdDev[columns[i]] = std
    
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
#        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_xlim(0, 0.1)
        ax[i, j].set_ylim(0, 90000)
#        ax[i, j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
#        ax[i, j].set_xticklabels(['0','','','','','5','','','','','10',''])
        
        ax[i, j].hist(probMean[idx])
        
        
        
fig.suptitle('Nbhd prob Histogram (Non-Seed)', fontsize=15)
fig.text(0.5, 0.03, 'Mean nbhd Probability', ha='center')
fig.text(0.02, 0.5, '#Nodes', va='center', c='black', rotation='vertical')
#fig.text(0.96, 0.5, 'Fraction of new cases in Comm v total (%) ', va='center', c='red', rotation='vertical')
        
plt.savefig('NbhdProbHistNonSeed.png', dpi = 500)