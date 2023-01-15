#Importacion de bibliotecas graficas
from tkinter import ttk
from tkinter import *

#Importamos el modulo de conexion
import sqlite3

#Clase producto para la creacion de ventanas
class producto:
	#Constructor que inicia la ejecucion de la ventana, y guarda en vent si ya existia
	def __init__(self, ventana):
		self.vent = ventana
		self.vent.title("Aplicacion de gestion de Productos")

		#Creamos un contenedor
		contenedor = LabelFrame(self.vent, text = "Registre un nuevo producto")
		contenedor.grid(row = 0, column = 0, columnspan = 3, pady = 20)

		#Input de nombre, ubicado dentro del contenedor
		Label(contenedor, text = "Nombre: ").grid(row = 1, column = 0)
		#caja de texto que se guarda en una propiedad de mi clase
		self.nombre = Entry(contenedor)
		self.nombre.focus()#propiedad que al iniciar el programa haga focus en el objeto
		self.nombre.grid(row = 1, column = 1)#Ubicacion del entry
		
		#Input del precio, ubicado dentro del contenedor
		Label(contenedor, text = "Precio: ").grid(row = 2, column = 0)
		#caja de texto que se guarda en una propiedad de mi clase
		self.precio = Entry(contenedor)
		self.precio.grid(row = 2, column = 1)#Ubicacion del entry

		#Boton de agregar producto, propiedad sticky le dice al boton que ocupe todo el espacio de West(oeste) a East(este)
		ttk.Button(contenedor, text = "Guardar producto ").grid(row = 3, columnspan = 2, sticky = W + E)

		#Creacion de una tabla para agregar datos, se guarda para eliminar o agregar datos
		self.arbol = ttk.Treeview(height = 10, columns = 2)
		self.arbol.grid(row = 4, column = 0, columnspan = 2)



#Arranque de aplicacion
if __name__ == "__main__":
	#Ventana principal, que pasa como parametro al constructor de producto
	ventana = Tk()
	aplicacion = producto(ventana)
	ventana.mainloop()  