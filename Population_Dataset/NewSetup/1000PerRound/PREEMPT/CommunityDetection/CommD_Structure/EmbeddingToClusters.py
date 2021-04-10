# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 12:57:45 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT\\CommunityDetection\\CommD_Structure')


import pandas as pd
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt


embeddingFile = 'Seattle100kTopology.edgelist.emb'
with open(embeddingFile, 'r') as file:
    data = file.read().replace('\n', ',')
    
    
data = data.split(',')                          # Splits the different lines

for i in range(len(data)):
    data[i] = data[i].split(' ')                # Splits the lines into a list of tokens
    
data.pop(0)                                     # First line popped (containes #nodes and #dim)
data.pop(-1)                                    # Last line popped (contains empty string)

def node(e):
    return int(e[0],10)

data.sort(key = node)                           # Sort according to vertex index

for i in range(len(data)):
    data[i].pop(0)
    data[i] = [float(x) for x in data[i]]       # data[i] contains embedding of vertex i indexed from 0
    
x = []
y = []
z = []

for i in range(len(data)):
    x.append(data[i][0])
    y.append(data[i][1])
    z.append(data[i][2])
    
    
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(xs = x, ys = y, zs = z, s = 0.01)

fig.savefig('EmbeddingViz.png', dpi = 500)

db = DBSCAN(eps=0.01, min_samples=10).fit(data)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)


colors = np.random.rand(len(labels),3)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(xs = x, ys = y, zs = z, c = colors[labels], s = 0.01)

fig.savefig('EmbeddingVizClustered.png', dpi = 500)























