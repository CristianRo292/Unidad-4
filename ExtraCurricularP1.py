'''Hacer un programa que eun una base de datos guarde el nombre y 3 calificaciones de un alumno,
el programa va a permitir agregar alumnos y sus calificaciones y eliminarlos, por lo tanto tiene que tener una 
tabla para ver los datos.'''

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3

def crearBaseDatos():
    obBaseDatos = sqlite3.connect("restro_alumnos.db")
    cursor =  obBaseDatos.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alumnos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   calf_uno INTEGER NOT NULL,
                   calf_dos INTEGER NOT NULL,
                   calf_tres INTEGER NOT NULL,
                   calf_prom REAL NOT NULL
                   )
                    ''')
    obBaseDatos.commit()
    obBaseDatos.close()


class Principal():
    def __init__(self, master):
        self.ventana = master
        # dimenciones de mi ventana 
        ancho_vetanatana  = 550 
        alto_vetanatana = 500
        #Dimeniones de mi pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        #coordenadas de la ventana 
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)
        #Creamos la vetana con las dimenciones deseadas
        self.ventana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        self.index = None

    def inicio(self):
        Label(self.ventana, text = "Nombre").place(x = 1, y = 5)
        self.nombre = Entry(self.ventana)
        self.nombre.place(x = 1, y = 30)
        Label(self.ventana, text = "Calificacion 1:").place(x = 130, y = 5)
        self.calificacion_uno = Entry(self.ventana)
        self.calificacion_uno.place(x = 130, y = 30)
        Label(self.ventana, text = "Calificacion 2:").place(x = 260, y = 5)
        self.califiacion_dos = Entry(self.ventana)
        self.califiacion_dos.place(x = 260, y = 30)
        Label(self.ventana, text = "Calificacion 3:").place(x = 390, y = 5)
        self.califiacion_tres = Entry(self.ventana)
        self.califiacion_tres.place(x = 390, y = 30)
        # cracion de tabla
        columnas = ("ID","Nombre", "C1", "C2", "C3", "Promedio")
        self.tabla = ttk.Treeview(self.ventana, columns = columnas, show = "headings") # se crea la tabla, se indica que tenga la cantidad de 
        self.tabla.place(x = 2, y = 55, width = 500, height = 190)                     # columnas igual a la cantidad de lemenor en la variable columnas

        for col in columnas:
            self.tabla.heading(col, text = col) # se agrega el datos al encabezado
            self.tabla.column(col, anchor = "center", width = 30) # se indica el tamaño que debera tener la celda
        
        self.actualizarTabla()

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila) # detectar eventos en la tabla
        
        # botones
        self.btnAgregar = Button(self.ventana, text = "Agregar", command = self.agregar)
        self.btnAgregar.place(x = 10, y = 260)
        self.btnModificar = Button(self.ventana, text = "Modificar", command = self.modificar, state = "disabled")
        self.btnModificar.place(x = 100, y = 260)
        self.btnEliminar = Button(self.ventana, text = "Eliminar", command = self.eliminar, state = "disabled")
        self.btnEliminar.place(x = 200, y = 260)
        self.btnSalir = Button(self.ventana, text = "Salir", command = self.salir)
        self.btnSalir.place(x = 400, y = 260)


    def agregar(self):
        if self.validarCajasBacias():
            nom,c1,c2,c3 = self.extraerDatosDeCajas()
            promedio = self.promRapido((nom,c1,c2,c3))
            print(promedio)
            obBaseDatos = sqlite3.connect("restro_alumnos.db")
            cursor = obBaseDatos.cursor()
            cursor.execute("INSERT INTO alumnos(name,calf_uno,calf_dos,calf_tres,calf_prom) VALUES (?,?,?,?,?)",(nom,c1,c2,c3,promedio,))
            obBaseDatos.commit()
            obBaseDatos.close()
            self.borrarCajas()
            self.actualizarTabla()


    def modificar(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        # Validar que los campos no estén vacíos antes de actualizar
        # Validate that fields are not empty before updating
        if self.validarCajasBacias():
            valores = self.tabla.item(self.index,"values")
            # print(valores)
            id = valores[0]
            nom,c1,c2,c3 = self.extraerDatosDeCajas()
            promedio = self.promRapido((nom,c1,c2,c3))

            obBaseDatos = sqlite3.connect("restro_alumnos.db")
            cursor = obBaseDatos.cursor()
            # Actualiza ambas tablas
            # Update both tables
            cursor.execute("UPDATE alumnos SET name=?, calf_uno=?, calf_dos=?, calf_tres=?, calf_prom=? WHERE id=?", (nom,c1,c2,c3,promedio, id))
            obBaseDatos.commit()
            obBaseDatos.close()
            self.actualizarTabla()
            self.borrarCajas()
            self.btnAgregar.config(state= "normal")
            self.btnModificar.config(state="disabled")
        else:
            messagebox.showerror("Error", "Faltan datos")


    def eliminar(self):
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        
        valores = self.tabla.item(self.index,"values")
        id = valores[0]
        obBaseDatos = sqlite3.connect("restro_alumnos.db")
        cursor = obBaseDatos.cursor()
        # Elimina de ambas tablas usando el ID
        # Deletes from both tables using the ID
        cursor.execute("DELETE FROM alumnos WHERE id=?",(id,)) # (f"DELETE FROM usuarios WHERE id={id}"
        obBaseDatos.commit()
        obBaseDatos.close()
        self.actualizarTabla()
        self.borrarCajas()
        self.btnAgregar.config(state= "normal")
        self.btnEliminar.config(state="disabled")
        self.btnModificar.config(state="disabled")
    

    def salir(self):
        self.ventana.destroy()
    
            
    def seleccionFila(self, event):
        self.borrarCajas()
        try: 
            self.index = self.tabla.selection()[0] # obtengo solo la direccion que estoy seleccionando
            
        except:
            return
        
        # Llena los campos de entrada con los valores de la fila seleccionada
        # Fills the entry fields with the values of the selected row
        valores = self.tabla.item(self.index,"values")
        self.nombre.insert(0,valores[1])
        self.calificacion_uno.insert(0, valores[2] )
        self.califiacion_dos.insert(0,valores[3])
        self.califiacion_tres.insert(0, valores[4])
        # Habilita botones de modificar/eliminar y deshabilita agregar
        # Enables modify/delete buttons and disables add
        self.btnAgregar.config(state= "disabled")
        self.btnModificar.config(state="normal")
        self.btnEliminar.config(state="normal")



    def actualizarTabla(self):

        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        self.mostrarDatos()

    def mostrarDatos(self):
        obBaseDatos = sqlite3.connect("restro_alumnos.db")
        cursor = obBaseDatos.cursor()
        cursor.execute("SELECT * FROM alumnos")
        datos = cursor.fetchall()
        # print(datos)
        for i in datos:
            self.tabla.insert("",END, values = i)
        obBaseDatos.commit()
        obBaseDatos.close()
    
    def borrarCajas(self):
        self.nombre.delete(0, END)
        self.calificacion_uno.delete(0, END)
        self.califiacion_dos.delete(0,END)
        self.califiacion_tres.delete(0, END)


    def promRapido(self, resultados):
        cnt = 0
        prom = 0.0
        for i in range( 1, len(resultados)):
            cnt += resultados[i]
        
        prom = cnt/(len(resultados) -1)

        return prom


    def validarCajasBacias(self):
        if (len(self.nombre.get()) != 0 
            and len(self.calificacion_uno.get()) != 0 
            and len(self.califiacion_dos.get()) != 0 
            and len(self.califiacion_tres.get()) != 0):

            return True
        messagebox.showerror("Error", "Campos bacios")
        return False

    def extraerDatosDeCajas(self):
        try:
            nombre = self.nombre.get()
            if nombre.isalpha():
                calificacion1 = int(self.calificacion_uno.get())
                calificacion2 = int(self.califiacion_dos.get())
                calificacion3 = int(self.califiacion_tres.get())

                return nombre, calificacion1, calificacion2, calificacion3
        except:
            messagebox.showerror("Error", "Datos no validos")

        messagebox.showerror("Error", "Datos no validos")

        return False









if __name__ == "__main__":
    crearBaseDatos()
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()
