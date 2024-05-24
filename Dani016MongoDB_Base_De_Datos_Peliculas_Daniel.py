import pymongo
import tkinter as tk
from tkinter import messagebox
import os

# Función para centrar una ventana
def centrar_ventana(ventana, width, height):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    ventana.geometry(f'{width}x{height}+{x}+{y}')

# Función para mostrar la ventana de inicio
def ventana_inicio():
    ventana_inicio = tk.Toplevel()
    ventana_inicio.title("Cargando")
    centrar_ventana(ventana_inicio, 300, 100)
    tk.Label(ventana_inicio, text="Bienvenido a la base de datos MongoPelisDB\nCargando la base de datos...").pack(pady=20)
    ventana_inicio.after(3000, lambda: ventana_inicio.destroy())  # 5 segundos
    ventana_inicio.transient(ventana)
    ventana_inicio.grab_set()
    ventana_inicio.focus_set()

# Función para mostrar la ventana de salida
def ventana_salida():
    ventana_salida = tk.Toplevel()
    ventana_salida.title("Salida")
    centrar_ventana(ventana_salida, 300, 100)
    tk.Label(ventana_salida, text="Nos vemos muy pronto...\n:)").pack(pady=20)
    ventana_salida.after(2000, lambda: ventana_salida.destroy())  # 2 segundos
    ventana_salida.transient(ventana)
    ventana_salida.grab_set()
    ventana_salida.focus_set()
    ventana_salida.wait_window()

# Configuración de la conexión a MongoDB
try:
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["Dani"]  # Nombre de la base de datos
except pymongo.errors.ConnectionError as e:
    messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
    exit(1)

# Colecciones
plataformas = db["plataformas"]
peliculas = db["peliculas"]

# Insertar datos por defecto en las plataformas
plataformas_por_defecto = ["Netflix", "Amazon Prime", "HBO Max", "Disney+", "Apple TV+", "Otros"]
for plataforma in plataformas_por_defecto:
    plataformas.update_one({"nombre": plataforma}, {"$setOnInsert": {"nombre": plataforma}}, upsert=True)

# Insertar datos por defecto en las películas
peliculas_por_defecto = [
    {"nombre": "El Padrino", "ano_estreno": 1972, "director": "Francis Ford Coppola", "plataforma": "Netflix"},
    {"nombre": "Matrix", "ano_estreno": 1999, "director": "Lana Wachowski", "plataforma": "Amazon Prime"},
    {"nombre": "Pulp Fiction", "ano_estreno": 1994, "director": "Quentin Tarantino", "plataforma": "Netflix"},
    {"nombre": "Forrest Gump", "ano_estreno": 1994, "director": "Robert Zemeckis", "plataforma": "Amazon Prime"},
    {"nombre": "El Caballero Oscuro", "ano_estreno": 2008, "director": "Christopher Nolan", "plataforma": "Netflix"},
    {"nombre": "Inception", "ano_estreno": 2010, "director": "Christopher Nolan", "plataforma": "HBO Max"},
    {"nombre": "Titanic", "ano_estreno": 1997, "director": "James Cameron", "plataforma": "Disney+"},
    {"nombre": "Gladiator", "ano_estreno": 2000, "director": "Ridley Scott", "plataforma": "Apple TV+"},
    {"nombre": "Avengers: Endgame", "ano_estreno": 2019, "director": "Anthony y Joe Russo", "plataforma": "Disney+"},
    {"nombre": "Jurassic Park", "ano_estreno": 1993, "director": "Steven Spielberg", "plataforma": "Netflix"},
    {"nombre": "Cadena perpetua", "ano_estreno": 1994, "director": "Frank Darabont", "plataforma": "HBO Max"},
    {"nombre": "The Godfather: Part II", "ano_estreno": 1974, "director": "Francis Ford Coppola", "plataforma": "Amazon Prime"},
    {"nombre": "Fight Club", "ano_estreno": 1999, "director": "David Fincher", "plataforma": "Otros"},
    {"nombre": "Goodfellas", "ano_estreno": 1990, "director": "Martin Scorsese", "plataforma": "Netflix"},
    {"nombre": "Interstellar", "ano_estreno": 2014, "director": "Christopher Nolan", "plataforma": "Amazon Prime"},
    {"nombre": "The Lion King", "ano_estreno": 1994, "director": "Roger Allers y Rob Minkoff", "plataforma": "Disney+"},
    {"nombre": "El silencio de los corderos", "ano_estreno": 1991, "director": "Jonathan Demme", "plataforma": "Netflix"}
]

