import tkinter as tk
from PIL import Image, ImageTk

class BackgroundApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Background Image Test")

        # Cargar la imagen de fondo
        self.background_image = Image.open("2.jpeg")  # Cambia esto por la ruta a tu imagen
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Crear una etiqueta para la imagen de fondo
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Añadir algún contenido encima de la imagen de fondo
        self.label = tk.Label(master, text="Hello, World!", bg="white", fg="black", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button = tk.Button(master, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        print("Button clicked!")

# Ejemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundApp(root)
    root.mainloop()
