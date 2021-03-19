# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 14:03:01 2021

@author: reetb
"""

import covasim as cv
import networkx as nx

def return_Graph(sim):

    G = nx.Graph()
    G.add_nodes_from(sim.people.uid)

    layers = ['h', 's', 'c', 'w']

    maxWeight = 0

    for layer in layers:
        contacts = sim.people.contacts[layer]

        for i in range(len(contacts)):
            p1 = contacts['p1'][i]
            p2 = contacts['p2'][i]

            if (G.has_edge(p1,p2)):
                G.add_edge(p1, p2, weight = G[p1][p2]['weight'] + sim.pars['beta_layer'][layer])
                if (maxWeight < G[p1][p2]['weight'] + sim.pars['beta_layer'][layer]):
                	maxWeight = G[p1][p2]['weight'] + sim.pars['beta_layer'][layer]
            else:
                G.add_edge(p1, p2, weight = sim.pars['beta_layer'][layer])
                if (maxWeight < sim.pars['beta_layer'][layer]):
                	maxWeight = sim.pars['beta_layer'][layer]

    return G, maxWeight

sim = cv.load('Japan100kV0.sim')

G, maxWeight = return_Graph(sim)
for p1,p2 in G.edges():
	G[p1][p2]['weight'] = G[p1][p2]['weight'] / maxWeight

# G = nx.convert_node_labels_to_integers(G, first_label = 1)
nx.write_edgelist(G, 'Japan_100k_Community_Unweighted.edgelist', data = False)
nx.write_weighted_edgelist(G, 'Japan_100k_Community.edgelist')