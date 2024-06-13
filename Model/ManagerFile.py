from io import open

from Model.Arist import Arist
from Model.Vertexx import Vertexx

class ManagerFile(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ManagerFile.__instance is None:
            ManagerFile.__instance = object.__new__(cls)
        return ManagerFile.__instance

    def obtenerGrafo(self):
        fileedge = open("aristaGra.txt","r")
        listAr = fileedge.readlines()
        fileedge.close()
        return listAr

    def obtenerNodesMana(self,graph):
        var = graph.getNodeslist()
        return var

    def obGrafoSinText(self,graph):
        g = graph()

        g.addVertex(Vertexx('e1', 13, 83))
        g.addVertex(Vertexx('e2', 13, 345))
        g.addVertex(Vertexx('e3', 13, 570))
        g.addVertex(Vertexx('e4', 305, 660))
        g.addVertex(Vertexx('e5', 788, 660))
        g.addVertex(Vertexx('e6', 1150, 660))
        g.addVertex(Vertexx('e7', 1208, 490))
        g.addVertex(Vertexx('e8', 1208, 285))
        g.addVertex(Vertexx('e9', 1208, 30))
        g.addVertex(Vertexx('e10', 697, 13))
        g.addVertex(Vertexx('e11', 391, 13))

        g.addVertex(Vertexx('nn1', 215, 84))
        g.addVertex(Vertexx('nn2', 216, 345))
        g.addVertex(Vertexx('nn3', 216, 458))
        g.addVertex(Vertexx('nn4', 428, 568))
        g.addVertex(Vertexx('nn5', 790, 565))
        g.addVertex(Vertexx('nn6', 987, 565))
        g.addVertex(Vertexx('nn7', 1118, 484))
        g.addVertex(Vertexx('nn8', 790, 483))
        g.addVertex(Vertexx('nn9', 572, 452))
        g.addVertex(Vertexx('nn10', 418, 343))
        g.addVertex(Vertexx('nn11', 516, 79))
        g.addVertex(Vertexx('nn12', 595, 126))
        g.addVertex(Vertexx('nn13', 743, 200))
        g.addVertex(Vertexx('nn14', 766, 286))
        g.addVertex(Vertexx('nn15', 1071, 287))
        g.addVertex(Vertexx('nn16', 980, 169))
        g.addVertex(Vertexx('nn17', 844, 93))
        g.addVertex(Vertexx('nn18', 748, 42))

        g.addVertex(Vertexx('parque1', 215, 154))
        g.addVertex(Vertexx('parque2', 320, 393))
        g.addVertex(Vertexx('parque3', 667, 84))
        g.addVertex(Vertexx('parque4', 763, 153))
        g.addVertex(Vertexx('parque5', 786, 420))
        g.addVertex(Vertexx('parque6', 1000, 286))
        g.addVertex(Vertexx('parque7', 1083, 616))
        g.addVertex(Vertexx('parque8', 298, 510))

        g.addVertex(Vertexx('hospital1', 445, 214))
        g.addVertex(Vertexx('hospital2', 872, 567))
        g.addVertex(Vertexx('hospital3', 1034, 425))

        g.addVertex(Vertexx('colegio1', 622, 563))
        g.addVertex(Vertexx('colegio2', 1109, 102))
        g.addVertex(Vertexx('colegio3', 70, 348))

        g.addVertex(Vertexx('mall1', 494, 401))
        g.addVertex(Vertexx('mall2', 557, 287))
        g.addVertex(Vertexx('mall3', 817, 74))
        g.addVertex(Vertexx('mall4', 1057, 208))

        g.addArist(Arist(g.getVertex('e1'), g.getVertex('nn1')))
        g.addArist(Arist(g.getVertex('nn1'), g.getVertex('parque1')))
        g.addArist(Arist(g.getVertex('parque1'), g.getVertex('nn2')))
        g.addArist(Arist(g.getVertex('e2'), g.getVertex('nn2')))
        g.addArist(Arist(g.getVertex('nn2'), g.getVertex('nn3')))
        g.addArist(Arist(g.getVertex('e3'), g.getVertex('nn3')))
        g.addArist(Arist(g.getVertex('nn3'), g.getVertex('parque2')))
        g.addArist(Arist(g.getVertex('parque2'), g.getVertex('nn10')))
        g.addArist(Arist(g.getVertex('nn3'), g.getVertex('parque8')))
        g.addArist(Arist(g.getVertex('parque8'), g.getVertex('nn4')))
        g.addArist(Arist(g.getVertex('e4'), g.getVertex('nn4')))
        g.addArist(Arist(g.getVertex('nn4'), g.getVertex('colegio1')))
        g.addArist(Arist(g.getVertex('colegio1'), g.getVertex('nn5')))
        g.addArist(Arist(g.getVertex('e5'), g.getVertex('nn5')))
        g.addArist(Arist(g.getVertex('e6'), g.getVertex('parque7')))
        g.addArist(Arist(g.getVertex('parque7'), g.getVertex('nn6')))
        g.addArist(Arist(g.getVertex('nn5'), g.getVertex('hospital2')))
        g.addArist(Arist(g.getVertex('hospital2'), g.getVertex('nn6')))
        g.addArist(Arist(g.getVertex('nn4'), g.getVertex('nn9')))
        g.addArist(Arist(g.getVertex('nn2'), g.getVertex('nn10')))
        g.addArist(Arist(g.getVertex('nn10'), g.getVertex('mall1')))
        g.addArist(Arist(g.getVertex('mall1'), g.getVertex('nn9')))
        g.addArist(Arist(g.getVertex('nn9'), g.getVertex('nn8')))
        g.addArist(Arist(g.getVertex('nn5'), g.getVertex('nn8')))
        g.addArist(Arist(g.getVertex('nn10'), g.getVertex('hospital1')))
        g.addArist(Arist(g.getVertex('nn10'), g.getVertex('mall2')))
        g.addArist(Arist(g.getVertex('mall2'), g.getVertex('nn14')))
        g.addArist(Arist(g.getVertex('nn8'), g.getVertex('parque5')))
        g.addArist(Arist(g.getVertex('parque5'), g.getVertex('nn14')))
        g.addArist(Arist(g.getVertex('nn8'), g.getVertex('hospital3')))
        g.addArist(Arist(g.getVertex('hospital3'), g.getVertex('nn15')))
        g.addArist(Arist(g.getVertex('nn15'), g.getVertex('e8')))
        g.addArist(Arist(g.getVertex('nn8'), g.getVertex('nn7')))
        g.addArist(Arist(g.getVertex('nn7'), g.getVertex('e7')))
        g.addArist(Arist(g.getVertex('nn14'), g.getVertex('parque6')))
        g.addArist(Arist(g.getVertex('parque6'), g.getVertex('nn15')))
        g.addArist(Arist(g.getVertex('hospital1'), g.getVertex('nn12')))
        g.addArist(Arist(g.getVertex('nn1'), g.getVertex('nn11')))
        g.addArist(Arist(g.getVertex('e11'), g.getVertex('nn11')))
        g.addArist(Arist(g.getVertex('nn11'), g.getVertex('nn12')))
        g.addArist(Arist(g.getVertex('nn12'), g.getVertex('nn13')))
        g.addArist(Arist(g.getVertex('nn14'), g.getVertex('nn13')))
        g.addArist(Arist(g.getVertex('nn13'), g.getVertex('parque4')))
        g.addArist(Arist(g.getVertex('parque4'), g.getVertex('nn17')))
        g.addArist(Arist(g.getVertex('nn12'), g.getVertex('parque3')))
        g.addArist(Arist(g.getVertex('parque3'), g.getVertex('nn18')))
        g.addArist(Arist(g.getVertex('e10'), g.getVertex('nn18')))
        g.addArist(Arist(g.getVertex('nn18'), g.getVertex('mall3')))
        g.addArist(Arist(g.getVertex('mall3'), g.getVertex('nn17')))
        g.addArist(Arist(g.getVertex('nn17'), g.getVertex('nn16')))
        g.addArist(Arist(g.getVertex('nn16'), g.getVertex('colegio2')))
        g.addArist(Arist(g.getVertex('nn16'), g.getVertex('mall4')))
        g.addArist(Arist(g.getVertex('colegio2'), g.getVertex('e9')))
        g.addArist(Arist(g.getVertex('mall4'), g.getVertex('nn15')))

        return g