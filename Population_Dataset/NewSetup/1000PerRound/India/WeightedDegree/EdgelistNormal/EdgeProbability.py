# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:36:04 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/Covasim_PREEMPT/Population_Dataset/EdgelistNormal/')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = []

for i in range(0,13):
    filename = 'Japan_100k_V' + str(i) + '.edgelist'
    
    df.append(pd.read_csv(filename, sep = ' ', header = None))
    
    
columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']

probs = pd.DataFrame(columns=columns)


for i in range(0,13):
    probs[columns[i]] = df[i][2]
    
#ylim = max(max(probs['V0']), max(probs['V1']), max(probs['V2']), max(probs['V3']), max(probs['V4']), max(probs['V5']), max(probs['V6']), max(probs['V8']), max(probs['V9']), max(probs['V10']), max(probs['V11']), max(probs['V12']))


####################### Sorted Edge Probabilities ########################
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_ylim(0, 1)
        ax[i, j].plot(l)
        
        
fig.suptitle('Edge Probability distributions', fontsize=15)
fig.text(0.5, 0.03, 'Edges', ha='center')
fig.text(0.04, 0.5, 'Probability', va='center', rotation='vertical')
        
plt.savefig('ProbabilitiesSorted.png', dpi = 500)

###########################################################################


###################### Un-Sorted Edge Probabilities #######################
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(probs['V' + str(idx)])
        x = probs.index
        ax[i, j].set_ylim(0, 1)
        ax[i, j].scatter(x,y,s=0.01)
        
        
fig.suptitle('Edge Probability distributions', fontsize=15)
fig.text(0.5, 0.03, 'Edges', ha='center')
fig.text(0.04, 0.5, 'Probability', va='center', rotation='vertical')
        
plt.savefig('Probabilities.png', dpi = 500)

###########################################################################


###################### Probabilities as Violin PLots ######################

ax = sns.violinplot(data=probs)
ax.set_title('Edge Probability distributions for 12 vaccination rounds')
ax.set_xlabel('Vaccination Round')
ax.set_ylabel('Edge Probability')
        
plt.savefig('ProbabilitiesViolin.png', dpi = 500)

###########################################################################



