from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import random

def crearBaceDatos():
    obBaseDatos = sqlite3.connect("tienda.db")
    cursor = obBaseDatos.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS productos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   codigo TEXT NOT NULL,
                   producto TEXT NOT NULL,
                   precio REAL NOT NULL)
                   ''')
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



class Principal():
    def __init__(self, master):
        self.vetana = master # vetanatana primaria para todo el programa
        self.vetana.title("Practica  2 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title
        # self.val = validaciones1()  # 🧩 Crea un objeto de la clase validaciones1 / Creates an instance of validation class
        ancho_vetanatana  = 550  # 📏 Ancho de la vetanatana / Window width
        alto_vetanatana = 500  # 📐 Alto de la vetanatana / Window height

        # ⚙️ Obtiene el ancho y alto de la pantalla en milímetros / Gets screen width and height in millimeters
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.vetana.winfo_screenwidth()
        alto_pantalla = self.vetana.winfo_screenheight()

        # Calcular posición para centrar
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        # Aplicar geometría
        self.vetana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        
    
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
        columnas = ("ID", "CODIGO", "PRODUCTO", "DESCRIPCION", "PRECIO", "STOCK") # Son las columnas de nuestra base de datos
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
        # self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila) # detectar eventos en la tabla
        Button(self.vetana, text = "Agregar", command = self.agregarProducto, width = 10).place(x = 30, y = 320)
        Button(self.vetana, text = "Modificar", command = None, width = 10, state = "disabled").place(x = 120, y = 320)
        Button(self.vetana, text = "Eliminar", command = None, width = 10, state = "disabled").place(x = 210, y = 320)
        self.mostrarDatos()

    def mostrarDatos(self):
        obBaseDatos = sqlite3.connect("tienda.db")
        cursor = obBaseDatos.cursor()
        cursor.execute('''
            SELECT productos.id,
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
        print(datos)
        obBaseDatos.commit()
        obBaseDatos.close()

    def agregarProducto(self):
        precioFloat = 0.0
        stockInt = 0
        producto = self.producto.get()
        descripcion = self.descripcion.get()
        precio = self.precio.get()
        stock = self.cantidad.get()
        if len(precio) != 0 and len(descripcion) != 0 and len(producto) != 0 and len(stock) != 0:
            precioFloat = float(precio)
            stockInt = int(stock)
            codigo = producto[:2].upper() + str(random.randint(0,100)) + descripcion[0].upper()
            obBaseDatos = sqlite3.connect("tienda.db")
            cursor = obBaseDatos.cursor()
            cursor.execute(f"INSERT INTO productos(codigo,producto,precio) VALUES (?,?,?)",(codigo,producto,precioFloat))
            cursor.execute("INSERT INTO almacen(codigo_producto,descripcion,stock) VALUES (?,?,?)", (codigo,descripcion, stockInt))
            obBaseDatos.commit()
            obBaseDatos.close()
        else:
            messagebox.showerror("Error","Faltan Datos")










if __name__=="__main__":
    crearBaceDatos() # los primero que hace es crear la base de datos
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()
