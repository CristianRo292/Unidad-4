from tkinter import *   # 📦 Importa todos los widgets de Tkinter / Imports all tkinter widgets
from tkinter import messagebox   # 💬 Ventanas emergentes para mensajes / Popup message dialogs
from tkinter import ttk   # 🎛️ Widgets avanzados como Treeview / Advanced widgets like Treeview
import tkinter as tk      # 🖼️ Alias para usar tkinter / Alias to use tkinter
import sqlite3            # 🗄️ Manejo de base de datos SQLite / SQLite database handling

def crearBaceDatos():
    obBaseDatos = sqlite3.connect("usuarios.db")  # 🔌 Conecta o crea la BD / Connects or creates database
    cursor = obBaseDatos.cursor()                 # 📝 Cursor para ejecutar comandos SQL / SQL command cursor

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT NOT NULL,
                   password TEXT NOT NULL)
                   ''')  # 🏗️ Crea tabla si no existe / Creates table if not exists
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'") # 🔍 Busca usuario admin / Searches admin
    # si si existe regresa un TRUE, por lo tanto no agrega otro admin, ya que la condicion no se cumple
    if not cursor.fetchone():  # ✔️ Si no existe admin, lo crea / If admin not found, inserts it
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)", ("admin","12345")) # se ingresa el dato a la base de datos
    
    obBaseDatos.commit()       # 💾 Guarda cambios / Saves changes
    obBaseDatos.close()        # despues de cada consulta siempre se debe cerrar la base de datos / always close DB

class Principal():
    def __init__(self, master):
        self.vetana = master # vetanatana primaria para todo el programa / Main window for the program
        self.vetana.title("Practica  2 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title

        ancho_vetanatana  = 250  # 📏 Ancho de la vetanatana / Window width
        alto_vetanatana = 200   # 📐 Alto / Window height

        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.vetana.winfo_screenwidth()   # 🖥️ Ancho de pantalla / Screen width
        alto_pantalla = self.vetana.winfo_screenheight()   # 🖥️ Alto / Screen height

        # Calcular posición para centrar
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)  # 🎯 Centrado horizontal / Center X
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)    # 🎯 Centrado vertical / Center Y

        self.vetana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")  # 📍 Coloca ventana centrada / Center window

    def inicio(self):
        # caja 1
        Label(self.vetana, text = "Usuario ").place(x = 20, y = 20)  # 🏷️ Etiqueta usuario / Username label
        self.n1 = Entry(self.vetana)  # ✏️ Entrada usuario / Username input
        self.n1.place(x = 50, y = 50)

        # caja 2
        Label(self.vetana, text= "Password").place(x = 20, y = 75)  # 🏷️ Etiqueta password / Password label
        self.n2 = Entry(self.vetana, show="x")  # 🔐 Entrada oculta / Hidden input
        self.n2.place(x = 50, y = 100)

        # botones
        Button(self.vetana, text = "Validar", width=10, command= self.enviar).place(x = 30, y = 140)  # ✔️ Validar datos / Validate
        Button(self.vetana, text = "Cerrar", width=10, command= self.cerrar).place(x = 150, y = 140) # ❌ Cierra app / Close app

    def enviar(self):
        u = self.n1.get()  # 🧾 Obtiene usuario / Gets username
        p = self.n2.get()  # 🔑 Obtiene password / Gets password

        con = sqlite3.connect("usuarios.db")  # 🔌 Conexión BD / Connect DB
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? and password=?", (u,p)) # busca si ya existe ese usuario "admin"
        resultado = cursor.fetchone() # preguntamos si encontrol el registro admin
        con.close()

        if resultado: # si si lo ecnontro pasamos a la otra ventana
            self.n1.delete(0, END)  # 🧹 Limpia entrada / Clear input
            self.n2.delete(0, END)
            self.vetana.withdraw() # oculta la ventana 🙈 / Hides login window

            otra = Toplevel(self.vetana) # 🪟 Nueva ventana secundaria / New window
            Ventana2(otra, self.vetana, u) # se va con la otra / Goes to main window
            return 1
        
        self.n1.delete(0, END)
        self.n2.delete(0, END)
        messagebox.showerror("Error", "Datos incorrectos 🥺")  # ❌ Datos incorrectos / Wrong credentials

    def cerrar(self):
        self.vetana.destroy()  # 🛑 Cierra programa / Close application

    
class Ventana2 ():
    def __init__(self, master,vetana, u): # recive lo que le madaron
        self.venDos = master    # 🪟 Ventana hija / Child window
        self.usuario = u        # 🙋 Usuario actual / Current user
        self.vetana = vetana    # 🔙 Ventana principal oculta / Hidden main window

        self.venDos.title("Practica  1 Parcial 3")  # 🏷️ Título / Title

        ancho_vetanatana  = 550  # 📏 Ancho / Width
        alto_vetanatana = 320    # 📐 Alto / Height

        ancho_pantalla = self.venDos.winfo_screenwidth()
        alto_pantalla = self.venDos.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        self.venDos.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")

        Label(self.venDos, text = "Escribe el usuario").place(x = 10, y = 10)  # 📝 Etiqueta / Label
        self.usuarioVenDos = Entry(self.venDos)  # ✏️ Entrada usuario / Input for user
        self.usuarioVenDos.place(x = 10, y = 30)

        Label(self.venDos, text = "Escribe el Password").place(x = 150, y = 10)
        self.contraseñaN = Entry(self.venDos) # 🔐 Nueva contraseña / New password
        self.contraseñaN.place(x = 150, y = 30)

        self.us = Label(self.venDos,  text = "")
        self.us.place(x = 300, y = 10)
        self.us.config(text = f"Bienvenido \n {self.usuario}")  # 🙋 Mensaje bienvenida / Welcome message

        self.mostrar()       # 📊 Crea tabla / Creates table
        self.mostrar_tabla() # 📥 Llena tabla / Loads data

        self.menus = tk.Menu(self.venDos)      # 📁 Barra menú / Menu bar
        self.venDos.config(menu = self.menus)
        self.archivo = tk.Menu(self.menus, tearoff = 0)

        self.archivo.add_command(label = "Salir", command = self.salir)              # 🚪 Cerrar / Exit
        self.archivo.add_command(label = "Modificar", command = self.modificarUsuario) # 📝 Editar / Modify
        self.indexModificar = self.archivo.index("end")

        self.archivo.add_command(label = "Eliminar", command = self.eliminarUsuario)  # 🗑️ Borrar / Delete
        self.indexEliminar = self.archivo.index("end")

        self.archivo.add_command(label = "Agregar", command = self.crearUsuario)      # ➕ Agregar user / Add user
        self.indexAgregar = self.archivo.index("end")

        self.menus.add_cascade(label = "Archivo", menu = self.archivo)
        self.index = -1

        # ❌ Por defecto se deshabilitan los permisos / Disable all by default
        self.archivo.entryconfig(self.indexAgregar, state = "disable")
        self.archivo.entryconfig(self.indexModificar, state = "disable")
        self.archivo.entryconfig(self.indexEliminar, state = "disable")

        self.roles()  # 🔐 Aplica permisos según usuario / Apply roles

    def roles(self):
        if self.usuario == "admin":  # 👑 Admin: todo permitido / Everything allowed
            self.archivo.entryconfig(self.indexAgregar, state = "normal")
            self.archivo.entryconfig(self.indexModificar, state = "normal")
            self.archivo.entryconfig(self.indexEliminar, state = "normal")

        elif self.usuario in ("Supervisor", "supervisor"): # 👨‍🔧 Supervisor: agregar / add
            self.archivo.entryconfig(self.indexAgregar, state = "normal")
            self.archivo.entryconfig(self.indexModificar, state = "disable")
            self.archivo.entryconfig(self.indexEliminar, state = "disable")
        
        elif self.usuario in ("Jefe de area", "jefe de area"): # 👨‍💼 Jefe: editar / modify
            self.archivo.entryconfig(self.indexAgregar, state = "disable")
            self.archivo.entryconfig(self.indexModificar, state = "normal")
            self.archivo.entryconfig(self.indexEliminar, state = "disable")

    def seleccionFila(self, event):
        try: 
            self.index = self.tabla.selection()[0] # 🔍 Obtiene ID interno de fila / Gets selected row ID
            
        except:
            return
        
        valores = self.tabla.item(self.index,"values") # 📥 Obtiene datos fila / Gets row data
        self.usuarioVenDos.delete(0, END)
        self.contraseñaN.delete(0, END)
        self.usuarioVenDos.insert(0, valores[1])
        self.contraseñaN.insert(0, valores[2])

    def eliminarUsuario(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            valores = self.tabla.item(self.index,"values")
            usuario = valores[1]
            id = valores[0]

            if usuario == self.usuario:  # 🚫 No puede borrarse a sí mismo / Cannot delete itself
                messagebox.showerror("Error", "No te puedes eliminar a ti mismo")
                return 1
                
            obBaseDatos = sqlite3.connect("usuarios.db")
            cursor = obBaseDatos.cursor()
            cursor.execute(f"DELETE FROM usuarios WHERE id={id}") 
            obBaseDatos.commit()
            obBaseDatos.close()

            self.actualizarTabla()
            self.borrarDatos("Usuario Eliminado Corretamente")
            self.index = -1

        except:
            messagebox.showerror("Error", "Elije una fila")  # ⚠️ No seleccionó fila / No row selected
           
    def modificarUsuario(self):
        try: 
            self.index = self.tabla.selection()[0] # Seleccion fila / Select row
        except:
            messagebox.showerror("Error", "Elije un Usuario") # ⚠️ No seleccionó usuario / No user selected
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
            messagebox.showerror("Error","Faltan Datos")  # ⚠️ Campos vacíos / Missing fields

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
        
        messagebox.showerror("Error", "Faltan datos")  # ⚠️ Campos vacíos / Missing fields

    def salir(self):
        self.venDos.destroy()  # ❌ Cierra ventana secundaria / Close child window
        self.vetana.destroy()  # 🔚 Cierra app completa / Close full app
        

    def actualizarTabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)  # 🧹 Limpia tabla / Clears table
        
        self.mostrar_tabla()  # 🔄 Vuelve a cargar / Reload table

    def mostrar_tabla(self):
        con = sqlite3.connect("usuarios.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios") 
        resultado = cursor.fetchall()

        for i in resultado:
            self.tabla.insert("", END, values = i)  # 📌 Inserta fila / Insert row
            print(i)

        con.close()
    
    def borrarDatos(self, mensaje):
        self.usuarioVenDos.delete(0, END)
        self.contraseñaN.delete(0, END)
        messagebox.showinfo("Datos", mensaje)  # 📢 Mensaje informativo / Info message
        
    def mostrar(self):
        columnas = ("ID", "USUARIO", "PASSWORD")
        self.tabla = ttk.Treeview(self.venDos, columns = columnas, show= "headings")
        self.tabla.place(x = 10, y = 100, width = 350, heigh = 190)

        for col in columnas:
            self.tabla.heading(col, text = col)
            self.tabla.column(col, anchor="center", width = 30)

        scrolly = ttk.Scrollbar(self.venDos, orient = "vertical", command = self.tabla.yview)
        scrollx= ttk.Scrollbar(self.venDos, orient = "horizontal", command = self.tabla.xview)
        scrolly.place(x = 360, y = 100, height = 190)
        scrollx.place(x = 10, y = 280, width = 350 )
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila)  # 🖱️ Detecta selección / Detect selection
    

if __name__ == "__main__":
    crearBaceDatos() # los primero que hace es crear la base de datos / first creates DB
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()  # 🔁 Loop principal / Main event loop
