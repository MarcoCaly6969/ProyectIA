
class Arist:

    def __init__(self, vertexOirigin, vertexDest):
        self.origen = vertexOirigin
        self.destino = vertexDest

    def getVertexOrigin(self):
        return self.origen

    def getVertexDest(self):
        return self.destino
    
    def __str__(self) -> str:
        return self.origen.getName()+"  ------>  "+self.destino.getName()
