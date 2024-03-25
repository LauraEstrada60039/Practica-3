# Para trabajar con la interfaz
import tkinter as Tk
# Para abrir archivos
from tkinter import filedialog
# Para trabajar con widgets más modernos
from tkinter import ttk
# Para trabajar con imágenes
from PIL import Image, ImageTk, ImageDraw
import os
#Uso de markdown
import markdown2


"""Aqui va la interfaz de usuario.
"""


# Colores
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

def load_corpus(label, file_paths):
    """Carga un corpus y actualiza la etiqueta correspondiente."""
    def load_corpus_inner():
        filename = filedialog.askopenfilename()
        if filename:
            file_paths['archivoCorpus'] = filename
            filename_only = os.path.basename(filename)
            label.config(text=f"{filename_only}")
            print("Ruta del archivo cargado:", filename)
            print("Diccionario de rutas de archivos cargados:", file_paths)
        else:
            label.config(text="No se seleccionó ningún archivo")
    return load_corpus_inner

def load_test_file(label, file_paths):
    """Carga un archivo de prueba y actualiza la etiqueta correspondiente."""
    def load_test_file_inner():
        filename = filedialog.askopenfilename()
        if filename:
            file_paths['archivoPrueba'] = filename
            filename_only = os.path.basename(filename)
            label.config(text=f"{filename_only}")
            print("Ruta del archivo cargado:", filename)
            print("Diccionario de rutas de archivos cargados:", file_paths)
        else:
            label.config(text="No se seleccionó ningún archivo")
    return load_test_file_inner

def load_another_file(label, file_paths, selected_files):
    """Carga otro archivo y actualiza la etiqueta correspondiente."""
    def load_another_file_inner():
        filename = filedialog.askopenfilename()
        if filename:
            if filename not in selected_files:
                # Agregar el archivo a la lista de archivos seleccionados en "Cargar otro archivo"
                selected_files.append(filename)

                # Encontrar el índice más alto actualmente utilizado
                max_index = max([int(key.split('_')[1]) for key in file_paths.keys() if key.startswith('archivoOtros')], default=0)
                # Incrementar el índice para obtener el siguiente número en la secuencia
                index = max_index + 1
                # Construir la nueva clave
                new_key = f'archivoOtros_{index}'

                # Agregar el archivo al diccionario de rutas de archivos cargados
                file_paths[new_key] = filename
                filenames_only = {key: os.path.basename(value) for key, value in file_paths.items() if key.startswith('archivoOtros')}
                text = "\n".join([f"{value}" for value in filenames_only.values()])
                # Mostrar en el label el nombre del archivo
                label.config(text=text)
                print("Ruta del archivo cargado:", filename)
                print("Diccionario de rutas de archivos cargados:", file_paths)
            else:
                print("El archivo ya ha sido cargado anteriormente.")
        else:
            label.config(text="No se seleccionó ningún archivo")
    return load_another_file_inner

def update_selects_options(key, value, selects_options):
    """Actualiza las opciones seleccionadas en los combobox."""
    selects_options[key] = value
    print("selects_options:", selects_options)

def calculate_and_print_data(file_paths, selected_options_representation):
    """Función para calcular y mostrar los datos recopilados."""
    information_calculate = {}

    # Combinar los diccionarios en uno solo
    information_calculate.update(file_paths)

    # Verificar si selected_options_representation es un diccionario válido
    if isinstance(selected_options_representation, dict):
        information_calculate.update(selected_options_representation)
    else:
        print("Error: selected_options_representation no es un diccionario válido")

    print("Datos combinados para el cálculo:")
    for key, value in information_calculate.items():
        print(f"{key}: {value}")

def convert_to_html(markdown_text):
    """Convierte texto en formato Markdown a HTML."""
    return markdown2.markdown(markdown_text)


def update_canvas_text(canvas, text_widget, markdown_text):
    """Actualiza el texto en el widget de texto dentro del canvas."""
    html_text = convert_to_html(markdown_text)
    text_widget.config(state=Tk.NORMAL)  # Habilita la edición del widget de texto
    text_widget.delete("1.0", Tk.END)     # Borra todo el texto existente
    text_widget.insert(Tk.END, html_text) # Inserta el nuevo texto HTML
    text_widget.config(state=Tk.DISABLED) # Deshabilita la edición del widget de texto



