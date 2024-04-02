# Para trabajar con la interfaz
import tkinter as Tk
# Para abrir archivos
from tkinter import filedialog
# Mostrar mensajes 
from tkinter import messagebox
# Para trabajar con widgets más modernos
from tkinter import ttk
# Para trabajar con imágenes
from PIL import Image, ImageTk, ImageDraw
# Para abrir los archivos y buscar su ruta relativa
import os
#Uso de html
from tkhtmlview import HTMLLabel
#scrollbar
from tkinter import Scrollbar
# Para dar formato a la tabla que se va a mostrar (uso de expresiones regulares para pasar el html a grid)
import re

# Implementación del análisis de la práctica
# normalizar 
from normalizer import normalize_text
# realizar todo el proceso de análisis
from test_vec_sim import get_table

"""Aqui va la interfaz de usuario.
"""

# Colores empleados
# bg="#343A47" -> Azul marino
# bg="#9CA475" -> Verde olivo
# bg="#F5E2DC" -> Rosa claro
# bg="#EEB4B0" -> Salmón
# bg="#C38491" -> Rosa palo

# Definición de funciones

def open_image(path, size):
    """Abre una imagen y la redimensiona al tamaño especificado."""
    return ImageTk.PhotoImage(Image.open(path).resize(size))


def open_circular_image(path, size):
    """Abre una imagen, la recorta en forma circular y la devuelve."""
    original_image = Image.open(path)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    circular_image = Image.new("RGBA", size)
    circular_image.paste(original_image.resize(size), (0, 0), mask)
    photo = ImageTk.PhotoImage(circular_image)
    return photo


