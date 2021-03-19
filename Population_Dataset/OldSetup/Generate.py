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
    pop_size = 100000,
    pop_type = 'hybrid',
    location = 'Japan',
    # pop_infected = 100,
    start_day = '2020-01-01',
    end_day = '2020-04-30'
)

# sim = cv.Sim(pars)
# sim.run(until='2020-01-30')
# sim.save('Japan100kV' + str(version) + '.sim')
sim = cv.load('Japan100kV' + str(version) + '.sim')

# fig = sim.people.plot().savefig('fig.png')

G = nx.DiGraph()
G.add_nodes_from(sim.people.uid)

layers = ['h', 's', 'c', 'w']

for layer in layers:
	contacts = sim.people.contacts[layer]

	for i in range(len(contacts)):
		p1 = contacts['p1'][i]
		p2 = contacts['p2'][i]

		probabilityP1_P2 = sim.pars['beta_layer'][layer] * sim.pars['beta'] * sim.people.rel_trans[p1] * sim.people.rel_sus[p2]
		probabilityP2_P1 = sim.pars['beta_layer'][layer] * sim.pars['beta'] * sim.people.rel_trans[p2] * sim.people.rel_sus[p1]

		if (probabilityP1_P2 > 1):
			probabilityP1_P2 = 1

		if (probabilityP2_P1 > 1):
			probabilityP2_P1 = 1

		if (G.has_edge(p1,p2)):
			G.add_edge(p1, p2, weight = max(G[p1][p2]['weight'],'{:.6f}'.format(probabilityP1_P2)))
			
		else:
			G.add_edge(p1, p2, weight = '{:.6f}'.format(probabilityP1_P2))
			
		if (G.has_edge(p2,p1)):
			G.add_edge(p2, p1, weight = max(G[p2][p1]['weight'],'{:.6f}'.format(probabilityP2_P1)))
			
		else:
			G.add_edge(p2, p1, weight = '{:.6f}'.format(probabilityP2_P1))

nx.write_weighted_edgelist(G, 'Japan_100k_V' + str(version) + '.edgelist')

removeNodes = np.where(sim.people['rel_sus'] == 0)[0]

for node in removeNodes:
	G.remove_node(node)

nx.write_weighted_edgelist(G, 'Japan_100k_PREEMPT_V' + str(version) + '.edgelist')

# import covasim as
# cv sim = cv.Sim(start_day='2021-01-01', end_day='2021-04-01')
# sim.run()
# window_start = '2021-02-01'
# window_end = '2021-03-01'
# infected_after  = sim.people.date_exposed >= sim.day(window_start) # Convert date string to day number and check when people were infected
# infected_before = sim.people.date_exposed < sim.day(window_end) 
# infected_in_window = cv.true(infected_after * infected_before) # Convert the boolean array into a list of indices; 
#                                                                # * is equivalent to np.logical_and() here
# print(len(infected_in_window))