def main():
    # Diccionario para almacenar las rutas de los archivos cargados
    file_paths = {}
    # Lista para almacenar los archivos seleccionados en "Cargar otro archivo"
    selected_files = []
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
    MyWindow.geometry(center_window(MyWindow, 800, 500))

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

    # Crear etiquetas y botones en el frame de la barra lateral

    # Carga la imagen y
    # ajusta su tamaño al ancho del sidebar
    sidebar_width = 110  # Ancho máximo del sidebar
    image_path = "Practica3/pato_Angello.jpg"
    image = Image.open(image_path)
    image.thumbnail((sidebar_width, sidebar_width))
    image_size = image.size
    image_photo = ImageTk.PhotoImage(image)

    # label_image = Tk.Label(sidebar_content_frame, image=image_photo, bg="#343A47")
    label_image = Tk.Label(sidebar_content_frame, image=image_photo, font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_image.image = image_photo
    label_image.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Crear etiqueta para mostrar la ruta del archivo cargado
    label_corpus = Tk.Label(sidebar_content_frame, text="Seleccione un archivo", font=("Verdana", 8), fg="#F5E2DC", bg=sidebar_content_frame["background"])
    label_corpus.grid(row=2, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Botón para cargar el corpus
    button_load_corpus = Tk.Button(sidebar_content_frame, font=("Verdana", 8, "bold"), bg="#9CA475", text="Cargar Corpus", command=load_corpus(label_corpus, file_paths))
    button_load_corpus.grid(row=1, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Etiqueta para mostrar la ruta del otro archivo cargado
    label_another_file_path = Tk.Label(sidebar_content_frame, text="Seleccione un archivo", font=("Verdana", 8), fg="#F5E2DC", bg=sidebar_content_frame["background"])
    label_another_file_path.grid(row=5, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Botón para cargar otro archivo
    button_load_another_file = Tk.Button(sidebar_content_frame, bg="#9CA475", font=("Verdana", 8, "bold"), text="Cargar otro archivo", command=load_another_file(label_another_file_path, file_paths, selected_files))
    button_load_another_file.grid(row=4, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Crear etiqueta para mostrar la ruta del archivo de prueba cargado
    label_test_file_path = Tk.Label(sidebar_content_frame, text="Seleccione un archivo", font=("Verdana", 8), fg="#F5E2DC", bg=sidebar_content_frame["background"])
    label_test_file_path.grid(row=7, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Botón para cargar el archivo de prueba
    button_load_test_file = Tk.Button(sidebar_content_frame, bg="#9CA475", font=("Verdana", 8, "bold"), text="Cargar archivo de prueba", command=load_test_file(label_test_file_path, file_paths))
    button_load_test_file.grid(row=6, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    # Selector para la representación vectorial
    label_vector_representation = Tk.Label(sidebar_content_frame, text="Representación vectorial", fg="#F5E2DC", font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_vector_representation.grid(row=8, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    vector_representation_options = ["TF-IDF", "Frecuency", "Binarized", "All"]  # Opciones para el menú desplegable
    selected_vector_representation = Tk.StringVar(sidebar_content_frame)  # Variable para almacenar la opción seleccionada
    selected_vector_representation.set(vector_representation_options[0])  # Establecer la primera opción como la predeterminada
    # Selector para la representación vectorial
    combobox_vector_representation = ttk.Combobox(sidebar_content_frame, font=("Verdana", 8), textvariable=selected_vector_representation, values=vector_representation_options)
    combobox_vector_representation.grid(row=9, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)
    combobox_vector_representation.bind("<<ComboboxSelected>>", lambda event: update_selects_options("representacion_vectorial", selected_vector_representation.get(), selects_options))

    # Crear select para las características
    label_vector_representation = Tk.Label(sidebar_content_frame, text="Características", fg="#F5E2DC", font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_vector_representation.grid(row=11, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    vector_features = ["Unigrams", "Bigrams", "All"]  # Opciones para el menú desplegable
    selected_vector_features = Tk.StringVar(sidebar_content_frame)  # Variable para almacenar la opción seleccionada
    selected_vector_features.set(vector_features[0])  # Establecer la primera opción como la predeterminada
    # Selector para las características
    combobox_vector_features = ttk.Combobox(sidebar_content_frame, font=("Verdana", 8), textvariable=selected_vector_features, values=vector_features)
    combobox_vector_features.grid(row=12, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)
    combobox_vector_features.bind("<<ComboboxSelected>>", lambda event: update_selects_options("caracteristicas", selected_vector_features.get(), selects_options))

    # Select para los elementos comparativos
    label_vector_representation = Tk.Label(sidebar_content_frame, text="Elementos comparativos", fg="#F5E2DC", font=("Verdana", 8, "bold"), bg=sidebar_content_frame["background"])
    label_vector_representation.grid(row=14, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)

    comparative_elements = ["Title", "Content", "Title + Content", "All"]  # Opciones para el menú desplegable
    selected_comparative_elements = Tk.StringVar(sidebar_content_frame)  # Variable para almacenar la opción seleccionada
    selected_comparative_elements.set(comparative_elements[0])  # Establecer la primera opción como la predeterminada
    # Selector para los elementos comparativos
    combobox_comparative_elements = ttk.Combobox(sidebar_content_frame, font=("Verdana", 8), textvariable=selected_comparative_elements, values=comparative_elements)
    combobox_comparative_elements.grid(row=15, column=0, sticky="nsew", padx=10, pady=2, columnspan=2)
    combobox_comparative_elements.bind("<<ComboboxSelected>>", lambda event: update_selects_options("elementos_comparativos", selected_comparative_elements.get(), selects_options))

    # Botón para terminar y cerrar la aplicación
    def exit_application():
        MyWindow.destroy()

    # Botón para calcular y mostrar los datos
    button_calculate = Tk.Button(sidebar_content_frame, font=("Verdana", 8, "bold"), bg="#9CA475", text="Calcular", command=lambda: calculate_and_print_data(file_paths, selects_options))
    button_calculate.grid(row=16, column=0, sticky="nsew", padx=10, pady=5)

    button_exit = Tk.Button(sidebar_content_frame, font=("Verdana", 8, "bold"), bg="#9CA475", text="Terminar", command=exit_application)
    button_exit.grid(row=17, column=0, sticky="nsew", padx=10, pady=5)
    
    # Dentro de la función load_another_file, después de que se ha cargado exitosamente otro archivo
    another_file_markdown_text = """
    # Otro archivo cargado

    Este es el contenido del otro archivo cargado.

    - Otro documento 1
    - Otro documento 2
    - Otro documento 3
    """
    

    ############################################## Fin del Sidebar ##############################################

    # Crear el frame para el contenido principal
    frame_content = Tk.Frame(MyWindow, bg="#F5E2DC")
    # Sticky para ajustarse horizontal y verticalmente norte-sur-este-oeste
    frame_content.grid(row=0, column=1, sticky="nsew")

    # Configurar el peso de las columnas para el diseño responsivo
    MyWindow.columnconfigure(0, weight=3)  # 30%
    MyWindow.columnconfigure(1, weight=7)  # 70%

    ############################################## De aquí en adelante se diseña la vista de los resultados ##############################################

    # Crear un Canvas dentro del frame_content
    canvas = Tk.Canvas(frame_content, bg="#F5E2DC", width=frame_content.winfo_width())
    canvas.pack(side="left", fill="both", expand=True)
    
    # Crear un frame dentro del Canvas para colocar los elementos
    content_frame = Tk.Frame(canvas, bg="#F5E2DC")
    content_frame.pack(fill="both", expand=True)

    # Configurar el Canvas para que el Scrollbar lo controle
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # Agregar un Scrollbar
    scrollbar = ttk.Scrollbar(frame_content, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configurar el Canvas para usar el Scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Permitir hacer scroll con la rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Crear un widget de texto dentro del frame de contenido
    text_widget = Tk.Text(content_frame, wrap="word", font=("Verdana", 10), state=Tk.DISABLED, bg="#F5E2DC", relief="flat")
    text_widget.pack(fill="both", expand=True)

    # Actualizar la función update_canvas_text para que tenga acceso al text_widget
    def update_canvas_text(canvas, text_widget, markdown_text):
        """Actualiza el texto en el widget de texto dentro del canvas."""
        html_text = convert_to_html(markdown_text)
        text_widget.config(state=Tk.NORMAL)  # Habilita la edición del widget de texto
        text_widget.delete("1.0", Tk.END)     # Borra todo el texto existente
        text_widget.insert(Tk.END, html_text) # Inserta el nuevo texto HTML
        text_widget.config(state=Tk.DISABLED) # Deshabilita la edición del widget de texto


    ############################################## Fin de la sección de resultados ##############################################

    # Ejecutar el bucle principal de la aplicación
    MyWindow.mainloop()

if __name__ == "__main__":
    main()