def center_window(window, widthWindow, heightWindow):
    """Centra una ventana en la pantalla."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = max(0, int((screen_width - widthWindow)/2))
    y = max(0, int((screen_height - heightWindow)/2))
    return f"{widthWindow}x{heightWindow}+{x}+{y}"


#Manejar un solo documento
def load_test_file(label, file_content):
    """Carga un archivo de prueba y actualiza la etiqueta correspondiente."""
    def load_test_file_inner():
        
        # Seleccionar el archivo
        filename = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])

        if filename:
            # Actualizar la etiqueta con el nombre del archivo
            filename_only = os.path.basename(filename)
            label.config(text=f"{filename_only}")
            # Leer el contenido del archivo
            with open(filename, 'r', encoding='utf-8') as file:
                file_content_o = file.read()
                file_content_o = normalize_text(file_content_o)

            # Obtener el nombre del archivo sin la extensión
            filename_only = os.path.splitext(os.path.basename(filename))[0]
            # Eliminar todos los elementos existentes en el diccionario file_content
            file_content.clear()
            # Agregar el nuevo elemento al diccionario
            file_content[filename_only] = file_content_o
        else:
            label.config(text="No se seleccionó ningún archivo")
            # Eliminar todos los elementos existentes en el diccionario file_content
            file_content.clear()
    return load_test_file_inner


def update_selects_options(key, value, selects_options):
    """Actualiza las opciones seleccionadas en los combobox."""
    if key == "representacion_vectorial":
        # Si se selecciona "All", convertir la lista en ["tf-idf", "frecuency", "binarized"]
        if value.lower() == "all":
            value = ["tfidf", "frequency", "binary"]
        elif value.lower() == "tf-idf":
            value = ["tfidf"]
        elif value.lower() == "seleccione una opción":
            value = ["seleccione"]
        else:
            # Si no es "All", asegurarse de que la opción seleccionada esté en la lista permitida
            if value.lower() not in ["tf-idf", "frequency", "binary"]:
                messagebox.showerror("Error", "Por favor, seleccione una opción válida para la representación vectorial.")
                return
            value = [value.lower()]  # Convertir la opción individual en una lista
    elif key == "caracteristicas":
        # Si se selecciona "All", convertir la lista en ["Unigrams", "Bigrams"]
        if value.lower() == "all":
            value = [1, 2]  # Guardar como una lista con ambos valores
        elif value.lower() == "seleccione una opción":
            value = ["seleccione"]
        else:
            # Si no es "All", asegurarse de que la opción seleccionada esté en la lista permitida
            if value.lower() not in ["unigrams", "bigrams"]:
                messagebox.showerror("Error", "Por favor, seleccione una opción válida para las características.")
                return
            # Convertir la opción individual en la lista correspondiente
            if value.lower() == "unigrams":
                value = [1]
            elif value.lower() == "bigrams":
                value = [2]
    elif key == "elementos_comparativos":
        # Si se selecciona "All", convertir la lista en ["Title", "Content", "Both"]
        if value.lower() == "all":
            value = ["title", "content", "both"]
        elif value.lower() == "seleccione una opción":
            value = ["seleccione"]
        else:
            # Si no es "All", asegurarse de que la opción seleccionada esté en la lista permitida
            if value.lower() not in ["title", "content", "both"]:
                messagebox.showerror("Error", "Por favor, seleccione una opción válida para los elementos comparativos.")
                return
            value = [value.lower()]  # Convertir la opción individual en una lista
    selects_options[key] = value
    # print("selects_options:", selects_options)



def elements_validator(file_info, information_calculate, n_value_entry):
    # Verificar que no falten datos
    if len(file_info) == 0:
        messagebox.showerror("Error", "Por favor, seleccione un archivo de prueba con extensión txt")
        return 0
    if len(information_calculate) == 0:
        messagebox.showerror("Error", "No ingresó la siguiente información:\n\n*Representación vectorial\n*Características\n*Elemento comparativo")
        return 0
    # Ahora si falta un select con información
    for key, value in information_calculate.items():
        if not value:
            messagebox.showerror("Error", "No ingresó " + key)
            return 0
        else:
            for elemento in value:
                if str(elemento).lower() == "seleccione":
                    messagebox.showerror("Error", "No ingresó " + key)
                    return 0
    # Verificar que es un número
    if (n_value_entry.get()).isdigit() == False:
        messagebox.showerror("Error", "Por favor, ingrese un valor númerico para \"Top n\".\n\nUsted ingresó: " + n_value_entry.get())
        return 0 # Convertir el valor de n_value_entry a entero si está presente


# Dentro de la función calculate_and_print_data
def calculate_and_print_data(html_label, file_info, selected_options_representation, n_value_entry, file_content):
    """Función para calcular y mostrar los datos recopilados."""
    validar = 1;
    # Crear una copia del diccionario de rutas de archivos cargados
    information_calculate = selected_options_representation.copy()
    # information_calculate.update(file_info)
    file_info = file_content.copy()

    # INFORMACION DEL ARCHIVO CARGADO
    # print("\nInformación del archivo cargado:")
    # for key, value in file_info.items():
    #     print(f"{key}: {value}")
    
    # INFORMACIÓN DE LOS SELECTS
    # print("\nDatos combinados para el cálculo:")
    # for key, value in information_calculate.items():
    #     print(f"{key}: {value}")
    
    while True:
        validar = elements_validator(file_info, information_calculate, n_value_entry)
        if validar != 0:
            n_value = int(n_value_entry.get()) if n_value_entry.get() else None  # Convertir el valor de n_value_entry a entero si está presente
            html_table = get_table(corpus='corpus.csv', new_entry=file_info, test_type = information_calculate['elementos_comparativos'], ngrams=information_calculate['caracteristicas'], representation=information_calculate['representacion_vectorial'], top=n_value)    
            # Mostrar la tabla generada en el subframe_html
            generate_tkinter_table_from_html(html_table, html_label, file_info)  # Reemplaza example_html_table con tu HTML generado
            break  # Salir del bucle si la validación es exitosa
        else:
            break
    

def generate_tkinter_table_from_html(html_content, parent, file_info):
    """
    Genera una tabla de Tkinter a partir de HTML con el diseño de grid.

    Args:
        html_content (str): El contenido HTML que describe la tabla.
        parent (tk.Frame): El widget Frame donde se colocará la tabla.
    """

    # Eliminar cualquier tabla existente en el parent
    for widget in parent.winfo_children():
        widget.destroy()
        
    # Eliminar cualquier salto de línea o espacio adicional en el HTML
    html_content = re.sub(r'\n\s*', '', html_content)

    # Definir expresiones regulares para extraer los datos de la tabla
    pattern_table = re.compile(r'<table>(.*?)</table>', re.DOTALL)
    pattern_row = re.compile(r'<tr>(.*?)</tr>')
    pattern_header_cell = re.compile(r'<th.*?>(.*?)</th>', re.DOTALL)
    pattern_cell = re.compile(r'<td.*?>(.*?)</td>', re.DOTALL)

    # Encontrar la tabla en el HTML
    table_match = pattern_table.search(html_content)
    if table_match:
        table_html = table_match.group(1)
        rows = pattern_row.findall(table_html)
        
        # Crear un frame para contener la tabla
        table_frame = Tk.Frame(parent, bg="#F5E2DC", highlightbackground="#F5E2DC")
        table_frame.pack(fill="both", expand=True) # Esto contiene el scrollable
        table_frame.config(width=10)

        # Crear un canvas para contener el frame de la tabla
        table_canvas = Tk.Canvas(table_frame, bg="#F5E2DC", highlightbackground="#F5E2DC")
        # Le agregamos el padding
        table_canvas.pack(side="left", fill="both", expand=True, padx=(15,2), pady=(35,10)) #Para separar resultados el padding
        table_canvas.config(width=10)
        
        # Crear un frame para la tabla real
        table_content_frame = Tk.Frame(table_canvas, bg="#F5E2DC", highlightbackground="#343A47", highlightthickness=1)
        table_content_frame.config(width=10)
        table_content_frame.pack(pady=(0,90))
        
        # Mostrar el texto "RESULTADOS"
        text_results = f"Contenido normalizado: {list(file_info.values())[0]}"
        label_results = Tk.Label(table_canvas, text="RESULTADOS\n", font=("Verdana", 12, "bold"), bg="#F5E2DC")
        label_results.pack(fill="x", expand=False)
        label_results.config(width=1) # Parece que esto le aumentaba el ancho
        # Mostrar el texto normalizado
        label_results_content = Tk.Label(table_canvas, text=text_results, font=("Verdana", 8), bg="#F5E2DC", justify="left", wraplength=500)
        label_results_content.pack(fill="x", expand=False, pady=(0,5))
        label_results_content.config(width=1) # Parece que esto le aumentaba el ancho
        
        # Tamaño del borde de la tabla
        borde_tabla = 2
        # Ancho fijo para todas las celdas
        cell_width = 3

        # Loop a través de las filas
        for i, row_html in enumerate(rows):
            # Verificar si es la primera fila para agregar los encabezados de la tabla
            if i == 0:
                header_cells = pattern_header_cell.findall(row_html)
                total_width = 0  # Inicializa el ancho total de las columnas
                for j, cell_html in enumerate(header_cells):
                    cell_html = cell_html.replace("<br>", "\n")
                    # Crear un widget Label para cada celda y agregarlo al frame de contenido de la tabla
                    label = Tk.Label(table_content_frame, text=cell_html, background="#343A47", fg="#fff", borderwidth=1, highlightbackground="#343A47", relief="solid", padx=10, pady=5, wraplength=130)
                    label.grid(row=i, column=j, sticky="nsew")
                    # Establecer el ancho mínimo de la columna
                    table_content_frame.columnconfigure(j, weight=1, minsize=cell_width)
                    total_width += cell_width  # Sumar el ancho de la columna al ancho total
                # Restar el ancho total del borde de la tabla
                total_width -= borde_tabla * len(header_cells)
                # Ajustar el ancho total de las columnas restando el borde
                for j in range(len(header_cells)):
                    table_content_frame.columnconfigure(j, minsize=cell_width, weight=1, pad=total_width)
            else:
                cells = pattern_cell.findall(row_html)
                total_width = 0  # Inicializa el ancho total de las columnas
                for j, cell_html in enumerate(cells):
                    # Reemplazar <br> por saltos de línea
                    cell_html = cell_html.replace("<br>", "\n")
                    # Crear un widget Label para cada celda y agregarlo al frame de contenido de la tabla
                    label = Tk.Label(table_content_frame, text=cell_html, borderwidth=1, relief="solid", padx=10, pady=5, wraplength=80)
                    label.grid(row=i, column=j, sticky="nsew")
                    # Establecer el ancho mínimo de la columna
                    table_content_frame.columnconfigure(j, weight=1, minsize=cell_width)
                    total_width += cell_width  # Sumar el ancho de la columna al ancho total
                # Restar el ancho total del borde de la tabla
                total_width -= borde_tabla * len(cells)
                # Ajustar el ancho total de las columnas restando el borde
                for j in range(len(cells)):
                    table_content_frame.columnconfigure(j, minsize=cell_width, weight=1, pad=total_width)

        # Calcular el tamaño de la tabla
        table_content_frame.update_idletasks()
        table_width = table_content_frame.winfo_reqwidth()
        table_height = table_content_frame.winfo_reqheight() + label_results.winfo_reqheight() + label_results_content.winfo_reqheight() + 5 #Para que el scroll pueda mostrar todo el contenido de la tabla

        # Ajustar el tamaño del área de visualización del canvas al tamaño de la tabla
        table_canvas.config(scrollregion=(0, 0, table_width, table_height))
                
        # Calcula la altura del label_results
        label_results_height = label_results.winfo_reqheight()
        
        # Calcula la altura del label_results_content
        label_results_content_height = label_results_content.winfo_reqheight()

        # Crear una ventana en el canvas con el tamaño de la tabla y anclarla en la esquina superior izquierda
        table_canvas.create_window((0, label_results_height + label_results_content_height + 5), window=table_content_frame, anchor="nw") # esto está generando problemas al mostrar la ventana

        # Agregar una barra de desplazamiento vertical
        scrollbar_y = Tk.Scrollbar(table_frame, orient="vertical",  command=table_canvas.yview)
        scrollbar_y.pack(side="right", fill="y")

        # Configurar el scrollbar para que funcione con el contenido de la tabla
        table_canvas.configure(yscrollcommand=scrollbar_y.set)
        
        # Permitir que el canvas expanda verticalmente según sea necesario
        table_frame.rowconfigure(1, weight=1)
        
        # Centrar la tabla en la ventana
        table_frame.pack_configure(anchor="center")

        # Retornar el frame de la tabla para poder acceder a él desde fuera de la función
        return table_frame

    else:
        print("No se encontró una tabla en el HTML proporcionado.")


def main():
    # Diccionario para almacenar las rutas de los archivos cargados
    file_paths = {}
    # Diccionario para almacenar el contenido del archivo cargado
    file_content = {}
    # Diccionario para almacenar las opciones seleccionadas en los combobox
    selects_options = {
        "representacion_vectorial": "",
        "caracteristicas": "",
        "elementos_comparativos": ""
    }

    # Crear la ventana principal
    MyWindow = Tk.Tk()

    # Le colocamos el título a la ventana
    MyWindow.title("Document similarity - Pratice III")

    # Definir el tamaño de la ventana (largo x ancho) además de centrarla
    MyWindow.geometry(center_window(MyWindow, 805, 500))
    MyWindow.resizable(False, False) #Restringir el tamaño    

    # Configurar la primera fila para que tome todo el espacio vertical
    MyWindow.rowconfigure(0, weight=1)

    # Crear un frame para la barra lateral izquierda
    frame_sidebar = Tk.Frame(MyWindow, bg="#343A47")
    # Sticky para ajustarse verticalmente norte-sur
    frame_sidebar.grid(row=0, column=0, sticky="nsew")
    # Configurar las filas y columnas del frame_sidebar para que se expandan
    # y contraigan según sea necesario
    frame_sidebar.rowconfigure(0, weight=1)
    frame_sidebar.columnconfigure(0, weight=1)
    sidebar_content_frame = Tk.Frame(frame_sidebar, bg="#343A47")
    sidebar_content_frame.grid(row=0, column=0, sticky="nsew")

    # Limitar el ancho máximo del sidebar al 40% del ancho de la ventana principal
    max_sidebar_width = MyWindow.winfo_width() * 0.4
    frame_sidebar.grid_propagate(False)
    frame_sidebar.config(width=max_sidebar_width)

    # Configurar la columna del sidebar_content_frame para que se expanda y contraiga según sea necesario
    sidebar_content_frame.columnconfigure(0, weight=1)

    ############################################## De aquí en adelante vamos a ir diseñando el sidebar ##############################################
    
    # Carga la imagen y ajustar su tamaño al ancho del sidebar
    sidebar_width = 150  # Ancho máximo del sidebar
    image_path = "Practica3/pato_Angello.jpg"
    image = Image.open(image_path)
    image.thumbnail((sidebar_width, sidebar_width))
    image_size = image.size
    image_photo = ImageTk.PhotoImage(image)

    # label_image = Tk.Label(sidebar_content_frame, image=image_photo, bg="#343A47")
    label_image = Tk.Label(sidebar_content_frame, image=image_photo, font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_image.image = image_photo
    label_image.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Crear etiqueta para mostrar la ruta del archivo de prueba cargado
    label_test_file_path = Tk.Label(sidebar_content_frame, text="Seleccione un archivo", font=("Verdana", 8), fg="#F5E2DC", bg=sidebar_content_frame["background"])
    label_test_file_path.grid(row=4, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Botón para cargar el archivo de prueba
    button_load_test_file = Tk.Button(sidebar_content_frame, bg="#9CA475", font=("Verdana", 8, "bold"), text="Cargar archivo de prueba", command=load_test_file(label_test_file_path, file_content))
    button_load_test_file.grid(row=3, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Selector para la representación vectorial
    label_vector_representation = Tk.Label(sidebar_content_frame, text="Representación vectorial", fg="#F5E2DC", font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_vector_representation.grid(row=8, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    vector_representation_options = ["Seleccione una opción","TF-IDF", "Frequency", "Binary", "All"]  # Opciones para el menú desplegable
    selected_vector_representation = Tk.StringVar(sidebar_content_frame)  # Variable para almacenar la opción seleccionada
    selected_vector_representation.set(vector_representation_options[0])  # Establecer la primera opción como la predeterminada
    # Selector para la representación vectorial
    combobox_vector_representation = ttk.Combobox(sidebar_content_frame, font=("Verdana", 8), textvariable=selected_vector_representation, values=vector_representation_options)
    combobox_vector_representation.grid(row=9, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)
    combobox_vector_representation.bind("<<ComboboxSelected>>", lambda event: update_selects_options("representacion_vectorial", selected_vector_representation.get(), selects_options))

    # Crear select para las características
    label_vector_representation = Tk.Label(sidebar_content_frame, text="Características", fg="#F5E2DC", font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_vector_representation.grid(row=11, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    vector_features = ["Seleccione una opción", "Unigrams", "Bigrams", "All"]  # Opciones para el menú desplegable
    selected_vector_features = Tk.StringVar(sidebar_content_frame)  # Variable para almacenar la opción seleccionada
    selected_vector_features.set(vector_features[0])  # Establecer la primera opción como la predeterminada
    # Selector para las características
    combobox_vector_features = ttk.Combobox(sidebar_content_frame, font=("Verdana", 8), textvariable=selected_vector_features, values=vector_features)
    combobox_vector_features.grid(row=12, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)
    combobox_vector_features.bind("<<ComboboxSelected>>", lambda event: update_selects_options("caracteristicas", selected_vector_features.get(), selects_options))

    # Select para los elementos comparativos
    label_vector_representation = Tk.Label(sidebar_content_frame, text="Elementos comparativos", fg="#F5E2DC", font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_vector_representation.grid(row=14, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    comparative_elements = ["Seleccione una opción", "Title", "Content", "Both", "All"]  # Opciones para el menú desplegable
    selected_comparative_elements = Tk.StringVar(sidebar_content_frame)  # Variable para almacenar la opción seleccionada
    selected_comparative_elements.set(comparative_elements[0])  # Establecer la primera opción como la predeterminada
    # Selector para los elementos comparativos
    combobox_comparative_elements = ttk.Combobox(sidebar_content_frame, font=("Verdana", 8), textvariable=selected_comparative_elements, values=comparative_elements)
    combobox_comparative_elements.grid(row=15, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)
    combobox_comparative_elements.bind("<<ComboboxSelected>>", lambda event: update_selects_options("elementos_comparativos", selected_comparative_elements.get(), selects_options))
    
    # Etiqueta para solicitar el valor de n
    n_value_label = Tk.Label(sidebar_content_frame, text="Top n:", font=("Verdana", 8, "bold"), fg="#F5E2DC", bg=sidebar_content_frame["background"])
    n_value_label.grid(row=16, column=0, sticky="nsew", padx=10, pady=1)

    # Campo de entrada para el valor de n
    n_value_entry = Tk.Entry(sidebar_content_frame, validate="key", fg="#000", font=("Verdana", 8))
    n_value_entry.grid(row=17, column=0, sticky="nsew", padx=10, pady=4)
    
    # Botón para terminar y cerrar la aplicación
    def exit_application():
        MyWindow.destroy()
    
    # Botón para calcular y mostrar los datos
    button_calculate = Tk.Button(sidebar_content_frame, font=("Verdana", 8, "bold"), bg="#9CA475", text="Calcular", command=lambda: calculate_and_print_data(html_label, file_paths, selects_options, n_value_entry, file_content))
    button_calculate.grid(row=18, column=0, sticky="nsew", padx=10, pady=5)

    button_exit = Tk.Button(sidebar_content_frame, font=("Verdana", 8, "bold"), bg="#9CA475", text="Terminar", command=exit_application)
    button_exit.grid(row=19, column=0, sticky="nsew", padx=10, pady=4)

    ############################################## Fin del Sidebar ##############################################

    # Crear el frame para el contenido principal
    frame_content = Tk.Frame(MyWindow, bg="#F5E2DC")
    # Sticky para ajustarse horizontal y verticalmente norte-sur-este-oeste
    frame_content.grid(row=0, column=1, sticky="nsew")

    # Configurar el peso de las columnas para el diseño responsivo
    MyWindow.columnconfigure(0, weight=3)  # 30%
    MyWindow.columnconfigure(1, weight=7)  # 70%

    ############################################## De aquí en adelante se diseña la vista de los resultados ##############################################
    
    # Crear un subframe dentro del frame_content para el html_label
    subframe_html = Tk.Frame(frame_content)
    # subframe_html.pack(expand=True, fill="both", padx=20, pady=15) # Le quitamos su padding
    subframe_html.pack(expand=True, fill="both")

    # HTMLLabel para mostrar el HTML
    html_label = HTMLLabel(subframe_html, background="#F5E2DC")
    html_label.pack(expand=True, fill="both")
    html_label.config(width=10)  # Establecer un ancho máximo para el HTMLLabel, esto lo acomodó como el padre
    label_initial = Tk.Label(html_label, text="Llene los campos para comenzar", font=("Verdana", 12, "bold"), bg="#F5E2DC")
    label_initial.place(relx=0.5, rely=0.45, anchor="center")  # Centra el label en el centro del html_label

    ############################################## Fin de la sección de resultados ##############################################

    # Ejecutar el bucle principal de la aplicación
    MyWindow.mainloop()

if __name__ == "__main__":
    main()
