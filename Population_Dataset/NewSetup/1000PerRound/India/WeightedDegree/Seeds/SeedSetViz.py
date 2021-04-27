# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:12:57 2021

@author: reetb
"""

#import os
#os.chdir('C:\\Users\\reetb\Desktop\Covasim_PREEMPT\Population_Dataset\NewSetup\1000PerRound\Seeds\')

import json 
from venn import venn
import matplotlib.pyplot as plt


seedSets = {}

s = set()
 
for i in range(0,13):
    filename = 'Seattle_100k_V' + str(i) + '.json'

    with open(filename) as json_file: 
        data = json.load(json_file)
        
    seedSets[i] = set(data[0]['Seeds'])
    
    for j in data[0]['Seeds']:
        s.add(j)

for i in range(0,12):    
    seed = {}

    seed[i] = seedSets[i]
    seed[i + 1] = seedSets[i + 1]
    
    fig, ax = plt.subplots(1, figsize=(16,12))
    venn(seed, ax=ax)
    plt.savefig('set' + str(i) +'.png', dpi = 500)
#plt.legend(labels[:-2], ncol=6)
