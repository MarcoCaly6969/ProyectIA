from Model.Arist import Arist
from Model.Grafo import Grafo

class GrafoNoDirigido(Grafo):
    def addArist(self, arist):
        Grafo.addArist(self, arist)
        aristBack = Arist(arist.getVertexDest(), arist.getVertexOrigin())

        Grafo.addArist(self, aristBack)
