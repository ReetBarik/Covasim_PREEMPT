# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 18:12:06 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\Degree\\CommunityDetection')

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
#import covasim as cv
import numpy as np
import json


def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]
    
comm = read_integers('Seattle100kTopology.edgelist_clustInfo')
comm_size = Counter(comm)
size = []
for i in range(0,12):
    size.append(comm_size[i] / 1000)
    
columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
cases = pd.DataFrame(columns=columns)

infected_before = set()

for i in range(0,12):
    
    simfile = '../Sims/Seattle100kV' + str(i) + '.sim'
    sim = cv.load(simfile)
    
    curr_infected = set(np.where(sim.people['infectious'] == True)[0])
    
    new_infections = []
    l = []
    
    for p in curr_infected:
        if p not in infected_before:
           new_infections.append(p)
           infected_before.add(p)
           
    for c in list(comm_size.keys()):
        count = 0
        for p in new_infections:
            if (comm[p] == c):
                count += 1
                
        l.append(count * 100 / len(new_infections))
        
    cases[columns[i]] = l
            
    
cases.to_csv('CommCases.csv', index=False)


cases = pd.read_csv('CommCases.csv')


######################################## Correlation ################################################

fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
#        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_ylim(0, 15)
        ax[i, j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        ax[i, j].set_xticklabels(['0','','','','','5','','','','','10',''])
        
        ax[i, j].plot(size, marker = 'o', alpha = 0.4, markersize = 3, color = 'blue')
        ax2 = ax[i, j].twinx()
        ax2.set_ylim(0, 15)
        if (j < 3):
            ax2.axes.yaxis.set_visible(False)
        ax2.plot(cases['V' + str(idx)], marker = 'o', alpha = 0.4, markersize = 3, color = 'red')
        
        
        
fig.suptitle('Community Cases vs Size (Degree)', fontsize=15)
fig.text(0.5, 0.03, 'Communities (total = 12)', ha='center')
fig.text(0.04, 0.5, 'Comm Size (%)', va='center', c='blue', rotation='vertical')
fig.text(0.96, 0.5, 'Fraction of new cases in Comm v total (%) ', va='center', c='red', rotation='vertical')
        
plt.savefig('CommD5.png', dpi = 500)


########################################## Discrepancy ################################################

fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        
        ax[i, j].set_ylim(-3, 3)
        ax[i, j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        ax[i, j].set_xticklabels(['0','','','','','5','','','','','10',''])
        
        lst = []
        for k in range(len(size)):
            lst.append(size[k] - cases['V' + str(idx)][k])
            
        ax[i, j].plot(lst, marker = 'o', alpha = 0.4, markersize = 3, color = 'blue')
        
fig.suptitle('Cases v Community size Discrepancy (Degree)', fontsize=15)
fig.text(0.5, 0.03, 'Communities (total = 12)', ha='center')
fig.text(0.04, 0.5, 'Diff in % of Comm size - case belonging', va='center', c='blue', rotation='vertical')

plt.savefig('CommD6.png', dpi = 500)


########################################### Overlay ####################################################


probs = pd.DataFrame(columns=columns)

for i in range(0,12):
    
    seedfile = '../Seeds/Seattle100kSeedsV' + str(i) + '.txt'
        
    seeds = read_integers(seedfile)
    
    l = []
    for s in seeds:
        l.append(comm[s])
        
    probs[columns[i]] = l
    
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        
        ax[i, j].set_ylim(-3, 3)
        ax[i, j].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
        ax[i, j].set_xticklabels(['0','','','','','5','','','','','10',''])
        
        l1 = Counter(probs['V' + str(idx)])
        comm_s = []
        for k in range(0,12):
            comm_s.append(l1[k] / 10)
        
        lst = []
        for k in range(len(size)):
            lst.append(size[k] - cases['V' + str(idx)][k])
            
        lst2 = []
        for l in range(len(comm_s)):
            lst2.append(size[l] - comm_s[l])
            
        ax[i, j].plot(lst, marker = 'o', alpha = 0.4, markersize = 3, color = 'blue')
        ax[i, j].plot(lst2, marker = 'o', alpha = 0.4, markersize = 3, color = 'red')
        
fig.suptitle('Cases and seeds v Community size Discrepancy (Degree)', fontsize=12)
fig.text(0.5, 0.03, 'Communities (total = 12)', ha='center')
fig.text(0.04, 0.5, 'Cases v Comm Size discrepancy', va='center', c='blue', rotation='vertical')
fig.text(0.94, 0.5, 'Seed Community discrepancy', va='center', c='red', rotation='vertical')

plt.savefig('CommD7.png', dpi = 500)
    



































    
    
    
    
