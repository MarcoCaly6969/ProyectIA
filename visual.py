import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import osmnx as ox

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

# Ejemplo de uso:
if __name__ == "__main__":
    city_graph = CityGraph("Tu Ciudad, País")

    root = tk.Tk()
    app = CityMapApp(root, city_graph)
    root.mainloop()
