from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import random

# Función para crear la base de datos y las tablas si no existen
# Function to create the database and tables if they do not exist
def crearBaceDatos():
    obBaseDatos = sqlite3.connect("tienda.db")
    cursor = obBaseDatos.cursor()

    # Crea la tabla 'productos' con id, código, nombre y precio
    # Creates the 'productos' table with id, code, name, and price
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   codigo TEXT NOT NULL,
                   producto TEXT NOT NULL,
                   precio REAL NOT NULL)
                   ''')
    
    # Crea la tabla 'almacen' con id, código de producto, stock y descripción
    # Creates the 'almacen' table with id, product code, stock, and description
    cursor.execute('''CREATE TABLE IF NOT EXISTS almacen(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   codigo_producto TEXT NOT NULL,
                   stock INTEGER NOT NULL,
                   descripcion TEXT NOT NULL)
                   ''')
    
    # cursor.execute("SELECT * FROM productos WHERE usuario='admin'") # busca si ya existe ese usuario "admin"
    # # si si existe regresa un TRUE, por lo tanto no agrega otro admin, ya que la condicion no se cumple
    # if not cursor.fetchone():
    #     cursor.execute("INSERT INTO productos(producto, precio) VALUES (?,?)", ("admin","12345")) # se ingresa el dato a la base de datos
    
    obBaseDatos.commit()
    obBaseDatos.close() # despues de cada consulta siemprese debe cerrar la base de datos


# Clase Principal que gestiona la interfaz gráfica y la lógica del CRUD
# Main Class that manages the graphical interface and the CRUD logic
class Principal():
    def __init__(self, master):
        self.vetana = master # vetanatana primaria para todo el programa
        self.vetana.title("Practica  2 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title
        # self.val = validaciones1()  # 🧩 Crea un objeto de la clase validaciones1 / Creates an instance of validation class
        ancho_vetanatana  = 550  # 📏 Ancho de la vetanatana / Window width
        alto_vetanatana = 500  # 📐 Alto de la vetanatana / Window height

        # ⚙️ Obtiene el ancho y alto de la pantalla en milímetros / Gets screen width and height in millimeters
        # Obtener dimensiones de la pantalla / Get screen dimensions
        ancho_pantalla = self.vetana.winfo_screenwidth()
        alto_pantalla = self.vetana.winfo_screenheight()

        # Calcular posición para centrar / Calculate position to center
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        # Aplicar geometría / Apply geometry
        self.vetana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        self.index = -1
        
    
    # Configuración de los widgets de la interfaz (Etiquetas, Entradas, Botones, Tabla)
    # Configuration of interface widgets (Labels, Entries, Buttons, Table)
    def inicio(self):
        self.us = Label(self.vetana, text = "CRUD del Producto")
        self.us.place(x = 5, y = 5)
        Label(self.vetana, text = "Producto").place(x = 5, y = 30)
        self.producto = Entry(self.vetana)
        self.producto.place(x = 5, y = 50)
        Label(self.vetana, text = "Descripcion").place(x = 135, y = 30)
        self.descripcion = Entry(self.vetana)
        self.descripcion.place(x = 135, y = 50)
        Label(self.vetana, text = "Precio").place(x = 265, y = 30)
        self.precio = Entry(self.vetana)
        self.precio.place(x = 265, y = 50)
        Label(self.vetana, text = "Cantidad").place(x = 400, y = 30)
        self.cantidad = Entry(self.vetana)
        self.cantidad.place(x = 400, y = 50)
        
        # Definición de las columnas para el Treeview (tabla)
        # Definition of columns for the Treeview (table)
        columnas = ("ID", "CODIGO", "PRODUCTO", "PRECIO", "DESCRIPCION", "STOCK") # Son las columnas de nuestra base de datos
        self.tabla = ttk.Treeview(self.vetana, columns = columnas, show= "headings")
        self.tabla.place(x = 10, y = 100, width = 480, heigh = 190)

        # 🔠 Configura encabezados y columnas centradas / Sets up headers and centers columns
        for col in columnas:
            self.tabla.heading(col, text = col)
            self.tabla.column(col, anchor="center", width = 30)

        # 🧭 Barras de desplazamiento vertical y horizontal / Vertical and horizontal scrollbars
        scrolly = ttk.Scrollbar(self.vetana, orient = "vertical", command = self.tabla.yview)
        scrollx= ttk.Scrollbar(self.vetana, orient = "horizontal", command = self.tabla.xview)
        scrolly.place(x = 480, y = 90, height = 200)
        scrollx.place(x = 10, y = 280, width = 470 )
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila) # detectar eventos en la tabla
        self.btnAgregar = Button(self.vetana, text = "Agregar", command = self.agregarProducto, width = 10)
        self.btnAgregar.place(x = 30, y = 320)
        self.btnModificar = Button(self.vetana, text = "Modificar", command = self.modificarProducto, width = 10, state = "disabled")
        self.btnModificar.place(x = 120, y = 320)
        self.btnEliminar = Button(self.vetana, text = "Eliminar", command = self.eliminarProducto, width = 10, state = "disabled")
        self.btnEliminar.place(x = 210, y = 320)
        self.mostrarDatos()

    # Función para modificar un producto existente en la base de datos
    # Function to modify an existing product in the database
    def modificarProducto(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        
        valores = self.tabla.item(self.index,"values")
        # print(valores)
        id = valores[0]
        producto = self.producto.get()
        precio = self.precio.get()
        descripcion = self.descripcion.get()
        cantidad = self.cantidad.get()
        
        # Validar que los campos no estén vacíos antes de actualizar
        # Validate that fields are not empty before updating
        if len(producto) != 0 and len(precio) != 0 and len(descripcion) != 0 and len(cantidad) != 0:

            # Genera un nuevo código basado en el nombre y descripción
            # Generates a new code based on the name and description
            codigo = producto[:2].upper() + str(random.randint(0,100)) + descripcion[0].upper()
            obBaseDatos = sqlite3.connect("tienda.db")
            cursor = obBaseDatos.cursor()
            # Actualiza ambas tablas
            # Update both tables
            cursor.execute("UPDATE productos SET codigo=?, producto=?, precio=? WHERE id=?", (codigo,producto,precio, id))
            cursor.execute("UPDATE almacen SET codigo_producto=?, stock=?, descripcion=? WHERE id=?", (codigo,cantidad,descripcion, id))
            obBaseDatos.commit()
            obBaseDatos.close()
            self.actualizarTabla()
            self.borrarCajas()
            self.btnAgregar.config(state= "normal")
            self.btnEliminar.config(state="disabled")
            self.btnModificar.config(state="disabled")
        else:
            messagebox.showerror("Error", "Faltan datos")



    # Función para eliminar un producto de la base de datos
    # Function to delete a product from the database
    def eliminarProducto(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        
        valores = self.tabla.item(self.index,"values")
        print(valores)
        id = valores[0]
        obBaseDatos = sqlite3.connect("tienda.db")
        cursor = obBaseDatos.cursor()
        # Elimina de ambas tablas usando el ID
        # Deletes from both tables using the ID
        cursor.execute("DELETE FROM productos WHERE id=?",(id,)) # (f"DELETE FROM usuarios WHERE id={id}")
        cursor.execute("DELETE FROM almacen WHERE id=?",(id,))
        obBaseDatos.commit()
        obBaseDatos.close()
        self.actualizarTabla()
        self.borrarCajas()
        self.btnAgregar.config(state= "normal")
        self.btnEliminar.config(state="disabled")
        self.btnModificar.config(state="disabled")
        

    # Evento activado al seleccionar una fila en la tabla
    # Event triggered when selecting a row in the table
    def seleccionFila(self, event):
        self.borrarCajas()
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        
        # Llena los campos de entrada con los valores de la fila seleccionada
        # Fills the entry fields with the values of the selected row
        valores = self.tabla.item(self.index,"values")
        self.producto.insert(0,valores[2])
        self.precio.insert(0, valores[3] )
        self.descripcion.insert(0,valores[4])
        self.cantidad.insert(0, valores[5])
        # Habilita botones de modificar/eliminar y deshabilita agregar
        # Enables modify/delete buttons and disables add
        self.btnAgregar.config(state= "disabled")
        self.btnEliminar.config(state="normal")
        self.btnModificar.config(state="normal")

    # Función para recuperar y mostrar datos de la base de datos (JOIN entre tablas)
    # Function to retrieve and display data from the database (JOIN between tables)
    def mostrarDatos(self):
        obBaseDatos = sqlite3.connect("tienda.db")
        cursor = obBaseDatos.cursor()
        cursor.execute('''
            SELECT productos.id,
                    productos.codigo,
                    productos.producto,
                    productos.precio,
                    almacen.descripcion,
                    almacen.stock
            FROM productos
            INNER JOIN almacen
            ON productos.codigo = almacen.codigo_producto  
            '''

        )
        datos = cursor.fetchall()
        # print(datos)
        for i in datos:
            self.tabla.insert("",END, values = i)
        obBaseDatos.commit()
        obBaseDatos.close()
    
    # Función para verificar si un producto ya existe en la base de datos
    # Function to check if a product already exists in the database
    def verificar(self):
        precioFloat = 0.0
        stockInt = 0
        producto = self.producto.get()
        descripcion = self.descripcion.get()
        precio = self.precio.get()
        stock = self.cantidad.get()
        if len(precio) != 0 and len(descripcion) != 0 and len(producto) != 0 and len(stock) != 0:
            obBaseDatos = sqlite3.connect("tienda.db")
            cursor = obBaseDatos.cursor()
            cursor.execute('''
                    SELECT *
                    FROM productos
                    WHERE producto=? 
            ''',(producto,))
            resultado = cursor.fetchone()
            obBaseDatos.commit()
            obBaseDatos.close()
            print(resultado)
            
            if resultado:
                return resultado[0]
            return False
            
    # Función principal para agregar un nuevo producto o actualizar si ya existe
    # Main function to add a new product or update if it already exists
    def agregarProducto(self):
        # Si el producto existe, actualiza sus datos
        # If the product exists, update its data
        if self.verificar():
            # messagebox.showinfo("Ya", "Este producto ya existe")
            id = self.verificar()
            print(id)
            precioFloat = 0.0
            stockInt = 0
            producto = self.producto.get()
            descripcion = self.descripcion.get()
            precio = self.precio.get()
            stock = self.cantidad.get()
            obBaseDatos = sqlite3.connect("tienda.db")
            cursor = obBaseDatos.cursor()
            cursor.execute("UPDATE productos SET precio=? WHERE id=?", (precio, id))
            cursor.execute("UPDATE almacen SET stock=?, descripcion=? WHERE id=?", (stock,descripcion, id))
            obBaseDatos.commit()
            obBaseDatos.close()
            self.actualizarTabla()
            self.borrarCajas()

        # Si no existe, crea un nuevo registro
        # If it does not exist, create a new record
        else: 
            precioFloat = 0.0
            stockInt = 0
            producto = self.producto.get()
            descripcion = self.descripcion.get()
            precio = self.precio.get()
            stock = self.cantidad.get()
            if len(precio) != 0 and len(descripcion) != 0 and len(producto) != 0 and len(stock) != 0:
                precioFloat = float(precio)
                stockInt = int(stock)
                # Generación de código aleatorio
                # Random code generation
                codigo = producto[:2].upper() + str(random.randint(0,100)) + descripcion[0].upper()
                obBaseDatos = sqlite3.connect("tienda.db")
                cursor = obBaseDatos.cursor()
                cursor.execute(f"INSERT INTO productos(codigo,producto,precio) VALUES (?,?,?)",(codigo,producto,precioFloat))
                cursor.execute("INSERT INTO almacen(codigo_producto,descripcion,stock) VALUES (?,?,?)", (codigo,descripcion, stockInt))
                obBaseDatos.commit()
                obBaseDatos.close()
                self.actualizarTabla()
                self.borrarCajas()
            else:
                messagebox.showerror("Error","Faltan Datos")

            
    # Función para limpiar la tabla y volver a cargar los datos
    # Function to clear the table and reload data
    def actualizarTabla(self):

        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        self.mostrarDatos()

    # Función para limpiar los campos de texto
    # Function to clear text fields
    def borrarCajas(self):
        self.precio.delete(0,END)
        self.producto.delete(0,END)
        self.descripcion.delete(0,END)
        self.cantidad.delete(0,END)
        return 0










if __name__=="__main__":
    crearBaceDatos() # los primero que hace es crear la base de datos
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()