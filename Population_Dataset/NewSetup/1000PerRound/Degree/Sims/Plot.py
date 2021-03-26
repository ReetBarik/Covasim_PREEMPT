import covasim as cv

simB = cv.load('Seattle100kV0.sim')
sim0 = cv.load('Seattle100kV1.sim')
# sim1 = cv.load('Seattle100kV2.sim')
# sim2 = cv.load('Seattle100kV3.sim')
# sim3 = cv.load('Seattle100kV4.sim')
# sim4 = cv.load('6MarSeattle100k.sim')
# sim5 = cv.load('13MarSeattle100k.sim')
# sim6 = cv.load('Seattle100kV7.sim')
# sim7 = cv.load('27MarSeattle100k.sim')
# sim8 = cv.load('3AprSeattle100k.sim')
# sim9 = cv.load('10AprSeattle100k.sim')
# sim10 = cv.load('Seattle100kV11.sim')
# sim11 = cv.load('24AprSeattle100k.sim')
sim12 = cv.load('Seattle100kV13.sim')


simB.label = 'Baseline'
sim0.label = 'V0'
# sim1.label = 'V1'
# sim2.label = 'V2'
# sim3.label = 'V3'
# sim4.label = 'V4'
# sim5.label = 'V5'
# sim6.label = 'V6'
# sim7.label = 'V7'
# sim8.label = 'V8'
# sim9.label = 'V9'
# sim10.label = 'V10'
# sim11.label = 'V11'
sim12.label = 'V12'

msim = cv.MultiSim([simB, sim0, sim12]) #, sim1, sim2, sim3, sim4, sim5]) #, sim6, sim7, sim8, sim9, sim10, sim11, sim12])
msim.run()
msim.plot().savefig('plot12.png', dpi = 500)

