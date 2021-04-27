# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:56:08 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT\\CommunityDetection')

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import json
import covasim as cv

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]
    
comm = read_integers('Seattle100kTopology.edgelist_clustInfo')
comm_size = Counter(comm)
size = []
for i in range(0,12):
    size.append(comm_size[i] / 1000)
    
    
columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
comm_avg = pd.DataFrame(columns=columns)
seed_avg = pd.DataFrame(columns=columns)

for i in range(0,13):
    
    seedfile = '../Seeds/Seattle_100k_V' + str(i) + '.json'
    
    with open(seedfile) as json_file: 
        data = json.load(json_file)
        
    seeds = list(data[0]['Seeds'])
    l = []
    for s in seeds:
        l.append(comm[s])
        
    l = Counter(l)
    
    simfile = '../Sims/Seattle100kV' + str(i) + '.sim'
    sim = cv.load(simfile)
    
    sus_comm_avg = []
    sus_seed_avg = []
    
    for c in range(len(comm_size)):
        avg_comm = 0
        avg_seed = 0
        for p in range(len(sim.people)):
            if (comm[p] == c):
#                avg_comm += sim.people['rel_sus'][p]
                if (sim.people['infectious'][p]):
                    avg_comm += 1
                if (p in seeds):
#                    avg_seed += sim.people['rel_sus'][p]
                    if (sim.people['infectious'][p]):
                        avg_seed += 1
                    
        sus_comm_avg.append(avg_comm / comm_size[c])
        if (avg_seed != 0):
            sus_seed_avg.append(avg_seed / l[c])
        else: 
            sus_seed_avg.append(0)
            
            
    comm_avg[columns[i]] = sus_comm_avg
    seed_avg[columns[i]] = sus_seed_avg
    
    
comm_avg.to_csv('CommAvgInf.csv', index=False)
seed_avg.to_csv('SeedAvgInf.csv', index=False)




#comm_avg = pd.read_csv('CommAvgInf.csv')
#seed_avg = pd.read_csv('SeedAvgInf.csv')
#
#
#fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')
#
#for i in range(3):
#    for j in range(4):
#        idx = 4 * i + j
#
#        ax[i, j].set_ylim(0, 20)
#
#        ax[i, j].plot(size, alpha = 0.3, color = 'blue')
#        ax2 = ax[i, j].twinx()
#        ax2.set_ylim(0, 0.3)
#        if (j < 3):
#            ax2.axes.yaxis.set_visible(False)
#        ax2.plot(seed_avg['V' + str(idx)], alpha = 0.75, color = 'green')
#        ax2.plot(comm_avg['V' + str(idx)], alpha = 0.75, color = 'red')
#        
#        
#        
#fig.suptitle('Seed Community Infectious (PREEMPT)', fontsize=15)
#fig.text(0.5, 0.03, 'Communities (total = 12)', ha='center')
#fig.text(0.04, 0.5, 'Comm Size (%)', va='center', c='blue', rotation='vertical')
#fig.text(0.96, 0.25, 'Infectious Frac Comm', va='center', c='red', rotation='vertical')
#fig.text(0.96, 0.75, 'Infectious Frac Seeds', va='center', c='green', rotation='vertical')
#        
#plt.savefig('Inf.png', dpi = 500)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        