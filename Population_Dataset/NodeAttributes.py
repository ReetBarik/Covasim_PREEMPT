# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:04:44 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/Covasim_PREEMPT/Population_Dataset/')
#import sys
import json 
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
#import covasim as cv
#from networkx.algorithms.community import greedy_modularity_communities

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]
    
comm = read_integers('Japan_100k_Community_Unweighted.edgelist_clustInfo')

#version = int(sys.argv[1])

# community_edgelist = 'Japan_100k_Community_V' + str(version) + '.edgelist'

columns = ['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
probs = pd.DataFrame(columns=columns)

for i in range(0,12):

#    edgelist = 'Edgelists/Japan_100k_V' + str(i) + '.edgelist'
    #sim = cv.load('Japan100kV' + str(version) + '.sim')
    #attributefile = 'SimSeedAttr_V' + str(version) + '.json'
    seedfile = '5000SeedsPerRound/PREEMPT/Seeds/Japan_100k_V' + str(i) + '.json'
#    sim = cv.load('Sims/Japan100kV' + str(i) + '.sim')
    
    with open(seedfile) as json_file: 
        data = json.load(json_file)
        
    seeds = list(data[0]['Seeds'])
    
#    G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)
    # H = nx.read_weighted_edgelist(community_edgelist, nodetype = int)
    
#    pr = nx.pagerank(G, alpha=0.9, weight = 'weight')
    #bc = nx.betweenness_centrality(G, weight = 'weight')
    #c = list(greedy_modularity_communities(H, weight = 'weight'))
    
    l = []
    for s in seeds:
        l.append(comm[s])
        
    probs[columns[i]] = l
    print(i)


ylim = max(max(probs['V0']), max(probs['V1']), max(probs['V2']), max(probs['V3']), max(probs['V4']), max(probs['V5']), max(probs['V6']), max(probs['V8']), max(probs['V9']), max(probs['V10']), max(probs['V11']), max(probs['V12']))    

fig, ax = plt.subplots(3, 4, sharex='col', sharey='row')

for i in range(3):
    for j in range(4):
        idx = 4 * i + j
#        l = list(sorted(probs['V' + str(idx)]))
        ax[i, j].set_ylim(0, 600)
        ax[i, j].hist(probs['V' + str(idx)], bins = 23)
        
        
fig.suptitle('Seed Community Histogram', fontsize=15)
fig.text(0.5, 0.03, 'Communities (total = 23)', ha='center')
fig.text(0.04, 0.5, '#Seeds', va='center', rotation='vertical')
        
plt.savefig('CommD.png', dpi = 500)




#layers = ['h', 's', 'c', 'w']
#
#NodeAttributes = {}
#
#for s in seeds:
#    
#    attr = {}
#    attr['pagerank'] = pr[s]
#    attr['outDegree'] = G.out_degree(s)
#    attr['inDegree'] = G.in_degree(s)
#    attr['clusteringCoeff'] = nx.clustering(G, s)
##    attr['betweennessCentrality'] = bc[s]
#
#    transmissibilities = []
#    attr['susceptibility'] = str(sim.people[seed].rel_sus)
#    for l in layers:
#        for c in sim.people[seed].contacts[l]:
#            transmissibilities.append(str(sim.people[int(c)].rel_trans))
#    attr['transmissibilities'] = transmissibilities
#    
#    NodeAttributes[s] = attr
#    
#    with open(attributefile, "w") as outfile:  
#        json.dump(NodeAttributes, outfile)
    
    
    
    