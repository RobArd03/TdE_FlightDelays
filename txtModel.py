from datetime import time

import networkx as nx
from datetime import datetime
from model.model import Model

mymodel = Model()
mymodel.buildGraph(5)

v0 = mymodel.getAllNodes()[0]

connessa = list(nx.node_connected_component(mymodel._graph, v0))

v1 = connessa[10]

print(v0, v1)

tic = datetime.now()
bestPath, bestObjFun = mymodel.getCamminoOttimo(v0, v1, 4)
toc = datetime.now()



print("--------------------------------")
print(f"Cammino ottimo tra {v0} e {v1} ha peso = {bestObjFun}")
print( "Ci mette: ", toc-tic)
print(*bestPath, sep="\n")

