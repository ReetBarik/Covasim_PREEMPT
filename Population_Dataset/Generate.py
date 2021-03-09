# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:03:01 2021

@author: reetb
"""

import covasim as cv
import networkx as nx 

pars = dict(
    pop_size = 100,
    pop_type = 'hybrid',
    location = 'Japan',
    # pop_infected = 100,
    start_day = '2020-01-01',
    end_day = '2020-01-31'
)

sim = cv.Sim(pars)
sim.run(until='2020-01-10')
sim.save('Japan100kV0.sim')
# sim = cv.load('Japan100kV12.sim')

# fig = sim.people.plot().savefig('fig.png')

G = nx.Graph()
G.add_nodes_from(sim.people.uid)

layers = ['h', 's', 'c', 'w']

for layer in layers:
	contacts = sim.people.contacts[layer]

	for i in range(len(contacts)):
		p1 = contacts['p1'][i]
		p2 = contacts['p2'][i]

		probability = sim.pars['beta_layer'][layer] * sim.pars['beta'] * sim.people.rel_trans[p1] * sim.people.rel_sus[p2]

		if (G.has_edge(p1,p2)):
			G.add_edge(p1, p2, weight = max(G[p1][p2]['weight'],'{:.6f}'.format(probability)))
		else:
			G.add_edge(p1, p2, weight = '{:.6f}'.format(probability))

nx.write_weighted_edgelist(G, "Japan_100k_V0.edgelist")


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



