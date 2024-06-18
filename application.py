import osmnx as ox
import networkx as nx
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import traceback

class CityGraph:
    def __init__(self, graphml_filepath):
        self.graphml_filepath = graphml_filepath
        self.graph = self.load_graph()

    def load_graph(self):
        # Cargar el grafo desde un archivo GraphML
        try:
            graph = ox.load_graphml(filepath=self.graphml_filepath)
            return graph
        except Exception as e:
            print(f"Error al cargar el grafo: {e}")
            traceback.print_exc()

    def get_nearest_node(self, point):
        # Encuentra el nodo más cercano a un punto (lat, lon)
        try:
            return ox.distance.nearest_nodes(self.graph, point[1], point[0])
        except Exception as e:
            print(f"Error al encontrar el nodo más cercano: {e}")
            traceback.print_exc()

    def find_shortest_route(self, orig_point, dest_point):
        # Encuentra la ruta más corta entre dos puntos
        try:
            orig_node = self.get_nearest_node(orig_point)
            dest_node = self.get_nearest_node(dest_point)
            shortest_path = nx.dijkstra_path(self.graph, orig_node, dest_node, weight='length')
            return shortest_path
        except Exception as e:
            print(f"Error al encontrar la ruta más corta: {e}")
            traceback.print_exc()

    def plot_route(self, route):
        # Visualiza la ruta en el grafo
        try:
            fig, ax = ox.plot_graph_route(self.graph, route, route_linewidth=6, node_size=0, bgcolor='k')
            return fig, ax
        except Exception as e:
            print(f"Error al visualizar la ruta: {e}")
            traceback.print_exc()

class CityMapApp:
    def __init__(self, master, city_graph):
        self.master = master
        self.master.title("City Map Route Finder")
        self.city_graph = city_graph

        # Interfaz de usuario
        self.start_label = ttk.Label(master, text="Punto de Inicio (lat, lon):")
        self.start_label.grid(row=0, column=0)
        self.start_entry = ttk.Entry(master)
        self.start_entry.grid(row=0, column=1)

        self.end_label = ttk.Label(master, text="Punto de Destino (lat, lon):")
        self.end_label.grid(row=1, column=0)
        self.end_entry = ttk.Entry(master)
        self.end_entry.grid(row=1, column=1)

        self.find_route_button = ttk.Button(master, text="Encontrar Ruta", command=self.find_route)
        self.find_route_button.grid(row=2, column=0, columnspan=2)

        self.canvas = None

    def find_route(self):
        # Obtener puntos de inicio y destino
        try:
            start_point = tuple(map(float, self.start_entry.get().split(',')))
            end_point = tuple(map(float, self.end_entry.get().split(',')))

            # Encontrar la ruta más corta
            route = self.city_graph.find_shortest_route(start_point, end_point)

            # Visualizar la ruta
            fig, ax = self.city_graph.plot_route(route)
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.master)
            self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)
            self.canvas.draw()

        except Exception as e:
            print(f"Error al calcular o visualizar la ruta: {e}")
            traceback.print_exc()

# Ejemplo de uso:
if __name__ == "__main__":
    graphml_filepath = 'grafo_cocha.graphml'  # Cambia esto por la ruta a tu archivo GraphML

    city_graph = CityGraph(graphml_filepath)

    root = tk.Tk()
    app = CityMapApp(root, city_graph)
    root.mainloop()
