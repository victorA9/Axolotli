import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, scrolledtext
import re
import io

class AnalizadorLexico:
    TOKENS = [

        ("TEXTO", r"(['\"])(?:(?!\1).)*\1"),
        ("PALABRA_RESERVADA", r"\b(if|else|while|return|bring)\b"),
        ("FUNCION", r"(([a-zA-Z_][a-zA-Z0-9_]*)\s*\()\b(show|catch|choose|case|while|show)"),  # Detecta funciones
        ("VARIABLE", r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*"),  # Detecta variables en asignación
        ("VARIABLE_USO", r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b"),  # Detecta reutilización de variables
        ("NUMERO", r"\b\d+(\.\d+)?\b"),
        #("OPERADOR", r"[+\-*/=\<\>\!]"),
        #("PARENTESIS", r"[\(\)]"),
        #("LLAVES", r"[\{\}]"),
        #("COMILLAS", r"[\"\']"),
        #("PUNTOS/COMAS", r"[\.\:\,\;]")

    ]

    @staticmethod
    def analizar(texto):
        tokens_encontrados = []
        posicion = 0
        variables_definidas = set()

        while posicion < len(texto):
            match = None
            for tipo, patron in AnalizadorLexico.TOKENS:
                regex = re.compile(patron)
                match = regex.match(texto, posicion)
                if match:
                    valor = match.group(0)

                    # Verificación de variables y funciones
                    if tipo == "VARIABLE":
                        variable = match.group(1)
                        variables_definidas.add(variable)
                    elif tipo == "FUNCION":
                        tokens_encontrados.append(("FUNCION", match.group(1)))

                    tokens_encontrados.append((tipo, valor))
                    posicion += len(valor)
                    break
            if not match:
                if texto[posicion].isspace():
                    posicion += 1  # Ignorar espacios
                else:
                    tokens_encontrados.append(("ERROR", texto[posicion]))
                    posicion += 1

        return tokens_encontrados


class Edicion:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def buscar(self):
        termino = simpledialog.askstring("Buscar", "Ingrese el texto a buscar:")
        if termino:
            start = "1.0"
            self.text_widget.tag_remove("highlight", "1.0", tk.END)
            while True:
                start = self.text_widget.search(termino, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(termino)}c"
                self.text_widget.tag_add("highlight", start, end)
                start = end
            self.text_widget.tag_config("highlight", background="yellow")

    def reemplazar(self):
        buscar = simpledialog.askstring("Reemplazar", "Ingrese el texto a buscar:")
        reemplazo = simpledialog.askstring("Reemplazar", "Ingrese el texto de reemplazo:")
        if buscar and reemplazo:
            contenido = self.text_widget.get("1.0", tk.END)
            nuevo_contenido = contenido.replace(buscar, reemplazo)
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", nuevo_contenido)

    def copiar(self):
        self.text_widget.event_generate("<<Copy>>")

    def cortar(self):
        self.text_widget.event_generate("<<Cut>>")

    def pegar(self):
        self.text_widget.event_generate("<<Paste>>")

class Editor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto Axolotli")
        self.text_area = tk.Text(self.root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        self.edicion = Edicion(self.text_area)

        # Barra de menú
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menú Archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Nuevo", command=self.nuevo)
        self.file_menu.add_command(label="Abrir", command=self.abrir)
        self.file_menu.add_command(label="Guardar", command=self.guardar)
        self.file_menu.add_command(label="Guardar como", command=self.guardar_como)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Cerrar", command=self.root.quit)

        # Menú Editar
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Editar", menu=self.edit_menu)
        self.edit_menu.add_command(label="Buscar", command=self.edicion.buscar)
        self.edit_menu.add_command(label="Reemplazar", command=self.edicion.reemplazar)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Copiar", command=self.edicion.copiar)
        self.edit_menu.add_command(label="Cortar", command=self.edicion.cortar)
        self.edit_menu.add_command(label="Pegar", command=self.edicion.pegar)

        # Menú Herramientas
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Herramientas", menu=self.tools_menu)
        self.tools_menu.add_command(label="Análisis Léxico", command=self.analisis_lexico)

    def nuevo(self):
        self.text_area.delete("1.0", tk.END)

    def abrir(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", file.read())

    def guardar(self):
        if not hasattr(self, 'current_file'):
            self.guardar_como()
        else:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

    def guardar_como(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))

    def analisis_lexico(self):
        contenido = self.text_area.get("1.0", tk.END)
        tokens = AnalizadorLexico.analizar(contenido)

        resultado = "Tipo de Token | Valor\n" + "-" * 30 + "\n"
        errores = []  # Asegurar inicialización
        tabla_simbolos = {}

        for tipo, valor in tokens:
            resultado += f"{tipo:<15} | {valor}\n"
            if tipo == "ERROR":
                errores.append(valor)
            elif tipo == "IDENTIFICADOR":
                tabla_simbolos[valor] = "Variable o función"
            elif tipo == "NUMERO":
                tabla_simbolos[valor] = "Constante"
            elif tipo == "PUNTOS/COMAS":
                tabla_simbolos[valor] = "Signo de \n puntuacion"

        # Mostrar ventana con el resultado
        self.mostrar_resultado(resultado, errores, tabla_simbolos)

    def mostrar_resultado(self, resultado, errores, tabla_simbolos):
        ventana = tk.Toplevel(self.root)
        ventana.title("Resultados del Análisis Léxico")
        text_result = scrolledtext.ScrolledText(ventana, wrap="word", width=60, height=20)
        text_result.insert("1.0", resultado)
        text_result.pack(expand=True, fill="both")

        if errores:
            messagebox.showerror("Errores Léxicos", f"Errores encontrados en: {', '.join(errores)}")

        # Mostrar tabla de símbolos
        if tabla_simbolos:
            resultado_simbolos = "Tabla de Símbolos\n" + "-" * 30 + "\n"
            for simbolo, tipo in tabla_simbolos.items():
                resultado_simbolos += f"{simbolo:<15} | {tipo}\n"

            ventana_simbolos = tk.Toplevel(self.root)
            ventana_simbolos.title("Tabla de Símbolos")
            text_simbolos = scrolledtext.ScrolledText(ventana_simbolos, wrap="word", width=40, height=10)
            text_simbolos.insert("1.0", resultado_simbolos)
            text_simbolos.pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    root.mainloop()
