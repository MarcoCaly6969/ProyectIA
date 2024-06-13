from Model.Vertexx import Vertexx

class Grafo():
    def __init__(self):
        self.grafoDiccionario = {}
        self.nodes =[]

    def addVertex(self, vertexx):
        if vertexx in self.grafoDiccionario:
            return "ya existe ese grafo"

        assert isinstance(vertexx, Vertexx)
        self.grafoDiccionario[vertexx] = []
        self.nodes.append(vertexx)
    def getNodeslist(self):
        return self.nodes

    def addArist(self, aristt):
        origen = aristt.getVertexOrigin()
        destino = aristt.getVertexDest()

        if origen not in self.grafoDiccionario:
            raise ValueError(f"Vertice {origen.getName()} no esta en el grafo")
        if destino not in self.grafoDiccionario:
            raise ValueError(f"Vertice {destino.getname()} no esta en grafo")

        self.grafoDiccionario[origen].append(destino)

    def vertexInGrafo(self, vertex):
        return vertex in self.grafoDiccionario

    def getVertex(self, nameVertex):
        for i in self.grafoDiccionario:
            if nameVertex == i.getName():
                return i
        print(f"Vertice {nameVertex} no existe en el grafo")

    def getNeighbors(self, vertex):
        return self.grafoDiccionario[vertex]

    def __str__(self) -> str:
        allVertex = ""

        for i in self.grafoDiccionario:  # todos los origenes o llaves
            for j in self.grafoDiccionario[i]:
                allVertex += i.getName() + str(i.getX())+","+str(i.getY())+" ---> "+j.getName()+str(j.getX())+","+str(j.getY())+"\n"
                               # nombre 1         x1  y1             nombre 2    x2   y2
        return allVertex
