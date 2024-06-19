import osmnx as ox
import networkx as nx
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import traceback
from PIL import Image, ImageTk

class CityGraph:
    def __init__(self, graphml_filepath, hospitals, houses):
        self.graphml_filepath = graphml_filepath
        self.locations = {**hospitals, **houses}
        self.graph = self.load_graph()
        self.location_nodes = self.get_location_nodes()

    def load_graph(self):
        # Cargar el grafo desde un archivo GraphML
        try:
            graph = ox.load_graphml(filepath=self.graphml_filepath)
            return graph
        except Exception as e:
            print(f"Error al cargar el grafo: {e}")
            traceback.print_exc()

    def get_location_nodes(self):
        # Encuentra los nodos más cercanos a los hospitales y casas
        location_nodes = {}
        try:
            for name, coords in self.locations.items():
                node = self.get_nearest_node(coords)
                location_nodes[name] = node
            return location_nodes
        except Exception as e:
            print(f"Error al encontrar los nodos de las ubicaciones: {e}")
            traceback.print_exc()

    def get_nearest_node(self, point):
        # Encuentra el nodo más cercano a un punto (lat, lon)
        try:
            return ox.distance.nearest_nodes(self.graph, point[1], point[0])
        except Exception as e:
            print(f"Error al encontrar el nodo más cercano: {e}")
            traceback.print_exc()

    def find_shortest_route(self, orig_name, dest_name):
        # Encuentra la ruta más corta entre dos ubicaciones por nombre
        try:
            orig_node = self.location_nodes[orig_name]
            dest_node = self.location_nodes[dest_name]
            shortest_path = nx.dijkstra_path(self.graph, orig_node, dest_node, weight='length')
            return shortest_path
        except Exception as e:
            print(f"Error al encontrar la ruta más corta: {e}")
            traceback.print_exc()

    def plot_graph(self):
        # Visualiza el grafo completo con hospitales y casas
        try:
            fig, ax = ox.plot_graph(self.graph, show=False, close=False, node_size=0, figsize=(11, 7), bgcolor='none', edge_color='black')
            hospital_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in hospitals]
            hospital_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in hospitals]
            house_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in houses]
            house_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in houses]
            ax.scatter(hospital_xs, hospital_ys, s=100, c='red', marker='^', label='Hospitals')
            ax.scatter(house_xs, house_ys, s=100, c='blue', marker='o', label='Houses')
            ax.legend()
            fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)  # Ajustar márgenes
            return fig, ax
        except Exception as e:
            print(f"Error al visualizar el grafo: {e}")
            traceback.print_exc()

    def plot_route(self, route):
        # Visualiza la ruta en el grafo con hospitales y casas
        try:
            fig, ax = ox.plot_graph_route(self.graph, route, route_linewidth=6, node_size=0, bgcolor='none', edge_color='black', show=False, close=False, figsize=(12, 8))
            hospital_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in hospitals]
            hospital_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in hospitals]
            house_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in houses]
            house_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in houses]
            ax.scatter(hospital_xs, hospital_ys, s=100, c='red', marker='^', label='Hospitals')
            ax.scatter(house_xs, house_ys, s=100, c='blue', marker='o', label='Houses')
            ax.legend()
            fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)  # Ajustar márgenes
            return fig, ax
        except Exception as e:
            print(f"Error al visualizar la ruta: {e}")
            traceback.print_exc()

class CityMapApp:
    def __init__(self, master, city_graph):
        self.master = master
        self.master.title("City Map Route Finder")
        self.city_graph = city_graph

        # Crear marcos para dividir la interfaz
        self.top_frame = tk.Frame(master, height=int(master.winfo_screenheight() * 0.15))
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)  # Asegurar que no haya padding

        # Controles de entrada del usuario
        self.start_label = ttk.Label(self.top_frame, text="Punto de Inicio:")
        self.start_label.grid(row=0, column=0, pady=5)
        self.start_combobox = ttk.Combobox(self.top_frame, values=list(city_graph.location_nodes.keys()))
        self.start_combobox.grid(row=0, column=1, pady=5)

        self.end_label = ttk.Label(self.top_frame, text="Punto de Destino:")
        self.end_label.grid(row=1, column=0, pady=5)
        self.end_combobox = ttk.Combobox(self.top_frame, values=list(city_graph.location_nodes.keys()))
        self.end_combobox.grid(row=1, column=1, pady=5)

        self.find_route_button = ttk.Button(self.top_frame, text="Encontrar Ruta", command=self.find_route)
        self.find_route_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Inicializar el canvas con el grafo completo
        self.canvas = None

        # Cargar y mostrar la imagen de fondo
        self.background_image = Image.open("2.jpeg")  # Cambia esto por la ruta a tu imagen
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.bottom_frame, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.load_initial_graph()

    def load_initial_graph(self):
        try:
            fig, ax = self.city_graph.plot_graph()
            self.canvas = FigureCanvasTkAgg(fig, master=self.bottom_frame)
            self.canvas.get_tk_widget().place(relwidth=1, relheight=1)  # Ajustar el gráfico al tamaño del fondo
            self.canvas.draw()
        except Exception as e:
            print(f"Error al cargar el grafo inicial: {e}")
            traceback.print_exc()

    def find_route(self):
        # Obtener los nombres de inicio y destino
        try:
            start_name = self.start_combobox.get()
            end_name = self.end_combobox.get()

            # Encontrar la ruta más corta
            route = self.city_graph.find_shortest_route(start_name, end_name)

            # Visualizar la ruta
            fig, ax = self.city_graph.plot_route(route)
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.bottom_frame)
            self.canvas.get_tk_widget().place(relwidth=1, relheight=1)  # Ajustar el gráfico al tamaño del fondo
            self.canvas.draw()

        except Exception as e:
            print(f"Error al calcular o visualizar la ruta: {e}")
            traceback.print_exc()

# Ejemplo de uso:
if __name__ == "__main__":
    graphml_filepath = 'mapa_limitado.graphml'  # Cambia esto por la ruta a tu archivo GraphML

    hospitals = {
        "Clinica los Olivos": (-17.38955,-66.17980), 
        "SSU": (-17.38795,-66.14802),
        "Hospital Viedma": (-17.38566,-66.14865),
        "Clinica Univalle": (-17.37205,-66.16075),
        "Clinica los Angeles": (-17.37859,-66.16472),
        "CORDES": (-17.37859,-66.16472)
    }  # Reemplaza lat1, lon1, etc., con las coordenadas de los hospitales

    houses = {
        "CasaA": (-17.39248,-66.15938),
        "CasaB": (-17.387175,-66.175565),
        "CasaSucre": (-17.39269,-66.14787)
    }  # Reemplaza lat6, lon6, etc., con las coordenadas de las casas

    city_graph = CityGraph(graphml_filepath, hospitals, houses)

    root = tk.Tk()

    app = CityMapApp(root, city_graph)
    root.mainloop()
