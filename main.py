import osmnx as ox
import networkx as nx
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
import traceback
from PIL import Image, ImageTk
import matplotlib.image as mpimg
import random
# Cambiar el backend de matplotlib a TkAgg
matplotlib.use('TkAgg')

class CityGraph:
    def __init__(self, graphml_filepath, hospitals, houses, background_image_path):
        self.graphml_filepath = graphml_filepath
        self.hospitals = hospitals
        self.houses = houses
        self.locations = {**hospitals, **houses}
        self.background_image_path = background_image_path
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

    def plot_graph(self):
        # Visualiza el grafo completo con hospitales y casas y una imagen de fondo
        try:
            fig, ax = ox.plot_graph(self.graph, show=False, close=False, node_size=0, figsize=(11, 7), bgcolor='none', edge_color='gray')
            img = mpimg.imread(self.background_image_path)
            ax.imshow(img, extent=ax.get_xlim() + ax.get_ylim(), aspect='auto')

            hospital_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in self.hospitals]
            hospital_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in self.hospitals]
            house_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in self.houses]
            house_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in self.houses]
            ax.scatter(hospital_xs, hospital_ys, s=100, c='red', marker='^', label='Hospitales o clinicas')
            ax.scatter(house_xs, house_ys, s=100, c='blue', marker='o', label='Casas')
            ax.legend()
            fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)  # Ajustar márgenes
            return fig, ax
        except Exception as e:
            print(f"Error al visualizar el grafo: {e}")
            traceback.print_exc()

    def plot_route(self, route):
        # Visualiza la ruta en el grafo con hospitales y casas y una imagen de fondo
        try:
            fig, ax = ox.plot_graph_route(self.graph, route, route_linewidth=6, node_size=0, bgcolor='none', edge_color='gray', show=False, close=False, figsize=(11, 7))
            img = mpimg.imread(self.background_image_path)
            ax.imshow(img, extent=ax.get_xlim() + ax.get_ylim(), aspect='auto')

            hospital_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in self.hospitals]
            hospital_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in self.hospitals]
            house_xs = [self.graph.nodes[node]['x'] for name, node in self.location_nodes.items() if name in self.houses]
            house_ys = [self.graph.nodes[node]['y'] for name, node in self.location_nodes.items() if name in self.houses]
            ax.scatter(hospital_xs, hospital_ys, s=100, c='red', marker='^', label='Hospitales o clinicas')
            ax.scatter(house_xs, house_ys, s=100, c='blue', marker='o', label='Casas')
            ax.legend()
            fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)  # Ajustar márgenes
            return fig, ax
        except Exception as e:
            print(f"Error al visualizar la ruta: {e}")
            traceback.print_exc()

    def find_shortest_route(self, start_name, end_name):
        try:
            start_node = self.location_nodes[start_name]
            end_node = self.location_nodes[end_name]
            route = nx.shortest_path(self.graph, start_node, end_node, weight='length')
            return route
        except Exception as e:
            print(f"Error al encontrar la ruta más corta: {e}")
            traceback.print_exc()

    def calculate_route_distance(self, route):
        try:
            distance = nx.shortest_path_length(self.graph, route[0], route[-1], weight='length')
            return distance
        except Exception as e:
            print(f"Error al calcular la distancia de la ruta: {e}")
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
        self.start_combobox = ttk.Combobox(self.top_frame, values=list(city_graph.houses.keys()))
        self.start_combobox.grid(row=0, column=1, pady=5)

        self.find_route_button = ttk.Button(self.top_frame, text="Encontrar Ruta", command=self.find_route)
        self.find_route_button.grid(row=0, column=2, pady=5, padx=5)

        self.end_label = ttk.Label(self.top_frame, text="Punto de Destino:")
        self.end_label.grid(row=1, column=0, pady=5)
        self.end_combobox = ttk.Combobox(self.top_frame, values=list(city_graph.hospitals.keys()))
        self.end_combobox.grid(row=1, column=1, pady=5)

        self.return_route_button = ttk.Button(self.top_frame, text="Camino de Vuelta", command=self.find_return_route)
        self.return_route_button.grid(row=1, column=2, pady=5, padx=5)

        # Área de texto para mostrar el registro de mensajes
        self.log_text = tk.Text(self.top_frame, height=4, width=110, state='disabled')
        self.log_text.grid(row=0, column=6, padx=5)

        # Inicializar el canvas con el grafo completo
        self.canvas = None

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

            # Calcular la distancia de la ruta
            distance = self.city_graph.calculate_route_distance(route)
            time = (distance / 160)
            total = time if time % 1 < 0.6 else time + 1 - 0.6
            cost = 10
            if(distance >= 2000):
                cost = 12
                if(distance >= 3000):
                    cost = 15
                    if(distance >= 4000):
                        cost = 20
            self.log_message("Paciente toma un Taxi de ida")
            self.log_message(f"Ruta desde {start_name} hasta {end_name}: {total:.2f} minutos y el costo de {cost} Bs")
            self.log_message("Paciente Llega a la recepción y pide una cita")
            doc = random.randint(20, 40)
            self.log_message(f"Doctor atiende a Paciente unos {doc} minutos")
            price = 80
            self.log_message(f"Paciente paga la consulta {price} Bs en la recepcion")


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

    def find_return_route(self):
        # Obtener los nombres de inicio y destino para el camino de vuelta
        try:
            start_name = self.start_combobox.get()
            end_name = self.end_combobox.get()

            # Encontrar la ruta de vuelta (desde el destino al inicio)
            route = self.city_graph.find_shortest_route(end_name, start_name)

            # Calcular la distancia de la ruta de vuelta
            distance = self.city_graph.calculate_route_distance(route)
            time = (distance / 160)
            total = time if time % 1 < 0.6 else time + 1 - 0.6
            cost = 10
            if(distance >= 2000):
                cost = 12
                if(distance >= 3000):
                    cost = 15
                    if(distance >= 4000):
                        cost = 20
            self.log_message("Paciente retorna a casa en un Taxi")
            self.log_message(f"Ruta desde {end_name} hasta {start_name}: {total:.2f} minutos y el costo de {cost} Bs")

            # Visualizar la ruta de vuelta
            fig, ax = self.city_graph.plot_route(route)
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.bottom_frame)
            self.canvas.get_tk_widget().place(relwidth=1, relheight=1)  # Ajustar el gráfico al tamaño del fondo
            self.canvas.draw()

        except Exception as e:
            print(f"Error al calcular o visualizar la ruta de vuelta: {e}")
            traceback.print_exc()

    def update_route_distance_text(self, text):
        self.route_distance_text.config(state='normal')
        self.route_distance_text.delete(1.0, tk.END)
        self.route_distance_text.insert(tk.END, text)
        self.route_distance_text.config(state='disabled')

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
# Ejemplo de uso:
if __name__ == "__main__":
    graphml_filepath = 'mapa_limitado.graphml'  # Cambia esto por la ruta a tu archivo GraphML
    background_image_path = '2.jpeg'  # Cambia esto por la ruta a tu imagen de fondo

    hospitals = {
        "Clinica los Olivos": (-17.38955,-66.17980), 
        "SSU": (-17.38792,-66.14876),
        "Hospital Viedma": (-17.38566,-66.14865),
        "Clinica Univalle": (-17.37205,-66.16075),
        "Clinica los Angeles": (-17.37872,-66.16479),
        "CORDES": (-17.37650,-66.16295)
    }  # Reemplaza lat1, lon1, etc., con las coordenadas de los hospitales

    houses = {
        "CasaA": (-17.39248,-66.15938),
        "CasaB": (-17.387175,-66.175565),
        "CasaSucre": (-17.39269,-66.14787)
    }  # Reemplaza lat6, lon6, etc., con las coordenadas de las casas

    city_graph = CityGraph(graphml_filepath, hospitals, houses, background_image_path)

    root = tk.Tk()

    app = CityMapApp(root, city_graph)
    root.mainloop()
