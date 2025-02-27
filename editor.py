import tkinter as tk
from tkinter import filedialog

class Editor:
    def __init__(self, root):
        #interfaz principal
        self.root = root
        self.root.title("Editor de Texto Axolotli")
        self.text_area = tk.Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        #barra de menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        #menu archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Nuevo", command=self.nuevo)
        self.file_menu.add_command(label="Abrir", command=self.abrir)
        self.file_menu.add_command(label="Guardar", command=self.guardar)
        self.file_menu.add_command(label="Guardar como", command=self.guardar_como)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Cerrar", command=self.root.quit)
        
        #menu editar

    def nuevo(self):
        self.text_area.delete(1.0, tk.END)

    def abrir(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())

    def guardar(self):
        if not hasattr(self, 'current_file'):
            self.save_file_as()
        else:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def guardar_como(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    root.mainloop()