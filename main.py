import tkinter as tk
import tkinter.filedialog as fd
from tkinter import font as tkfont  # python 3
from typing import Container
from fractalTree import fractalTree
import tkinter.messagebox as mb


class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F, geometry in zip((StartPage, PageOne, UploadPage), ('300x300', '500x500', '825x605')):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = (frame,geometry)
			frame.grid(row=0, column=0, sticky="nsew")

		self.showFrame("UploadPage")
		
	def showFrame(self, page_name):
		frame, geometry = self.frames[page_name]
		self.update_idletasks()
		self.geometry(geometry)
		frame.tkraise()


class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="This is the start page", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)

		button1 = tk.Button(self, text="Go to Page One",
							command=lambda: controller.showFrame("PageOne"))
		button2 = tk.Button(self, text="Go to Page Two",
							command=lambda: controller.showFrame("UploadPage"))
		button1.pack()
		button2.pack()


class PageOne(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.controller.resizable(True, True)
		label = tk.Label(self, text="This is page 1", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)
		button = tk.Button(self, text="Go to the start page",
						   command=lambda: controller.showFrame("StartPage"))
		button.pack()


class UploadPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.fractal = fractalTree()  # Clase con el arbol fractal
		# self.windowSettings()
		self.uploadImageWindow()

	def windowSettings(self):
		self.controller.title("Algoritmos genéticos")
		self.controller.resizable(0, 0)
		self.grid()

	# Ventana con las opciones de subir una imagen
	def uploadImageWindow(self):
		self.imagePath = "" 	#path de la imagen que se subirá
		tk.Label(self, text="Cargar una silueta", font=(
			"Segoe UI", 20)).grid(row=0, column=1, sticky="NE")
		defaultImg = tk.PhotoImage(file="Img.gif")			# imagen por defecto
		self.master.photo = defaultImg 						# Evita ser eliminado por el garbage colector
		self.imageLabel = tk.Label(self, image=defaultImg) 	# Label con la imagen por defecto
		self.imageLabel.grid(row=0, column=0, sticky="N")
		# boton de subir imagen
		tk.Button(self, text="Subir imágen", font=("Segoe UI", 10), command=lambda: self.uploadImage(
		), borderwidth=1, height=2, width=13).grid(row=0, column=1, sticky="SW")
		# boton de iniciar
		tk.Button(self, text="Iniciar", font=("Segoe UI", 10), command=lambda: self.createTreeWindow(
		), borderwidth=1, height=2, width=13).grid(row=0, column=1, sticky="SE")

	# Esta funcion sube una imagen y actualiza el label que la contiene
	def uploadImage(self):
		pickedfiletypes = (('png files', '*.png'), ('gif files', '*.gif'))
		self.imagePath = fd.askopenfilename(
			parent=self, title="Selecciona una silueta",   filetypes=pickedfiletypes)
		# Si no se seleccionó una imagen evita que se modifique
		if(self.imagePath != ""):
			if(self.fractal.checkImgResolution(self.imagePath)):
				photo = tk.PhotoImage(file=self.imagePath)
				self.master.photo = photo
				self.imageLabel.config(image=photo)
			else:
				mb.showinfo(
					"Resolución", "La resolución de la imagen debe ser 600x600")
				self.imagePath = ""				# Elimino el path de la imagen con resolución incorrecta.

	# Función que abre la interfaz para crear el arbol
	def createTreeWindow(self):
		if(self.imagePath != ""):
			self.fractal.geneticAlgorithm(self.imagePath)
			self.controller.showFrame("StartPage")
		else:
			mb.showinfo("Imagen", "No se ha cargado una silueta")

if __name__ == "__main__":
	app = App()
	app.mainloop()
