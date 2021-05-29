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
		self.master.title("Algoritmos genéticos")
		self.master.geometry("725x500")
		# self.master.resizable(0,0)
		self.grid()

	#Ventana con las opciones de subir una imagen
	def uploadImageWindow(self):
		tk.Label(self, text = "Cargar una silueta", font=("Segoe UI",20)).grid(row = 0,column=1,sticky="NE")
		defaultImg = tk.PhotoImage(file="Img.gif")
		self.master.photo = defaultImg		
		self.imageLabel = tk.Label(self, image = defaultImg)
		self.imageLabel.grid(row=0,column=0,sticky="N")
		tk.Button(self, text = "Subir imágen", font=("Segoe UI",10), command= lambda:self.uploadImage(), borderwidth=1, height=2, width=13).grid(row=0, column=1, sticky="SW")
		tk.Button(self, text = "Iniciar", font=("Segoe UI",10), command= lambda:self.createTreeWindow(), borderwidth=1, height=2, width=13).grid(row=0, column=1, sticky="SE")

	#Esta funcion sube una imagen y actualiza el label que la contiene
	def uploadImage(self):
		pickedfiletypes = (('png files', '*.png'), ('gif files', '*.gif'))
		imagePath = fd.askopenfilename(parent=self,title= "Selecciona una silueta",   filetypes= pickedfiletypes)
		#Si no se seleccionó una imagen evita que se modifique
		if(imagePath != ""):
			photo = tk.PhotoImage(file=imagePath)
			self.master.photo = photo
			self.imageLabel.config(image=photo)
		print(imagePath)

	#Función que abre la interfaz para crear el arbol
	def createTreeWindow(self):
		test = fractalTree()
		# test.createTree(300, 550, -90, 20, 9 , 10,1)
		test.createTree(300, 600, -90, 20, 15, 10, 1, 2, 0)


root = tk.Tk()
gui = interface(master=root)
gui.mainloop()