for pelicula in peliculas_por_defecto:
    plataforma_id = plataformas.find_one({"nombre": pelicula["plataforma"]})["_id"]
    pelicula["plataforma_id"] = plataforma_id
    peliculas.update_one({"nombre": pelicula["nombre"]}, {"$setOnInsert": pelicula}, upsert=True)

# Función para abrir el formulario de entrada de datos
def abrir_formulario(ventana_principal):
    def guardar_datos():
        nombre = entry_nombre.get()
        ano_estreno = entry_ano_estreno.get()
        director = entry_director.get()
        plataforma_nombre = var_streaming.get()

        plataforma = plataformas.find_one({"nombre": plataforma_nombre})
        if not plataforma:
            messagebox.showerror("Error", "La plataforma seleccionada no existe.")
            return

        pelicula = {
            "nombre": nombre,
            "ano_estreno": int(ano_estreno),
            "director": director,
            "plataforma_id": plataforma["_id"]
        }
        peliculas.insert_one(pelicula)
        messagebox.showinfo("Éxito", "Datos guardados correctamente")
        form_ventana.destroy()

    form_ventana = tk.Toplevel(ventana_principal)
    form_ventana.title("Introducir Datos")
    centrar_ventana(form_ventana, 500, 500)
    form_ventana.transient(ventana_principal)
    form_ventana.grab_set()
    form_ventana.focus_set()

    # Entradas de datos
    tk.Label(form_ventana, text="Nombre:").pack()
    entry_nombre = tk.Entry(form_ventana)
    entry_nombre.pack()

    tk.Label(form_ventana, text="Año de estreno:").pack()
    entry_ano_estreno = tk.Entry(form_ventana)
    entry_ano_estreno.pack()

    tk.Label(form_ventana, text="Director:").pack()
    entry_director = tk.Entry(form_ventana)
    entry_director.pack()

    # Menú desplegable para selección de plataformas de streaming
    tk.Label(form_ventana, text="Streaming:").pack()
    plataformas_streaming = plataformas.distinct("nombre")

    var_streaming = tk.StringVar(form_ventana)
    var_streaming.set(plataformas_streaming[0])  # Valor por defecto
    menu_streaming = tk.OptionMenu(form_ventana, var_streaming, *plataformas_streaming)
    menu_streaming.pack()

    # Botón para guardar datos
    tk.Button(
        form_ventana, text="Guardar Datos", command=guardar_datos
    ).pack(pady=5)

# Función para ver películas
def ver_peliculas():
    def eliminar_pelicula():
        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una película para eliminar.")
            return
        pelicula_seleccionada = lista.get(seleccion)
        nombre_pelicula = pelicula_seleccionada.split(", ")[0].replace("Nombre: ", "")
        peliculas.delete_one({"nombre": nombre_pelicula})
        lista.delete(seleccion)
        messagebox.showinfo("Éxito", "Película eliminada correctamente")

    ventana_ver = tk.Toplevel(ventana)
    ventana_ver.title("Películas registradas")
    centrar_ventana(ventana_ver, 400, 400)
    ventana_ver.transient(ventana)
    ventana_ver.grab_set()

    lista = tk.Listbox(ventana_ver, width=45, height=15)
    lista.pack(pady=10)

    # Consulta para unir películas y plataformas
    resultado = peliculas.aggregate([
        {
            "$lookup": {
                "from": "plataformas",
                "localField": "plataforma_id",
                "foreignField": "_id",
                "as": "plataforma"
            }
        },
        {
            "$unwind": "$plataforma"
        },
        {
            "$project": {
                "nombre": 1,
                "ano_estreno": 1,
                "director": 1,
                "plataforma_nombre": "$plataforma.nombre"
            }
        }
    ])

    for pelicula in resultado:
        lista.insert(tk.END, f"Nombre: {pelicula['nombre']}, Año: {pelicula['ano_estreno']}, Director: {pelicula['director']}, Streaming: {pelicula['plataforma_nombre']}")

    # Botón para eliminar película
    tk.Button(ventana_ver, text="Eliminar Película", command=eliminar_pelicula).pack(pady=5)

