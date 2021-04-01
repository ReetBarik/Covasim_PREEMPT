import covasim as cv
import networkx as nx
import matplotlib.pyplot as plt

pars = dict(
    pop_size = 50,                                 # Number of nodes
    pop_type = 'hybrid',							   # Hybrid population: household, school, work, community layer
    location = 'Seattle',								   # Location and demographic based on Seattle
    # pop_infected = 100,
    start_day = '2020-01-01',						   # Simulation start
    end_day = '2020-04-30'							   # Simulation end
)
sim = cv.Sim(pars)
sim.run()


G = sim.people.to_graph()
nodes = G.nodes(data=True)
edges = G.edges(keys=True)
node_colors = [n['age'] for i,n in nodes]
layer_map = dict(h='#37b', s='#e11', w='#4a4', c='#a49')
edge_colors = [layer_map[G[i][j][k]['layer']] for i,j,k in edges]
edge_weights = [G[i][j][k]['beta']*5 for i,j,k in edges]

fig, ax = plt.subplots()
nx.draw(G, ax = ax, pos=nx.spring_layout(G, seed=4321, k=0.025), node_size = 50, node_color = node_colors, edge_color = edge_colors, width = edge_weights, alpha = 0.5)
plt.savefig('Pop2.png', dpi = 500)