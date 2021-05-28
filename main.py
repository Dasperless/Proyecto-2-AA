import tkinter as tk
import tkinter.filedialog as fd
from fractalTree import fractalTree

class interface(tk.Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.master = master
		self.imageLabel = None
		self.windowSettings()
		self.uploadImageWindow()

	def windowSettings(self):
		self.master.resizable(0,0)
		self.master.title("Algoritmos genéticos")
		self.grid()

	#Ventana con las opciones de subir una imagen
	def uploadImageWindow(self):
		tk.Label(self, text = "Sube una silueta de un árbola para iniciar el algoritmo").grid(row = 0,column=0,columnspan=3)
		self.imageLabel = tk.Label(self)
		self.imageLabel.grid(row=1,column=0)
		tk.Button(self, text = "Subir imágen", command= lambda:self.uploadImage(), borderwidth=1, height=2, width=10).grid(row=2, column=0,columnspan=3)
		tk.Button(self, text = "Iniciar", command= lambda:self.createTreeWindow(), borderwidth=1, height=2, width=10).grid(row=3, column=0,columnspan=3)

	#Esta funcion sube una imagen y actualiza el label que la contiene
	def uploadImage(self):
		pickedfiletypes = (('png files', '*.png'), ('gif files', '*.gif'))
		imagePath = fd.askopenfilename(parent=self,title= "Selecciona una silueta",   filetypes= pickedfiletypes)
		photo = tk.PhotoImage(file=imagePath)
		self.master.photo = photo
		self.imageLabel.config(image=photo)
		self.imageLabel.grid(row=1,column=0)
		print(imagePath)

	#Función que abre la interfaz para crear el arbol
	def createTreeWindow(self):
		test = fractalTree()
		# test.createTree(300, 550, -90, 20, 9 , 10,1)
		test.createTree(300, 600, -90, 20, 15, 10, 1, 2, 0)


root = tk.Tk()
gui = interface(master=root)
gui.mainloop()