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
# 0 for PREEMPT, 1 for Random, and 2 for Degree
choice = 2


# Seeds based on Weighted Degree
def generateDegreeSeeds(version):

	edgelist = 'EdgelistDegree/Seattle_100k_Degree_V' + str(version) + '.edgelist'
	G = nx.read_weighted_edgelist(edgelist, nodetype = int, create_using = nx.DiGraph)

	deg = {}

	for n in list(G.nodes()):
		w = 0
		for s in G[n]:
			w += G[n][s]['weight']
		deg[n] = w

	deg = dict(sorted(deg.items(), reverse = True, key=lambda item: item[1]))
	seeds = list(deg.keys())[0:1000]
	
	np.savetxt('Seattle100kSeedsV' + str(version) + '.txt', seeds, fmt='%d', delimiter=' ')

	return seeds

# PREEMPT prescribed seeds
def generateSeeds(version):

	filename = 'Seattle_100k_V' + str(version) + '.json'         

	with open(filename) as json_file: 
		data = json.load(json_file)

	seeds = list(data[0]['Seeds'])

	return seeds

# Random seeds
def generateRandomSeeds(version):

	r_seeds = [0,1,2,3,4,5,6,7,8,9,10,11,12]
	random.seed(a = r_seeds[version])

	filename = 'Vaccinated.txt'
	previousSeeds = set(read_integers(filename))
	seeds = []

	while (len(seeds) < 150):
		seed = randrange(100000)
		if (seed not in previousSeeds):
			seeds.append(seed)
			previousSeeds.add(seed)

	with open(filename, 'w') as filehandle:
		filehandle.writelines("%s\n" % s for s in previousSeeds)

	return seeds

# Returns a dict of node indices as key and their probability of getting vaccinated as values
def vaccinateSeeds(sim, seeds):
	inds = sim.people.uid
	vals = np.zeros(len(sim.people))

	# set of seeds chosen by PREEMPT to have a 100% probability of getting vaccinated
	for seed in seeds:
		vals[seed] = 1.0

	output = dict(inds=inds, vals=vals)
	return output

# Load the sim
sim2 = cv.load('Seattle100kV' + str(version) + '.sim')

if (choice == 0):
	seeds = generateSeeds(version)
if (choice == 1):
	seeds = generateRandomSeeds(version)
if (choice == 2):
	seeds = generateDegreeSeeds(version)

# Define the vaccine and add it to the sim
vaccine =  cv.simple_vaccine(days=31 + (version * 7), rel_sus=0.0, rel_symp=0.02, subtarget=vaccinateSeeds(sim2, seeds))
vaccine.vaccinations = vaccine.subtarget['vals'].astype(int)
vaccine.initialize(sim2)
sim2.pars['interventions'].append(vaccine)

# setting 'rel_trans' od vaccinated seeds ensure edge probability on outgoing edges are set to zero
for seed in seeds:
	sim2.people.rel_trans[seed] = 0.0

# Let it run for a week
sim2.run(until='2020-04-30')
# Save the sim
sim2.save('Seattle100kV' + str(version + 1) + '.sim')