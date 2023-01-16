#Importacion de bibliotecas graficas
from tkinter import ttk
from tkinter import *

#Importamos el modulo de conexion
import sqlite3

#Clase producto para la creacion de ventanas
class producto:
	#Conexion a la base de datos "sqlite"
	db_nombre = "database.db"#Propiedad dentro del porgrama que hace referencia al archivo de base de datos

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
		ttk.Button(contenedor, text = "Guardar producto ", command = self.agregar_productos).grid(row = 3, columnspan = 2, sticky = W + E)

		#Notificaciones de modificacion
		self.mensaje = Label(text = "", fg = "red")
		self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)


		#Creacion de una tabla para agregar datos, se guarda para eliminar o agregar datos
		self.arbol = ttk.Treeview(height = 10, columns = 2)
		self.arbol.grid(row = 4, column = 0, columnspan = 2)
		#Encabezados(heading) de la tabla o arbol, anchor es para que el texto este centrado
		self.arbol.heading("#0", text = "Nombre", anchor = CENTER)
		self.arbol.heading("#1", text = "Precio", anchor = CENTER)

		#Botones de modificacion de productos existentes de la tabla
		ttk.Button(text = "BORRAR", command = self.eliminar_productos).grid(row = 5, column = 0, sticky = W + E) 
		ttk.Button(text = "	EDITAR").grid(row = 5, column = 1, sticky = W + E)

		#Ejecutamos la obtencion de datos para llenar la tabla
		self.obtener_productos()


	#Funcion encargada del enlace a la base de datos
	def ejecuta_consulta(self, consulta, parametros = ()):
		#Se utiliza una funcion de libreria para conectar con la base da datos
		with sqlite3.connect(self.db_nombre) as conn:
			cursor = conn.cursor()
			#Se hace uso de una funcion recursiva
			resultado = cursor.execute(consulta, parametros)#si existiesen valores en la tabla se guardan en resultado que es una tupla
			conn.commit()
		return resultado

	#Funcion que obtiene los datos almacenados en mi base de datos
	def obtener_productos(self):
		#Obtenemos los hijos existentes en la tabla y si existen, los eliminamos para actualizar sus valores
		guardados = self.arbol.get_children()
		for elemento in guardados:
			self.arbol.delete(elemento)
		#Se obtienen los datos desde la base de datos
		consulta = "SELECT * FROM productos ORDER BY nombre DESC"
		db_filas = self.ejecuta_consulta(consulta)
		#Llenando los datos en la tabla
		for fila in db_filas:
			self.arbol.insert("", 0, text = fila[1], values = fila[2])

	#Funcion que valida el ingreso de datos a la base de datos
	def validacion(self):
		return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0		

	#Funcion para agregar productos a la tabla
	def agregar_productos(self):
		#Usamos la funcion validacion
		if self.validacion():
			consulta = "INSERT INTO productos VALUES(NULL, ?, ?)"
			parametros = (self.nombre.get(),self.precio.get())
			self.ejecuta_consulta(consulta, parametros)
			#Eliminamos los datos del entry luego de agregar sus datos
			self.nombre.delete(0, END)
			self.precio.delete(0, END)
			#Actualizamos el valor de texto que esta en la notificacion de modificacion
			self.mensaje["text"] = "Producto {} fue agregado de manera correcta...".format(self.nombre.get())
		else:
			self.mensaje["text"] = "Nombre y Precio son requeridos"
		self.obtener_productos()

	#Funcion para eliminacion de productos
	def eliminar_productos(self):
		print(self.arbol.item(self.arbol.selection()))
		self.arbol.item(self.arbol.selection())


#Arranque de aplicacion
if __name__ == "__main__":
	#Ventana principal, que pasa como parametro al constructor de producto
	ventana = Tk()
	aplicacion = producto(ventana)
	ventana.mainloop()  
