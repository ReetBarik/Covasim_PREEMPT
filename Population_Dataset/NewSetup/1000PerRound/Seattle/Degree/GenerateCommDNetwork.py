# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:03:01 2021

@author: reetb
"""

import covasim as cv
import networkx as nx
import numpy as np
import sys

version = int(sys.argv[1])

pars = dict(
    pop_size = 100000,                                 # Number of nodes
    pop_type = 'hybrid',							   # Hybrid population: household, school, work, community layer
    # location = 'Seattle',								   # Location and demographic based on 2018 Seattle by default 
    # pop_infected = 100,
    start_day = '2020-01-01',						   # Simulation start
    end_day = '2020-04-30'							   # Simulation end
)

sim = cv.Sim(pars)
sim.run(until='2020-01-30')							   # Let it run for the first 30 days
sim.save('Seattle100kV' + str(version) + '.sim')		   # Save the sim
# sim = cv.load('Japan100kV' + str(version) + '.sim')    # Load the sim 


G = nx.Graph()									   	   # Undirected graph because for all (p1, p2) keeping an edge from p1 -> p2 and from p2 -> p1 is redundant
G.add_nodes_from(sim.people.uid)

layers = ['h', 's', 'c', 'w']

for layer in layers:
	contacts = sim.people.contacts[layer]

	for i in range(len(contacts)):
		p1 = contacts['p1'][i]						   # Source
		p2 = contacts['p2'][i]						   # Destination

		G.add_edge(p1, p2)							   # Add the edge just once
			
nx.write_edgelist(G, 'Seattle100kTopology.edgelist', data = False) 