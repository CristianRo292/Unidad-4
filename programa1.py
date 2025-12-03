from tkinter import *  # se importa todo / import everything
from tkinter import messagebox  # para mensajes emergentes / for popup messages



class Principal():
    def __init__(self, master):
        self.vetana = master  # ventana principal raíz / main root window
        self.vetana.title("Practica  1 Parcial 3")  # título de la ventana / window title
        
        ancho_vetanatana  = 250  # ancho fijo / fixed width
        alto_vetanatana = 200  # alto fijo / fixed height

        # obtener tamaño de pantalla / get screen size
        ancho_pantalla = self.vetana.winfo_screenwidth()
        alto_pantalla = self.vetana.winfo_screenheight()

        # calcular centro / calculate center
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        # aplicar geometría / apply geometry
        self.vetana.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        
    def inicio(self):
        # etiqueta y entrada 1 / label & input 1
        Label(self.vetana, text="Escribe un numero: ").place(x=20, y=20)
        self.n1 = Entry(self.vetana)  # caja de texto / text box
        self.n1.place(x=50, y=50)

        # etiqueta y entrada 2 / label & input 2
        Label(self.vetana, text="Escribe un numero ").place(x=20, y=75)
        self.n2 = Entry(self.vetana)
        self.n2.place(x=50, y=100)

        # botón enviar / send button
        Button(self.vetana, text="Enviar", width=15, command=self.enviar).place(x=50, y=130)

        # botón cerrar / close button
        Button(self.vetana, text="Cerrar", width=15, command=self.cerrar).place(x=50, y=160)

        self.vetana.mainloop()  # ciclo principal / main loop

    def enviar(self):
        try:
            caja1 = int(self.n1.get())  # convierte a entero / convert to int
            caja2 = int(self.n2.get())

            # limpiar entradas / clear entries
            self.n1.delete(0, END)
            self.n2.delete(0, END)

            self.vetana.withdraw()  # ocultar ventana / hide window

            otra = Toplevel(self.vetana)  # nueva ventana / new window
            Ventana2(otra, self.vetana, caja1, caja2)  # enviar datos / send data

        except ValueError:
            messagebox.showerror("Error", "Algun dato no es numero 😭")  # error si no es número / error if not numeric
            self.n1.delete(0, END)
            self.n2.delete(0, END)

    def cerrar(self):
        self.vetana.destroy()  # cerrar app / close app



class Ventana2():
    def __init__(self, master, vetana, c1, c2):
        self.venDos = master  # referencia ventana 2 / second window reference
        self.venDos.title("Practica  1 Parcial 3")  # título / title

        ancho_vetanatana  = 250  # ancho / width
        alto_vetanatana = 200  # alto / height

        # obtener tamaño pantalla / get screen size
        ancho_pantalla = self.venDos.winfo_screenwidth()
        alto_pantalla = self.venDos.winfo_screenheight()

        # calcular centro / calculate center
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        # aplicar geometría / apply geometry
        self.venDos.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")

        # etiqueta / label
        Label(self.venDos, text="Hola mundo").place(x=50, y=20)

        # botón regresar / back button
        Button(self.venDos, text="Regresar", width=10, command=self.regresar).place(x=50, y=100)

        # botón sumar / sum button
        Button(self.venDos, text="Sumar", width=10, command=self.sumar).place(x=50, y=50)

        self.vetana = vetana  # ventana principal / main window
        self.c1 = c1  # número 1 / number 1
        self.c2 = c2  # número 2 / number 2

    def regresar(self):
        self.venDos.destroy()  # cerrar ventana 2 / close window 2
        self.vetana.deiconify()  # mostrar ventana principal / show main window

    def sumar(self):
        # mensaje con resultado / message with result
        messagebox.showinfo("Suma", f"La suma de {self.c1} y {self.c2} es: {self.c1 + self.c2}")



if __name__ == "__main__":
    master = Tk()  # ventana raíz / root window
    app = Principal(master)  # instancia / instance
    app.inicio()  # iniciar / start
    master.mainloop()  # ciclo / loop
