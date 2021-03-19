# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 14:03:01 2021

@author: reetb
"""

import covasim as cv
import json 
import numpy as np
import random
from random import randrange
import networkx as nx
import sys

version = int(sys.argv[1])

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]

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


def vaccinateSeeds(sim):
	inds = sim.people.uid
	vals = np.zeros(len(sim.people))

	# G, maxWeight = return_Graph(sim)
	# for p1,p2 in G.edges():
	# 	G[p1][p2]['weight'] = G[p1][p2]['weight'] / maxWeight

	# nx.write_weighted_edgelist(G, 'Japan_100k_Community_V' + str(version) + '.edgelist')

	filename = 'Japan_100k_V' + str(version) + '.json'

	with open(filename) as json_file: 
		data = json.load(json_file)

	seeds = list(data[0]['Seeds'])

	for seed in seeds:
		vals[seed] = 1.0

	output = dict(inds=inds, vals=vals)
	return output

def vaccinateRandomSeeds(sim):

	r_seeds = [0,1,2,3,4,5,6,7,8,9,10,11,12]
	random.seed(a = r_seeds[version])
	inds = sim.people.uid
	vals = np.zeros(len(sim.people))

	filename = 'Vaccinated.txt'

	previousSeeds = set(read_integers(filename))

	seeds = []

	while (len(seeds) < 5000):
		seed = randrange(len(sim.people))
		if (seed not in previousSeeds):
			seeds.append(seed)
			previousSeeds.add(seed)

	with open(filename, 'w') as filehandle:
		filehandle.writelines("%s\n" % s for s in previousSeeds)

	for seed in seeds:
		vals[seed] = 1.0

	output = dict(inds=inds, vals=vals)
	return output


# sim1 = cv.load('1MonthJapan100k.sim')
sim2 = cv.load('Japan100kV' + str(version) + '.sim')

vaccine =  cv.vaccine(days=31 + (version * 7), rel_sus=0.0, rel_symp=0.02, subtarget=vaccinateRandomSeeds(sim2))
vaccine.vaccinations = vaccine.subtarget['vals'].astype(int)
vaccine.initialize(sim2)
sim2.pars['interventions'].append(vaccine)

# filename = 'Japan_100k_V' + str(version) + '.json'
filename = 'Vaccinated.txt'
# with open(filename) as json_file: 
# 		data = json.load(json_file)

seeds = set(read_integers(filename))

for seed in seeds:
	sim2.people.rel_trans[seed] = 0.0

sim2.run(until='2020-04-30')
sim2.save('Japan100kV' + str(version + 1) + '.sim')

# sim1.label = 'Baseline'
# sim2.label = 'Vaccine'


# msim = cv.MultiSim([sim1, sim2])
# msim.run()
# msim.plot().savefig('plot1.png', dpi = 500)





