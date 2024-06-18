import osmnx as ox
import networkx as nx

class CityGraph:
    def __init__(self, place_name):
        self.place_name = place_name
        self.graph = self.load_graph()

    def load_graph(self):
        # Descargar datos de la ciudad
        graph = ox.graph_from_place(self.place_name, network_type='drive')
        return graph

    def get_nearest_node(self, point):
        # Encuentra el nodo más cercano a un punto (lat, lon)
        return ox.distance.nearest_nodes(self.graph, point[1], point[0])

    def find_shortest_route(self, orig_point, dest_point):
        # Encuentra la ruta más corta entre dos puntos
        orig_node = self.get_nearest_node(orig_point)
        dest_node = self.get_nearest_node(dest_point)
        shortest_path = nx.shortest_path(self.graph, orig_node, dest_node, weight='length')
        return shortest_path

    def plot_route(self, route):
        # Visualiza la ruta en el grafo
        fig, ax = ox.plot_graph_route(self.graph, route, route_linewidth=6, node_size=0, bgcolor='k')
        return fig, ax

# Ejemplo de uso:
city_graph = CityGraph("Cochabamba, Bolivia")
