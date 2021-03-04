# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 14:03:01 2021

@author: reetb
"""

import covasim as cv
import json 
import numpy as np
import random

def vaccinateSeeds(sim):
	inds = sim.people.uid
	vals = np.zeros(len(sim.people))

	filename = 'Japan_100k_V12.json'

	with open(filename) as json_file: 
		data = json.load(json_file)

	seeds = list(data[0]['Seeds'])

	for seed in seeds:
		vals[seed] = 1.0

	output = dict(inds=inds, vals=vals)
	return output


# sim1 = cv.load('1MonthJapan100k.sim')
sim2 = cv.load('24AprJapan100k.sim')

vaccine =  cv.vaccine(days=115, rel_sus=0.1, rel_symp=0.02, subtarget=vaccinateSeeds(sim2))
vaccine.vaccinations = vaccine.subtarget['vals'].astype(int)
vaccine.initialize(sim2)
sim2.pars['interventions'].append(vaccine)

sim2.run(until='2020-04-30')
sim2.save('30AprJapan100k.sim')

# sim1.label = 'Baseline'
# sim2.label = 'Vaccine'


# msim = cv.MultiSim([sim1, sim2])
# msim.run()
# msim.plot().savefig('plot1.png', dpi = 500)





