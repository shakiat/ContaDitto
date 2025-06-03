import tkinter as tk
from tkinter import colorchooser
import json
import os

DATA_FILE = "contadores.json"

class Contador:
    def __init__(self, master, titulo, valor, color, save_callback, remove_callback):
        self.master = master
        self.titulo = tk.StringVar(value=titulo)
        self.valor = tk.IntVar(value=valor)
        self.color = color or "#ffffff"  # color por defecto: blanco
        self.save_callback = save_callback
        self.remove_callback = remove_callback

        self.frame = tk.Frame(master, pady=10, bg=self.color)
        self.frame.pack(padx=10, fill="x")

        # Header con título, botón color y eliminar
        self.header = tk.Frame(self.frame, bg=self.color)
        self.header.pack(fill="x")

        self.label_titulo = tk.Entry(self.header, textvariable=self.titulo, font=("Arial", 10, "bold"), width=20, justify='center')
        self.label_titulo.pack(side=tk.LEFT, padx=5)
        self.label_titulo.bind("<FocusOut>", lambda e: self.save_callback())

        self.btn_color = tk.Button(self.header, text="🎨", command=self.cambiar_color, width=3)
        self.btn_color.pack(side=tk.LEFT)

        self.btn_eliminar = tk.Button(self.header, text="🗑️", command=self.eliminar, fg="red", width=3)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        self.display = tk.Label(self.frame, text=str(self.valor.get()), font=("Courier", 48), bg=self.color)
        self.display.pack()

        self.botones = tk.Frame(self.frame, bg=self.color)
        self.botones.pack()

        self.btn_menos = tk.Button(self.botones, text="-", font=("Arial", 16), command=self.decrementar, width=3)
        self.btn_menos.pack(side=tk.LEFT, padx=5)

        self.btn_mas = tk.Button(self.botones, text="+", font=("Arial", 16), command=self.incrementar, width=3)
        self.btn_mas.pack(side=tk.LEFT, padx=5)



    def actualizar_colores(self):
        widgets = [self.frame, self.header, self.display, self.botones]
        for w in widgets:
            w.config(bg=self.color)
        self.display.config(bg=self.color)

    def cambiar_color(self):
        nuevo_color = colorchooser.askcolor(title="Elige un color")[1]
        if nuevo_color:
            self.color = nuevo_color
            self.actualizar_colores()
            self.save_callback()

    def incrementar(self):
        self.valor.set(self.valor.get() + 1)
        self.display.config(text=str(self.valor.get()))
        self.save_callback()

    def decrementar(self):
        if self.valor.get() > 0:
            self.valor.set(self.valor.get() - 1)
            self.display.config(text=str(self.valor.get()))
            self.save_callback()

    def reiniciar(self):
        self.valor.set(0)
        self.display.config(text="0")
        self.save_callback()

    def eliminar(self):
        self.frame.destroy()
        self.remove_callback(self)

    def get_data(self):
        return {"titulo": self.titulo.get(), "valor": self.valor.get(), "color": self.color}

class ContaDittoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ContaDitto")

        self.contadores = []

        self.btn_reiniciar = tk.Button(root, text="🔁 Reiniciar todos", font=("Arial", 12), command=self.reiniciar_todos)
        self.btn_reiniciar.pack(pady=5)

        self.btn_agregar = tk.Button(root, text="＋ Agregar contador", font=("Arial", 14), command=self.agregar_contador)
        self.btn_agregar.pack(pady=5)

        self.cargar_datos()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def agregar_contador(self, titulo="Nuevo contador", valor=0, color="#ffffff"):
        contador = Contador(self.root, titulo, valor, color, self.guardar_datos, self.eliminar_contador)
        self.contadores.append(contador)
        self.guardar_datos()

    def eliminar_contador(self, contador):
        if contador in self.contadores:
            self.contadores.remove(contador)
            self.guardar_datos()

    def reiniciar_todos(self):
        for contador in self.contadores:
            contador.reiniciar()

    def guardar_datos(self):
        data = [contador.get_data() for contador in self.contadores]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    def cargar_datos(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    self.agregar_contador(
                        item.get("titulo", "Contador"),
                        0,  # ← Siempre valor en cero al cargar
                        item.get("color", "#ffffff")
                    )

    def on_close(self):
        self.guardar_datos()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = ContaDittoApp(root)
    root.mainloop()