# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:03:01 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\Covasim_PREEMPT\\Population_Dataset\\NewSetup\\1000PerRound\\PREEMPT\\AttributeEmbedding')

import covasim as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import stellargraph as sg
from stellargraph import StellarGraph
from stellargraph.data import EdgeSplitter
from stellargraph.mapper import GraphSAGELinkGenerator
from stellargraph.mapper import GraphSAGENodeGenerator
from stellargraph.layer import GraphSAGE, link_classification
from stellargraph.data import UniformRandomWalk
from stellargraph.data import UnsupervisedSampler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from tensorflow import keras
from sklearn import preprocessing, feature_extraction, model_selection
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.metrics import accuracy_score

from stellargraph import globalvar

from stellargraph import datasets
from IPython.display import display, HTML


edgelist = 'Seattle100kTopology.edgelist'
simfile = 'Seattle100kV0.sim'

edges = pd.read_csv(edgelist, sep = ' ', header = None)
edges = edges.rename(columns={0: "source", 1: "target"})

sim = cv.load(simfile)

nodeID = sim.people.uid
age = sim.people.age
sex = sim.people.sex
symp_prob = sim.people.symp_prob
severe_prob = sim.people.severe_prob
crit_prob = sim.people.crit_prob
death_prob = sim.people.death_prob
rel_trans = sim.people.rel_trans
rel_sus = sim.people.rel_sus

feature_dict = {'age': age, 'sex': sex, 'symp_prob': symp_prob, 'severe_prob': severe_prob, 'crit_prob': crit_prob, 'death_prob': death_prob, 'rel_trans': rel_trans, 'rel_sus': rel_sus}

features = pd.DataFrame(feature_dict, index = nodeID)

G = StellarGraph(features, edges)

nodes = list(G.nodes())
number_of_walks = 1
length = 5


unsupervised_samples = UnsupervisedSampler(G, nodes=nodes, length=length, number_of_walks=number_of_walks)

batch_size = 50
epochs = 4
num_samples = [10, 5]

generator = GraphSAGELinkGenerator(G, batch_size, num_samples)
train_gen = generator.flow(unsupervised_samples)

layer_sizes = [50, 50]
graphsage = GraphSAGE(layer_sizes=layer_sizes, generator=generator, bias=True, dropout=0.0, normalize="l2")

x_inp, x_out = graphsage.in_out_tensors()

prediction = link_classification(output_dim=1, output_act="sigmoid", edge_embedding_method="ip")(x_out)

model = keras.Model(inputs=x_inp, outputs=prediction)

model.compile(optimizer=keras.optimizers.Adam(lr=1e-3), loss=keras.losses.binary_crossentropy, metrics=[keras.metrics.binary_accuracy])

history = model.fit(train_gen, epochs=epochs, verbose=1, use_multiprocessing=False, workers=4, shuffle=True)

x_inp_src = x_inp[0::2]
x_out_src = x_out[0]
embedding_model = keras.Model(inputs=x_inp_src, outputs=x_out_src)

node_ids = nodeID
node_gen = GraphSAGENodeGenerator(G, batch_size, num_samples).flow(node_ids)

node_embeddings = embedding_model.predict(node_gen, workers=4, verbose=1)

np.savetxt('SeattleEmbedding50Dim.txt', node_embeddings)






