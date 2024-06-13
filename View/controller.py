import math
import tkinter

import customtkinter as ctk
from PIL import Image, ImageTk

from Model.GrafoNoDirigido import GrafoNoDirigido
from Model.ManagerFile import ManagerFile
from Algorithms import astar, buscar_nodo_en_grafoBFS, bidirectional_search


class Controller():
    def __init__(self, app):
        self.app = app
        self.manage = ManagerFile()
        self.grafo = GrafoNoDirigido
        self.grafo = self.manage.obGrafoSinText(self.grafo)
        self.nodes = self.manage.obtenerNodesMana(self.grafo)

        self.drawBackground()
        self.draw_Nodes()

        self.app.send_agent_button.configure(command=lambda: self.run_algorithm())
        self.app.clear_button.configure(command=lambda: self.clear())
        self.app.mainloop()

    def run_algorithm(self):
        start = self.app.entry_start.get()
        goal = self.app.entry_destination.get()
        ini = self.grafo.getVertex(start)
        fin = self.grafo.getVertex(goal)

        algorith = self.app.option_algorith.get()

        if algorith == "A*":
            print("estrella")
            path = astar(self.grafo, ini, fin)
            self.drawPath(path)

        elif algorith == "BIDIRECCIONAL":
            print("bidireccional")
            path = bidirectional_search(self.grafo, ini, fin)
            self.drawPath(path)

        else:
            print("bfs")
            path = buscar_nodo_en_grafoBFS(self.grafo, ini, fin)
            self.drawPath(path)

        for i in self.app.objetos:
            self.app.text_box.insert("end", i+"\n")

    def drawBackground(self):
        for n in self.nodes:
            valor = self.grafo.grafoDiccionario[n]
            for nod in valor:
                node_ori_x = n.getX()
                node_ori_y = n.getY()
                node_dest_x = nod.getX()
                node_dest_y = nod.getY()
                self.drawEdge(node_ori_x,node_ori_y, node_dest_x,node_dest_y, "#7DA0CA")

    def drawPath(self, path):
        if path[0] != None:
            Fdistancia = 0
            start = path[0]
            for fs in range(1,len(path)):
                node_origin = (start.getX(),start.getY())
                node_dest = (path[fs].getX(),path[fs].getY())

                distan = self.distance(start.getX(), start.getY(), path[fs].getX(), path[fs].getY())
                Fdistancia += distan

                self.drawEdge(node_origin[0], node_origin[1], node_dest[0], node_dest[1], self.app.color)
                start = path[fs]


            total = f"de: {path[0].getName()} y {path[(len(path))-1].getName()}"
            totaldis = f"distancia: {int(Fdistancia)} m"
            tiempo = Fdistancia / 1.1
            tiem = f"tiempo : {int(tiempo / 60)} min"
            var = total+"\n"+totaldis+"\n"+tiem+"\n"
            self.app.objetos.clear()
            self.app.objetos.append(var)
        else:
            print("esta vacia")

    def drawEdge(self,x1,y1,x2,y2, color):
        self.app.img_frame.create_line(x1, y1, x2, y2, fill=color, width=3)

    def draw_Nodes(self):
        self.nodes
        imagen_cole = Image.open("imagenes/colegio.png")
        imagen_redi_cole = imagen_cole.resize((30,30))
        imagen_tk_cole = ImageTk.PhotoImage(imagen_redi_cole)

        imagen_park = Image.open("imagenes/parque.png")
        imagen_redi_park = imagen_park.resize((40, 40))
        imagen_tk_park = ImageTk.PhotoImage(imagen_redi_park)

        imagen_hosp = Image.open("imagenes/hospital.png")
        imagen_redi_hosp = imagen_hosp.resize((40, 40))
        imagen_tk_hosp = ImageTk.PhotoImage(imagen_redi_hosp)

        imagen_mall = Image.open("imagenes/mall.png")
        imagen_redi_mall = imagen_mall.resize((40, 40))
        imagen_tk_mall = ImageTk.PhotoImage(imagen_redi_mall)

        for nod in self.nodes:
            node = (nod.getX(),nod.getY())
            node_id = nod.getName()
            (x, y) = node
            var = "".join(filter(lambda char: not char.isdigit(), node_id))
            if var == "colegio": #colegios
                label = ctk.CTkLabel(self.app.img_frame, image=imagen_tk_cole,font=ctk.CTkFont(size=20, weight="bold") ,text=node_id, text_color="black")
                self.app.img_frame.create_window(x, y, window=label)

            elif var == "parque": #parques
                label = ctk.CTkLabel(self.app.img_frame, image=imagen_tk_park, font=ctk.CTkFont(size=20, weight="bold"),
                                     text=node_id, text_color="black")
                self.app.img_frame.create_window(x, y, window=label)

            elif var == "hospital": # hospitales
                label = ctk.CTkLabel(self.app.img_frame, image=imagen_tk_hosp, font=ctk.CTkFont(size=20, weight="bold"),
                                     text=node_id, text_color="black")
                self.app.img_frame.create_window(x, y, window=label)

            elif var == "mall": # mall
                label = ctk.CTkLabel(self.app.img_frame, image=imagen_tk_mall, font=ctk.CTkFont(size=20, weight="bold"),
                                     text=node_id, text_color="black")
                self.app.img_frame.create_window(x, y, window=label)
            else:
                self.app.img_frame.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
                self.app.img_frame.create_text(x, y, text=node_id)

    def draw_Nodes2(self):
        self.nodes
        for nod in self.nodes:
            node = nod.getXY()
            node_id = nod.getName()
            (x, y) = node

            self.app.img_frame.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
            self.app.img_frame.create_text(x, y, text=node_id)

    def clear(self):
        self.drawBackground()
        self.repaintNodes()
        self.app.text_box.delete("1.0",tkinter.END)

    def distance(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    def repaintNodes(self):
        for nod in self.nodes:
            node = (nod.getX(), nod.getY())
            node_id = nod.getName()
            (x, y) = node
            var = "".join(filter(lambda char: not char.isdigit(), node_id))
            if var == "nn" or var == "e":
                self.app.img_frame.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
                self.app.img_frame.create_text(x, y, text=node_id)
