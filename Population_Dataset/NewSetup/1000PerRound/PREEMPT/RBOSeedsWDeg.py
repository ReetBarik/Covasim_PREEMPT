# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:33:13 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT')

import pandas as pd
import matplotlib.pyplot as plt
import json
import networkx as nx
import rbo

rboWeightedDegree = []
iouWeightedDegree = []

for i in range(0,13):
    
    edgelist = 'EdgelistPREEMPT/Seattle_100k_PREEMPT_V' + str(i) + '.edgelist'
    seedFile = 'Seeds/Seattle_100k_V' + str(i) + '.json'
    
    deg = {}
    
    with open(seedFile) as json_file: 
        data = json.load(json_file)
    
    seeds = list(data[0]['Seeds'])
    
    G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)
    
    for n in list(G.nodes()):
        w = 0
        for s in G[n]:
            w += G[n][s]['weight']
        deg[n] = w
        
    
    deg = dict(sorted(deg.items(), reverse = True, key=lambda item: item[1]))
    
    degNodes = list(deg.keys())[0:len(seeds)]
    
    rboWeightedDegree.append(rbo.RankingSimilarity(seeds, degNodes).rbo())
    
    seeds = set(seeds)
    
    degNodes = set(degNodes)
    
    iouWeightedDegree.append(len(seeds.intersection(degNodes)) / len(seeds.union(degNodes)))
    
    
#rbo = [0.7757808986277869,0.6313278047243118,0.5538565480523722,0.5216035316880261,0.4783196759812056,0.45037435071649734,0.41123798586736,0.37424130340773243,0.366290139512475,0.37622741568775486,0.34169372670008197,0.34948220961554727,0.3248526375702813]
#iou = [0.6542597187758478,0.5661707126076743,0.5048908954100828,0.45666423889293517,0.4398848092152628,0.4094432699083862,0.3449899125756557,0.31752305665349145,0.3114754098360656,0.32275132275132273,0.28949065119277884,0.2861736334405145,0.2771392081736909]
    
fig, ax = plt.subplots()

ax.plot(rboWeightedDegree, color = 'red', marker = 'o', alpha = 0.75, label ='RBO')
ax.plot(iouWeightedDegree, color = 'blue', marker = 'o', alpha = 0.75, label ='IOU')
ax.legend()
plt.xlabel("Vaccination Rounds")
plt.ylabel("Similarity with PREEMPT")
plt.title("Seed selection similarity b/w PREEMPT & Weighted Degree")

plt.savefig('PREEMPTvWeightedDegSeeds.png', dpi = 500)