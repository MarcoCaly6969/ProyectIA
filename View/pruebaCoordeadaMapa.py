import tkinter as tk
import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk, Image
def obtener_coordenadas(event):
    x = event.x
    y = event.y
    print("Coordenadas:", x, y)

ven = ctk.CTk()
can = ctk.CTkCanvas(ven, width="1300",height="750")
can.pack()
ima = Image.open("imagenes/mapa.png")
nuevaima = ima.resize((1200, 650))

gf = ImageTk.PhotoImage(nuevaima)

imagen = tk.PhotoImage(file="imagenes/mapa.png")
can.create_image(10,10, anchor=tk.NW, image = gf)
can.bind("<Button-1>", obtener_coordenadas)
ven.mainloop()

if __name__ == "__main__":
    print("holis")