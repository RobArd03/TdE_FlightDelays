import copy

from database.DAO import DAO
import networkx as nx



class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestPath = []
        self._bestObjFun = 0


    def buildGraph(self, nMin: int):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        #self.addAllEdgesV1()
        #print(f"Metodo 1:\nN nodi: {self._graph.number_of_nodes()} - N archi: {self._graph.number_of_edges()}")
        self._graph.clear_edges()
        self.addAllEdgesV2()
        print(f"Metodo 2:\nN nodi: {self._graph.number_of_nodes()} - N archi: {self._graph.number_of_edges()}")


    def addAllEdgesV1(self):
        allEdges = DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aereoportoP in self._graph and e.aereoportoD in self._graph:
                if self._graph.has_edge(e.aereoportoP, e.aereoportoD):
                    self._graph[e.aereoportoP][e.aereoportoD]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aereoportoP, e.aereoportoD, weight = e.peso)

    def addAllEdgesV2(self):
        allEdges = DAO.getAllEdgesV2(self._idMapAirports)
        for e in allEdges:
            if e.aereoportoP in self._graph and e.aereoportoD in self._graph:
                self._graph.add_edge(e.aereoportoP, e.aereoportoD, weight = e.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes())
        nodes.sort(key = lambda x : x.IATA_CODE)
        return nodes

    def getSortedNeighbors(self, node):
        neighbors = self._graph.neighbors(node) # self._graph[node]
        neighbTuples = []
        for n in neighbors:
            neighbTuples.append( (n, self._graph[node][n]["weight"]) )
        neighbTuples.sort(key = lambda x : x[1], reverse = True)
        return neighbTuples

    def getPath(self, v0, v1):
        path = nx.dijkstra_path(self._graph, v0, v1, weight = None)
        return path

    def getCamminoOttimo(self, v0, v1, nMax):

        self._bestPath =[]
        self._bestObjFun = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, nMax)

        return self._bestPath, self._bestObjFun

    def _ricorsione(self, parziale, v1, nMax: int):

        # Verificare se il parziale è una possibile soluzione
            # verificare se parziale è meglio del best
            # esco
        if parziale[-1] == v1:
            if self.getObjFun(parziale) > self._bestObjFun:
                self._bestObjFun = self.getObjFun(parziale)
                self._bestPath = copy.deepcopy(parziale)
        if len(parziale) == nMax+1:
            return

        # Posso ancora aggiungere nodi
            # prendo i vicini ed aggiungo un nodo alla volta
        else:
            for n in self._graph.neighbors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale, v1, nMax)
                    parziale.pop()


    def getObjFun(self, listOfNodes):
        c = 0
        for i in range(0, len(listOfNodes)-1):
            c += self._graph[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return c
