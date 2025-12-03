'''
hacer un programa en tkinter que en una ventana mediante
una caja de texto lea un numero, ese numero se enviara a
otra ventana donde en un lisbiu, mostrara ese numero, el numero de veces
'''
# Descripción del programa / Program description


from tkinter import *  # importa todo tkinter / import all tkinter
from tkinter import messagebox  # para mensajes emergentes / for popup messages
from tkinter import ttk  # widgets mejorados / improved widgets


class Principal():
    def __init__(self, master):
        self.vetana = master  # ventana principal / main window
        self.vetana.title("Practica  1 Parcial 3")  # título de ventana / window title
        
        ancho_vetanatana  = 250  # ancho de ventana / window width
        alto_vetanatana = 200  # alto de ventana / window height

        # obtener dimensiones de pantalla / get screen dimensions
        ancho_pantalla = self.vetana.winfo_screenwidth()  # ancho pantalla / screen width
        alto_pantalla = self.vetana.winfo_screenheight()  # alto pantalla / screen height

        # calcular posición centrada / calculate centered position
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)  # posición X centrada / centered X
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)  # posición Y centrada / centered Y

        # aplicar geometría / apply geometry
        self.vetana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")  # asigna tamaño / set size
    
    def inicio(self):
        Label(self.vetana, text = "Numero: ").place(x = 100, y = 50)  # etiqueta / label
        self.nume1 = Entry(self.vetana)  # caja de texto / text box
        self.nume1.place(x = 60, y = 100)  # posición entrada / entry position

        Button(self.vetana, text = "Enviar", command = self.enviar).place(x = 100, y = 150)  # botón enviar / send button
        Button(self.vetana, text = "Salir", command = self.destruir).place(x = 200, y = 150)  # botón salir / exit button

    def enviar(self):
        try:
            if len(self.nume1.get()) <= 0:  # valida campo vacío / validate empty field
                messagebox.showerror("Error", "Campo Basio")  # error si vacío / empty field error
                return 1  # termina función / exit function
            
            numero = int(self.nume1.get())  # convierte a entero / convert to int
            self.nume1.delete(0, END)  # limpia caja / clear entry
            self.vetana.withdraw()  # ocultar ventana / hide window

            nuevaVen = Toplevel(self.vetana)  # nueva ventana / new window
            Ventana_lista(nuevaVen, self.vetana, numero)  # envía número a segunda ventana / send number

        except ValueError: 
            messagebox.showerror("Error", "No son numeros")  # error si no es entero / error if not integer
            self  # instrucción sin efecto / no effect

    def destruir(self):
        self.vetana.destroy()  # cerrar ventana / destroy window


class Ventana_lista():
    def __init__(self, master, vetana, dato):
        self.ventaPrimaria = vetana  # referencia ventana principal / main window reference
        self.numero = dato  # número recibido / received number
        self.vetnanaSec = master  # ventana secundaria / secondary window

        self.vetnanaSec.title("Resultado de numero")  # título / title
        
        ancho_vetanatana  = 250  # ancho ventana / window width
        alto_vetanatana = 200  # alto ventana / window height

        # obtener dimensiones pantalla / get screen dimensions
        ancho_pantalla = self.vetnanaSec.winfo_screenwidth()  # ancho pantalla / screen width
        alto_pantalla = self.vetnanaSec.winfo_screenheight()  # alto pantalla / screen height

        # calcular centro / calculate center
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)  # posición centrada X / centered X
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)  # posición centrada Y / centered Y

        # aplicar geometría / apply geometry
        self.vetnanaSec.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")  # asignar tamaño y posición / set window geometry
        
        self.inicio()  # iniciar elementos / start UI
    
    def inicio(self):
        Label(self.vetnanaSec, text = "Resultados de la Operacion").place(x = 50, y = 10)  # etiqueta / label

        self.miLista = Listbox(self.vetnanaSec, height = 10, width = 8, bg = "white")  # lista / listbox
        self.miLista.place(x = 80, y = 30)  # posición / position

        Button(self.vetnanaSec, text = "Regresar", command = self.volver).place(x = 10, y = 50)  # botón volver / return button
        
        self.ingresarDatos()  # cargar datos / load data

    def ingresarDatos(self):

        for i in range(self.numero):  # repetir según número / repeat according to number
            self.miLista.insert(END, self.numero)  # insertar número / insert number

    def volver(self):
        self.vetnanaSec.destroy()  # cerrar ventana secundaria / close secondary window
        self.ventaPrimaria.deiconify()  # mostrar ventana principal / show main window


if __name__ == "__main__":
    master = Tk()  # ventana raíz / root window
    app = Principal(master)  # crear aplicación / create app
    app.inicio()  # iniciar interfaz / start UI
    master.mainloop()  # bucle principal / main loop
