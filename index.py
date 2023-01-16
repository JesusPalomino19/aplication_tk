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
		self.vent.bind("<Return>", lambda event: self.agregar_productos())#Funcion Bind agregado a la ventana para que al presionar la tecla "Enter",  se accione el metodo agregar producto
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
		ttk.Button(text = "Eliminar Producto", command = self.eliminar_productos).grid(row = 5, column = 0, sticky = W + E) 
		ttk.Button(text = "Editar Informacion", command = self.editar_producto).grid(row = 5, column = 1, sticky = W + E)

		#Ejecutamos la obtencion de datos para llenar la tabla
		self.obtener_productos()
		self.vent.update()

		#Forma de hacre que la ventana se genere en la mitad de cualquier pantalla
		dimensiones_vent = (self.vent.winfo_reqwidth(), self.vent.winfo_reqheight())
		dimensiones_pantalla = (self.vent.winfo_screenwidth(), self.vent.winfo_screenheight())
		dimensiones_centro = (int((dimensiones_pantalla[0]-dimensiones_vent[0])/2), int((dimensiones_pantalla[1]-dimensiones_vent[1])/2))
		self.vent.geometry("+" + str(dimensiones_centro[0]) + "+" + str(dimensiones_centro[1]))

	#Funcion encargada del enlace a la base de datos
	def ejecuta_consulta(self, consulta, parametros = ()):
		#Se utiliza una funcion de libreria para conectar con la base da datos
		with sqlite3.connect(self.db_nombre) as conn:
			cursor = conn.cursor()
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

	#Funcion para corroborar si los valores estan llenos
	def son_vacios(self):
		return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0

	#Funcion para saber si el valor del precio es flotante
	def es_flotante(self):
		try:
			float(self.precio.get())
			return True
		except ValueError:
			return False


	#Funcion que valida el ingreso correcto a la base de datos
	def validacion(self):
		son_numeros = str.isdigit(self.precio.get()) or self.es_flotante()#primero se evalua si el contenido es un numero, y el otro si es un flotante
		return self.son_vacios() and son_numeros

	#Funcion para agregar productos a la tabla
	def agregar_productos(self):
		#Usamos la funcion validacion
		if self.validacion():
			consulta = "INSERT INTO productos VALUES(NULL, ?, ?)"
			parametros = (self.nombre.get(), self.precio.get())
			self.ejecuta_consulta(consulta, parametros)
			#Actualizamos el valor de texto que esta en la notificacion de modificacion
			self.mensaje["text"] = "Producto {} fue agregado de manera correcta...".format(self.nombre.get())
			#Eliminamos los datos del entry luego de agregar sus datos
			self.nombre.delete(0, END)
			self.precio.delete(0, END)
		else:
			self.mensaje["text"] = "Nombre y Precio(solo ingreso de numeros) son requeridos, "
		self.obtener_productos()
		self.nombre.focus()#Hacemos focus al nombre para seguir agregando datos si asi lo requiera el usuario

	#Funcion para eliminacion de productos
	def eliminar_productos(self):
		self.mensaje["text"] = None#Limpiamos la notificacion en caso ya este llena
		#Se usa un try and catch en caso de que el usuario no haya seleccionado nada
		try:
			#Se obtiene el texto del campo dentro del arbol ha sido seleccionado 
			self.arbol.item(self.arbol.selection())["text"][0]
		except IndexError as e:
			#Mensaje de error en caso la seleccion haya sido una fila vacia
			self.mensaje["text"] = "Por favor selecione un elemento o fila"
			return
		self.mensaje["text"] = None#Limpiamos la notificacion en caso ya este llena
		nombre = self.arbol.item(self.arbol.selection())["text"]#En esta variable se almacena el elemento selecionado 
		consulta = "DELETE FROM productos WHERE nombre = ?"
		self.ejecuta_consulta(consulta, (nombre, ))#Se ejecuta una consulta a la BD para eliminar el elemento en cuestion, se pone la "," luego de nombre para que se pueda identificar como tupla
		self.mensaje["text"] = "Registro {} ha sido borrado satisfactoriamente".format(nombre)#Se actualiza el mensaje de Notificacion
		self.obtener_productos()#Actualizamos la tabla de valores para ya no obtener el valor eliminado

	#Funcion que me permite editar un producto selccionado
	def editar_producto(self):
		self.mensaje["text"] = None#Limpiamos la notificacion en caso ya este llena
		#Se usa un try and catch en caso de que el usuario no haya seleccionado nada
		try:
			#Se obtiene el texto del campo dentro del arbol ha sido seleccionado 
			self.arbol.item(self.arbol.selection())["text"][0]
		except IndexError as e:
			#Mensaje de error en caso la seleccion haya sido una fila vacia
			self.mensaje["text"] = "Por favor selecione un elemento o fila"
			return
		nombre = self.arbol.item(self.arbol.selection())["text"]#Seleccion del nombre del producto a editar
		precio_anterior = self.arbol.item(self.arbol.selection())["values"][0]#Seleccion del precio anterior(recordar que es una tupla)
		#Hacemos uso de TopLevel una ventana que se pondra encima de la que tenemos actualmente
		self.ventana_edit = Toplevel()
		self.ventana_edit.tittle = "Editar Producto"
		self.ventana_edit.bind("<Return>", lambda event: self.editar_datos(nuevo_nombre.get(), nombre, nuevo_precio.get(), precio_anterior))#Funcion para que la tecla "Enter" acione el boton		Label(self.ventana_edit, text = "Nombre Anterior: ").grid(row = 0, column = 1, sticky = W)#Nombre Anterior
		Entry(self.ventana_edit, textvariable = StringVar(self.ventana_edit, value = nombre), state = "readonly").grid(row = 0, column = 2)
		Label(self.ventana_edit, text = "Nuevo Nombre: ").grid(row = 1, column = 1, sticky = W)#Nuevo Nombre
		nuevo_nombre = Entry(self.ventana_edit)
		nuevo_nombre.grid(row = 1, column = 2)
		Label(self.ventana_edit, text = "Precio Anterior: ").grid(row = 2, column = 1, sticky = W)#Precio Anterior
		Entry(self.ventana_edit, textvariable = StringVar(self.ventana_edit, value = precio_anterior), state = "readonly").grid(row = 2, column = 2)
		Label(self.ventana_edit, text = "Nuevo Precio: ").grid(row = 3, column = 1, sticky = W)#Nuevo Precio
		nuevo_precio = Entry(self.ventana_edit)
		nuevo_precio.grid(row = 3, column = 2)
		#Boton que se usara para actualizar datos
		Button(self.ventana_edit, text = "Actualizar Datos", command = lambda: self.editar_datos(nuevo_nombre.get(), nombre, nuevo_precio.get(), precio_anterior)).grid(row = 4, column = 2, sticky = W + E)
		#Uso de metodo para que el pop-up se genere en el centro
		dimensiones_ventana_edit = (self.ventana_edit.winfo_reqwidth(), self.ventana_edit.winfo_reqheight())
		dimensiones_pantalla = (self.ventana_edit.winfo_screenwidth(), self.ventana_edit.winfo_screenheight())
		dimensiones_centro = (int((dimensiones_pantalla[0]-dimensiones_ventana_edit[0])/2), int((dimensiones_pantalla[1]-dimensiones_ventana_edit[1])/2))
		self.ventana_edit.geometry("+" + str(dimensiones_centro[0]) + "+" + str(dimensiones_centro[1]))

	#Funcion que permite editar datos guardados en la tabla
	def editar_datos(self, nuevo_nombre, nombre, nuevo_precio, precio):
		consulta = "UPDATE productos SET Nombre = ?, Precio = ? WHERE Nombre = ? AND Precio = ?"
		parametros = (nuevo_nombre, nuevo_precio, nombre, precio)#Parametro que se pasan a la consulta
		self.ejecuta_consulta(consulta, parametros)
		self.ventana_edit.destroy()#Luego de haberse ejecutado la consulta se destruye el pop-up
		self.mensaje["text"] = "Producto {} ha sido actualizado satisfactoriamente".format(nombre)#Se presenta un mensaje que señala que el producto se actualizo
		self.obtener_productos()#Se cargan los datos(para mostrar el actualizado)

#Arranque de aplicacion
if __name__ == "__main__":
	#Ventana principal, que pasa como parametro al constructor de producto
	ventana = Tk()
	aplicacion = producto(ventana)
	ventana.mainloop()  
