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


rbo_pr = []
rbo_deg = []

#intersection_pr = []
#intersection_deg = []

for i in range(0,13):
    
    edgelist = 'EdgelistPREEMPT/Seattle_100k_PREEMPT_V' + str(i) + '.edgelist'
    seedFile = 'Seeds/Seattle_100k_V' + str(i) + '.json'
    
    with open(seedFile) as json_file: 
        data = json.load(json_file)

    seeds = list(data[0]['Seeds'])
    
    G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)    
    pr = nx.pagerank(G, alpha=0.9, weight = 'weight')
    
    pr = dict(sorted(pr.items(), key=lambda item: item[1]))
    pr_seeds = list(pr.keys())[0: len(seeds)]
    
    deg = sorted(G.degree, key=lambda x: x[1], reverse=True)
    deg_seeds = deg[0: len(seeds)]
    
    rbo_deg.append(rbo.RankingSimilarity(seeds, deg_seeds).rbo())
    rbo_pr.append(rbo.RankingSimilarity(seeds, pr_seeds).rbo())
    
    
#    intersection_pr.append(len((set(seeds).intersection(set(pr_seeds)))))
#    intersection_deg.append(len((set(seeds).intersection(set(deg_seeds)))))
    
#rbo_pr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0003972529920421939, 0.0008147343480988579, 0.0008521962966575607, 0.0006212807360828052, 0.0, 0.0, 0.001496387630903626, 0.0008151047966242855]
#rbo_deg = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    
