import igraph

g = igraph.read("../../raw_data/boost/gcc_9.3.0_O0/atomic/0a4955170a1f265bb651815b1e45f80a.gml")


print(g.get_adjacency())
layout = g.layout("kk")


import matplotlib.pyplot as plt
fig, ax = plt.subplots()
igraph.plot(g, layout=layout, target=ax)
plt.savefig("./graph.png")