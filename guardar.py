import osmnx as ox
import networkx as nx
import tkinter as tk
import customtkinter as ctk

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
    def plot_grap(self):
        try:
            fig, ax = ox.plot_graph(self.graph, node_size=0, bgcolor='k')
            return fig, ax
        except Exception as e:
            print(f"Error al visualizar la ruta: {e}")
            traceback.print_exc()


class CityMapApp(ctk.CTk):
    def __init__(self, master, city_graph):
        super().__init__()
        self.master = master
        self.master.title("Proyecto de Planificacion")
        self.city_graph = city_graph
        self.geometry("1200x580")
        self.resizable(False,False)
        self.update_idletasks()

        self.main_frame = ctk.CTkFrame(self,width=1200,height=650)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=3)

        self.options_frame = ctk.CTkFrame(self.main_frame, width=1200,height=650)
        self.options_frame.grid(row=0, column=0, sticky=tk.NSEW, ipadx=10, ipady=10, padx=(0, 10), pady=(0,10))
        self.options_frame.columnconfigure(0,weight=1)
        #self.ima = Image.open("imagenes/mapa.png")
        ##self.nuevaima = self.ima.resize((1200,650))

        #self.gf = ImageTk.PhotoImage(self.nuevaima)

        self.img_frame = ctk.CTkCanvas(self.main_frame, width=1200, height=650, bg="#0E6063")
        self.img_frame.grid(row=0, column=1, sticky=tk.NSEW, ipadx=10, ipady=10, padx=(0,10))
        #self.img_frame.create_image(10, 10, image=self.gf, anchor=tk.NW)

        self.label = ctk.CTkLabel(self.options_frame, text="RUTAS")
        self.label.grid(row=0, column=0, sticky=tk.NSEW)

        self.label_start = ctk.CTkLabel(self.options_frame, text="Inicio")
        self.label_start.grid(row=1, column=0, sticky=tk.NSEW)

        self.entry_start = ctk.CTkEntry(self.options_frame, placeholder_text="ingrese el inicio")
        self.entry_start.grid(row=2, column=0, sticky=tk.NSEW, pady=5, padx=5)

        self.label_destination = ctk.CTkLabel(self.options_frame, text="Destino")
        self.label_destination.grid(row=3, column=0, sticky=tk.NSEW)

        self.entry_destination = ctk.CTkEntry(self.options_frame, placeholder_text="ingrese el destino")
        self.entry_destination.grid(row=4, column=0, sticky=tk.NSEW, pady=5, padx=5)

        self.send_agent_button = ctk.CTkButton(self.options_frame, text="Enviar")
        self.send_agent_button.grid(row=5, column=0, sticky=tk.NSEW, pady=5, padx=5)

        # self.start_label = ttk.Label(master, text="Punto de Inicio (lat, lon):")
        # self.start_label.grid(row=0, column=0)
        # self.start_entry = ttk.Entry(master)
        # self.start_entry.grid(row=0, column=1)

        # self.end_label = ttk.Label(master, text="Punto de Destino (lat, lon):")
        # self.end_label.grid(row=1, column=0)
        # self.end_entry = ttk.Entry(master)
        # self.end_entry.grid(row=1, column=1)

        # self.find_route_button = ttk.Button(master, text="Encontrar Ruta", command=self.find_route)
        # self.find_route_button.grid(row=2, column=0, columnspan=2)

        # Interfaz de usuario
        self.canvas = None
        try:
            # Visualizar la ruta
            fig, ax = self.city_graph.plot_grap()
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
    graphml_filepath = 'mapa_limitado.graphml'  # Cambia esto por la ruta a tu archivo GraphML

    city_graph = CityGraph(graphml_filepath)

    root = tk.Tk()
    app = CityMapApp(root, city_graph)
    root.mainloop()
