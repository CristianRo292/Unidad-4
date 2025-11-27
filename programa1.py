from tkinter import * # se importa todo
from tkinter import messagebox



class Principal():
    def __init__(self, master):
        self.vetana = master # vetanatana primaria para todo el programa
        self.vetana.title("Practica  1 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title
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
        Label(self.vetana, text = "Escribe un numero: ").place(x = 20, y = 20)
        self.n1 = Entry(self.vetana)
        self.n1.place(x = 50, y = 50)
        # caja 2
        Label(self.vetana, text= "Escribe un numero ").place(x = 20, y = 75)
        self.n2 = Entry(self.vetana)
        self.n2.place(x = 50, y = 100)
        # botones
        Button(self.vetana, text = "Enviar", width=15, command= self.enviar).place(x = 50, y = 130)
        Button(self.vetana, text = "Cerrar", width=15, command= self.cerrar).place(x = 50, y = 160)

        self.vetana.mainloop()

    def enviar(self):
        try:
            caja1 = int(self.n1.get())
            caja2 = int(self.n2.get())
            self.n1.delete(0, END)
            self.n2.delete(0, END)
            # self.vetana.whithdraw()
            self.vetana.withdraw() # oculta la ventana
            otra = Toplevel(self.vetana) # manda a llamar a la otra ventana 
            Ventana2(otra, self.vetana, caja1, caja2) # se va con la otra 
        except ValueError:
            messagebox.showerror("Error", "Algun dato no es numero 😭")
            self.n1.delete(0, END)
            self.n2.delete(0, END)

    def cerrar(self):
        self.vetana.destroy()

class Ventana2 ():
    def __init__(self, master,vetana, c1, c2):
        self.venDos = master
        self.venDos.title("Practica  1 Parcial 3")  # 🏷️ Título de la vetanatana / Sets window title
        # self.val = validaciones1()  # 🧩 Crea un objeto de la clase validaciones1 / Creates an instance of validation class
        ancho_vetanatana  = 250  # 📏 Ancho de la vetanatana / Window width
        alto_vetanatana = 200  # 📐 Alto de la vetanatana / Window height

        # ⚙️ Obtiene el ancho y alto de la pantalla en milímetros / Gets screen width and height in millimeters
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.venDos.winfo_screenwidth()
        alto_pantalla = self.venDos.winfo_screenheight()

        # Calcular posición para centrar
        x = (ancho_pantalla // 2) - (ancho_vetanatana // 2)
        y = (alto_pantalla // 2) - (alto_vetanatana // 2)

        # Aplicar geometría
        self.venDos.geometry(f"{ancho_vetanatana}x{alto_vetanatana}+{x}+{y}")
        Label(self.venDos, text = "Hola mundo").place(x = 50, y = 20)
        Button(self.venDos, text = "Regresar",width=10, command= self.regresar).place(x = 50, y = 100)
        Button(self.venDos, text = "Sumar",width=10, command= self.sumar).place(x = 50, y = 50)
        self.vetana = vetana
        self.c1 = c1
        self.c2 = c2

    def regresar(self):
        self.venDos.destroy()
        self.vetana.deiconify()

    def sumar(self):
        messagebox.showinfo("Suma", f"La suma  de {self.c1} y {self.c2} es: {self.c1 + self.c2}")







if __name__ == "__main__":
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()