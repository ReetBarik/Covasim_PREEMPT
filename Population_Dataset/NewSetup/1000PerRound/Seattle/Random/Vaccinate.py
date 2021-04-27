# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:18:52 2021

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
# 0 for PREEMPT and 1 for Random
choice = 1

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]

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

	while (len(seeds) < 1000):
		seed = randrange(len(sim2.people))
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

# Define the vaccine and add it to the sim
vaccine =  cv.vaccine(days=31 + (version * 7), rel_sus=0.0, rel_symp=0.02, subtarget=vaccinateSeeds(sim2, seeds))
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