# Función para buscar películas
def buscar_peliculas():
    def realizar_busqueda():
        termino_busqueda = entry_busqueda.get()
        criterio = var_criterio.get()
        query = {}

        if criterio == "nombre":
            query = {"nombre": {"$regex": termino_busqueda, "$options": "i"}}
        elif criterio == "director":
            query = {"director": {"$regex": termino_busqueda, "$options": "i"}}
        elif criterio == "ano_estreno":
            try:
                termino_busqueda = int(termino_busqueda)
                query = {"ano_estreno": termino_busqueda}
            except ValueError:
                messagebox.showerror("Error", "El año de estreno debe ser un número.")
                return
        elif criterio == "plataforma":
            query = {"plataforma_id": plataformas.find_one({"nombre": termino_busqueda})["_id"]}

        # Realizar la consulta de búsqueda
        resultado = peliculas.find(query)

        # Mostrar los resultados en la lista
        lista_resultado.delete(0, tk.END)
        for pelicula in resultado:
            plataforma = plataformas.find_one({"_id": pelicula["plataforma_id"]})["nombre"]
            lista_resultado.insert(tk.END, f"Nombre: {pelicula['nombre']}, Año: {pelicula['ano_estreno']}, Director: {pelicula['director']}, Streaming: {plataforma}")

    ventana_busqueda = tk.Toplevel(ventana)
    ventana_busqueda.title("Buscar películas")
    centrar_ventana(ventana_busqueda, 375, 375)
    ventana_busqueda.transient(ventana)
    ventana_busqueda.grab_set()

    var_criterio = tk.StringVar(ventana_busqueda)
    var_criterio.set("nombre")

    tk.Label(ventana_busqueda, text="Buscar por:").pack()
    tk.Radiobutton(ventana_busqueda, text="Nombre", variable=var_criterio, value="nombre").pack()
    tk.Radiobutton(ventana_busqueda, text="Director", variable=var_criterio, value="director").pack()
    tk.Radiobutton(ventana_busqueda, text="Año de estreno", variable=var_criterio, value="ano_estreno").pack()

    # Menú desplegable para selección de plataformas de streaming
    tk.Radiobutton(ventana_busqueda, text="Plataforma (nombre concreto)", variable=var_criterio, value="plataforma").pack()
    #tk.Label(ventana_busqueda, text="Plataforma:").pack()
    plataformas_streaming = plataformas.distinct("nombre")

    var_streaming = tk.StringVar(ventana_busqueda)
    var_streaming.set(plataformas_streaming[0])  # Valor por defecto
    #menu_streaming = tk.OptionMenu(ventana_busqueda, var_streaming, *plataformas_streaming)
    #menu_streaming.pack()

    tk.Label(ventana_busqueda, text="Término de búsqueda").pack()
    entry_busqueda = tk.Entry(ventana_busqueda)
    entry_busqueda.pack()

    tk.Button(ventana_busqueda, text="Buscar", command=realizar_busqueda).pack(pady=10)

    lista_resultado = tk.Listbox(ventana_busqueda, width=45, height=15)
    lista_resultado.pack(pady=10)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Base de Datos")
centrar_ventana(ventana, 400, 400)

# Mostrar ventana de inicio
ventana_inicio()
ventana.after(5000, ventana.lift)  # Levantar la ventana principal después de 5 segundos

# Botones
tk.Button(ventana, text="Introducir Datos", command=lambda: abrir_formulario(ventana)).pack(pady=5)
tk.Button(ventana, text="Ver Películas", command=ver_peliculas).pack(pady=5)
tk.Button(ventana, text="Buscar Películas", command=buscar_peliculas).pack(pady=5)

# Mostrar ventana de salida al cerrar
def on_closing():
    ventana_salida()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", on_closing)
ventana.mainloop()
