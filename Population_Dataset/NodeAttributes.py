# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:04:44 2021

@author: reetb
"""

#import os
#os.chdir('C:/Users/reetb/Desktop/Covasim_PREEMPT/Population_Dataset/')
import sys
import json 
import networkx as nx
#from networkx.algorithms.community import greedy_modularity_communities

version = int(sys.argv[1])

edgelist = 'Japan_100k_V' + str(version) + '.edgelist'

attributefile = 'SimSeedAttr_V' + str(version) + '.json'

with open(attributefile) as json_file: 
		data = json.load(json_file)
        
        
seeds = list(data.keys())

seeds = [int(x) for x in seeds]

G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)

pr = nx.pagerank(G, alpha=0.9, weight = 'weight')
bc = nx.betweenness_centrality(G, weight = 'weight')
#c = list(greedy_modularity_communities(G, weight = 'weight'))

NodeAttributes = {}

for s in seeds:
    
    attr = {}
    attr['pagerank'] = pr[s]
    attr['outDegree'] = G.out_degree(s)
    attr['inDegree'] = G.in_degree(s)
    attr['clusteringCoeff'] = nx.clustering(G, s)
    attr['betweennessCentrality'] = bc[s]
    attr['susceptibility'] = data[str(s)]['susceptibility']
    attr['transmissibilities'] = data[str(s)]['transmissibilities']
    
    NodeAttributes[s] = attr
    
    with open(attributefile, "w") as outfile:  
        json.dump(NodeAttributes, outfile)
    
    
    
    