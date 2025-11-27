from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3

def crearBaceDatos():
    obBaseDatos = sqlite3.connect("usuarios.db")
    cursor = obBaseDatos.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT NOT NULL,
                   password TEXT NOT NULL)
                   ''')
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'") # busca si ya existe ese usuario "admin"
    # si si existe regresa un TRUE, por lo tanto no agrega otro admin, ya que la condicion no se cumple
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)", ("admin","12345")) # se ingresa el dato a la base de datos
    
    obBaseDatos.commit()
    obBaseDatos.close() # despues de cada consulta siemprese debe cerrar la base de datos

class Principal():
    def __init__(self, master):
        self.vetana = master # vetanatana primaria para todo el programa
        self.vetana.title("Practica  2 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title
        # self.val = validaciones1()  # 🧩 Crea un objeto de la clase validaciones1 / Creates an instance of validation class
        ancho_vetanatana  = 250  # 📏 Ancho de la vetanatana / Window width
        alto_vetanatana = 200  # 📐 Alto de la vetanatana / Window height

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
        # caja 1
        Label(self.vetana, text = "Usuario ").place(x = 20, y = 20)
        self.n1 = Entry(self.vetana)
        self.n1.place(x = 50, y = 50)
        # caja 2
        Label(self.vetana, text= "Password").place(x = 20, y = 75)
        self.n2 = Entry(self.vetana, show="x")
        self.n2.place(x = 50, y = 100)
        # botones
        Button(self.vetana, text = "Validar", width=10, command= self.enviar).place(x = 30, y = 140)
        Button(self.vetana, text = "Cerrar", width=10, command= self.cerrar).place(x = 150, y = 140)

    def enviar(self):
        u = self.n1.get()
        p = self.n2.get()
        # revisar en la base de datos si existe el usuario
        con = sqlite3.connect("usuarios.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? and password=?", (u,p)) # busca si ya existe ese usuario "admin"
        resultado = cursor.fetchone() # preguntamos si encontrol el registro admin
        con.close()
        if resultado: # si si lo ecnontro pasamos a la otra ventana
        # if u == "admin" and p == "12345":
            self.n1.delete(0, END)
            self.n2.delete(0, END)
            # self.vetana.whithdraw()
            self.vetana.withdraw() # oculta la ventana 🙈
            otra = Toplevel(self.vetana) # manda a llamar a la otra ventana 
            Ventana2(otra, self.vetana, u) # se va con la otra
            return 1
        
        self.n1.delete(0, END)
        self.n2.delete(0, END)
        messagebox.showerror("Error", "Datos incorrectos 🥺")

    def cerrar(self):
        self.vetana.destroy()

    
class Ventana2 ():
    def __init__(self, master,vetana, u): # recive lo que le madaron
        # lo que recibe guardado
        self.venDos = master
        self.usuario = u
        self.vetana = vetana

        self.venDos.title("Practica  1 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title
        # self.val = validaciones1()  # 🧩 Crea un objeto de la clase validaciones1 / Creates an instance of validation class
        ancho_vetanatana  = 550  # 📏 Ancho de la vetanatana / Window width
        alto_vetanatana = 320  # 📐 Alto de la vetanatana / Window height

        # ⚙️ Obtiene el ancho y alto de la pantalla en milímetros / Gets screen width and height in millimeters
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.venDos.winfo_screenwidth()
        alto_pantalla = self.venDos.winfo_screenheight()

        # Calcular posición para centrar
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        # Aplicar geometría
        self.venDos.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        # Label(self.venDos, text = "Hola mundo").place(x = 50, y = 20)
        Label(self.venDos, text = "Escribe el usuario").place(x = 10, y = 10)
        self.usuarioVenDos = Entry(self.venDos)
        self.usuarioVenDos.place(x = 10, y = 30)
        Label(self.venDos, text = "Escribe el Password").place(x = 150, y = 10)
        self.contraseñaN = Entry(self.venDos)
        self.contraseñaN.place(x = 150, y = 30)

        self.us = Label(self.venDos,  text = "")
        self.us.place(x = 300, y = 10)
        self.us.config(text = f"Bienvenido \n {self.usuario}")
        # Button(self.venDos, text = "Regresar",width=10, command= self.regresar).place(x = 50, y = 100)
        self.mostrar()
        self.mostrar_tabla()
        self.menus = tk.Menu(self.venDos) # objeto de la libreria de tk inter
        self.venDos.config(menu = self.menus)
        self.archivo = tk.Menu(self.menus, tearoff = 0)
        self.archivo.add_command(label = "Salir", command = self.salir)
        self.archivo.add_command(label = "Modificar", command = self.modificarUsuario)
        self.indexModificar = self.archivo.index("end")
        self.archivo.add_command(label = "Eliminar", command = self.eliminarUsuario)
        self.indexEliminar = self.archivo.index("end")
        self.archivo.add_command(label = "Agregar", command = self.crearUsuario)
        self.indexAgregar = self.archivo.index("end")
        self.menus.add_cascade(label = "Archivo", menu = self.archivo)
        self.index = -1
        self.archivo.entryconfig(self.indexAgregar, state = "disable")
        self.archivo.entryconfig(self.indexModificar, state = "disable")
        self.archivo.entryconfig(self.indexEliminar, state = "disable")
        # print(self.indexAgregar)
        # print(self.indexEliminar)
        self.roles()


    def roles(self):
        if self.usuario == "admin":
            self.archivo.entryconfig(self.indexAgregar, state = "normal")
            self.archivo.entryconfig(self.indexModificar, state = "normal")
            self.archivo.entryconfig(self.indexEliminar, state = "normal")

        elif self.usuario in ("Supervisor", "supervisor"):
            self.archivo.entryconfig(self.indexAgregar, state = "normal")
            self.archivo.entryconfig(self.indexModificar, state = "disable")
            self.archivo.entryconfig(self.indexEliminar, state = "disable")
        
        elif self.usuario in ("Jefe de area", "jefe de area"):
            self.archivo.entryconfig(self.indexAgregar, state = "disable")
            self.archivo.entryconfig(self.indexModificar, state = "normal")
            self.archivo.entryconfig(self.indexEliminar, state = "disable")

    def seleccionFila(self, event):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        
        valores = self.tabla.item(self.index,"values")
        self.usuarioVenDos.delete(0, END)
        self.contraseñaN.delete(0, END)
        self.usuarioVenDos.insert(0, valores[1])
        self.contraseñaN.insert(0, valores[2])
        # print(valores)
        # return valores

    
    def eliminarUsuario(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            valores = self.tabla.item(self.index,"values")
            # print(valores)
            usuario = valores[1]
            id = valores[0]
            # print(valores[0])
            # print("antes de interrogante")
            if usuario == self.usuario:
                messagebox.showerror("Error", "No te puedes eliminar a ti mismo")
                return 1
                
            
            obBaseDatos = sqlite3.connect("usuarios.db")
            cursor = obBaseDatos.cursor()
            cursor.execute(f"DELETE FROM usuarios WHERE id={id}")# , (id,)) # se debea agregar la coma para poder borrar dos elementos en el index
            obBaseDatos.commit()
            obBaseDatos.close()

            self.actualizarTabla()
            self.borrarDatos("Usuario Eliminado Corretamente")
            self.index = -1

        except:
            messagebox.showerror("Error", "Elije una fila")
           
    def modificarUsuario(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
        except:
            messagebox.showerror("Error", "Elije un Usuario")
            return 1
        
        valores = self.tabla.item(self.index,"values")
        id = valores[0]
        
        if len(self.usuarioVenDos.get()) != 0 and len(self.contraseñaN.get()) != 0:
            usuario = self.usuarioVenDos.get()
            password = self.contraseñaN.get()
            obBaseDatos = sqlite3.connect("usuarios.db")
            cursor = obBaseDatos.cursor()
            cursor.execute("UPDATE usuarios SET usuario=?, password=? WHERE id=?", (usuario,password, id))
            obBaseDatos.commit()
            obBaseDatos.close()
            self.borrarDatos("Datos actualizados")
            self.actualizarTabla()
            self.index = -1


        else:
            messagebox.showerror("Error","Faltan Datos")

    def crearUsuario(self):
        if len(self.usuarioVenDos.get()) != 0 and len(self.contraseñaN.get()) != 0:
            obBaseDatos = sqlite3.connect("usuarios.db")
            cursor = obBaseDatos.cursor()
            cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)", (self.usuarioVenDos.get(),self.contraseñaN.get()))
            obBaseDatos.commit()
            obBaseDatos.close()
            self.borrarDatos("Usuario Agregado correctamente")

            self.actualizarTabla()

            return 0
        #else:
        messagebox.showerror("Error", "Faltan datos")


    def salir(self):
        self.venDos.destroy()
        self.vetana.destroy()
        

    def actualizarTabla(self):

        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        self.mostrar_tabla()

    def mostrar_tabla(self):
        con = sqlite3.connect("usuarios.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios") # busca si ya existe ese usuario "admin"
        resultado = cursor.fetchall() # solicita acceso a todos los registros de la base de datos
        # print(resultado)
        for i in resultado:
            self.tabla.insert("", END, values = i)
            print(i)

        con.close()
    
    def borrarDatos(self, mensaje):
        self.usuarioVenDos.delete(0, END)
        self.contraseñaN.delete(0, END)
        messagebox.showinfo("Datos", mensaje)
        
    def mostrar(self):
                # dataGrid:
        # 📋 Crea la tabla (Treeview) con encabezados / Creates data table (Treeview) with headers
        columnas = ("ID", "USUARIO", "PASSWORD") # Son las columnas de nuestra base de datos
        self.tabla = ttk.Treeview(self.venDos, columns = columnas, show= "headings")
        self.tabla.place(x = 10, y = 100, width = 350, heigh = 190)

        # 🔠 Configura encabezados y columnas centradas / Sets up headers and centers columns
        for col in columnas:
            self.tabla.heading(col, text = col)
            self.tabla.column(col, anchor="center", width = 30)

        # 🧭 Barras de desplazamiento vertical y horizontal / Vertical and horizontal scrollbars
        scrolly = ttk.Scrollbar(self.venDos, orient = "vertical", command = self.tabla.yview)
        scrollx= ttk.Scrollbar(self.venDos, orient = "horizontal", command = self.tabla.xview)
        scrolly.place(x = 360, y = 100, height = 190)
        scrollx.place(x = 10, y = 280, width = 350 )
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila) # detectar eventos en la tabla
        

    # def regresar(self):
    #     self.venDos.destroy()
    #     self.vetana.deiconify()
    

    



if __name__ == "__main__":
    crearBaceDatos() # los primero que hace es crear la base de datos
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()