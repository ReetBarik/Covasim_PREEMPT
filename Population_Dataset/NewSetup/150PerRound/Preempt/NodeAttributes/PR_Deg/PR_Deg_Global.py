# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 13:28:59 2021

@author: reetb
"""

#import os
#os.chdir('C:/Users/reetb/Desktop/Covasim_PREEMPT/Population_Dataset//NodeAttributes/PR_Deg/')

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import json


columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']

pr_seeds = pd.DataFrame(columns=columns)
deg_seeds = pd.DataFrame(columns=columns)

vaccinated = set()

for i in range(0,13):
    
    df_pr = []
    df_deg = []
    
    edgelist = '../../EdgelistPREEMPT/Japan_100k_PREEMPT_V' + str(i) + '.edgelist'
    seedFile = '../../Seeds/Japan_100k_V' + str(i) + '.json'
    
    for v in vaccinated:
        df_pr.append(0)
        df_deg.append(0)
    
    with open(seedFile) as json_file: 
        data = json.load(json_file)
    
    seeds = list(data[0]['Seeds'])
    for seed in seeds:
        vaccinated.add(seed)
    
    G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)    
    pr = nx.pagerank(G, alpha=0.9, weight = 'weight')
    
    for p in list(G.nodes()):
        df_pr.append(pr[p])
        df_deg.append(G.degree(p))
        
        
    pr_seeds[columns[i]] = df_pr
    deg_seeds[columns[i]] = df_deg

    
#ylim = max(max(pr_seeds['V0']), max(pr_seeds['V1']), max(pr_seeds['V2']), max(pr_seeds['V3']), max(pr_seeds['V4']), max(pr_seeds['V5']), max(pr_seeds['V6']), max(pr_seeds['V8']), max(pr_seeds['V9']), max(pr_seeds['V10']), max(pr_seeds['V11']), max(pr_seeds['V12']))
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(pr_seeds['V' + str(idx)])
#        x = pr_seeds.index
#        ax[i, j].set_ylim(0, ylim)
#        ax[i, j].scatter(x,y,s=0.1)
        ax[i, j].hist(y)
        
fig.suptitle('Global Pagerank Histogram', fontsize=15)
fig.text(0.5, 0.03, 'Pagerank', ha='center')
fig.text(0.04, 0.5, '#Nodes', va='center', rotation='vertical')
        
plt.savefig('PagerankGlobal.png', dpi = 500)


#ylim = max(max(deg_seeds['V0']), max(deg_seeds['V1']), max(deg_seeds['V2']), max(deg_seeds['V3']), max(deg_seeds['V4']), max(deg_seeds['V5']), max(deg_seeds['V6']), max(deg_seeds['V8']), max(deg_seeds['V9']), max(deg_seeds['V10']), max(deg_seeds['V11']), max(deg_seeds['V12']))
    
fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
        y = list(deg_seeds['V' + str(idx)])
#        x = pr_seeds.index
#        ax[i, j].set_ylim(0, ylim)
#        ax[i, j].scatter(x,y,s=0.1)
        ax[i, j].hist(y)
        
        
fig.suptitle('Global Degree Histogram', fontsize=15)
fig.text(0.5, 0.03, 'Degree', ha='center')
fig.text(0.04, 0.5, '#Nodes', va='center', rotation='vertical')
        
plt.savefig('DegreeGlobal.png', dpi = 500)

