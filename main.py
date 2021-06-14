import tkinter as tk
import tkinter.filedialog as fd
from tkinter import Listbox, StringVar, font as tkfont
from fractalTree import fractalTree
import tkinter.messagebox as mb


class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title_font = tkfont.Font(
			family='Helvetica', size=18, weight="bold", slant="italic")
		self.title("Algoritmos genéticos")
		self.resizable(0, 0)
		self.imagePath = ""  # path de la imagen que se subirá

		self.geneticApp = fractalTree()  # Clase con el arbol fractal
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand=True)
		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		self.pages = []
		for F, geometry in zip((DashboardPage, UploadPage), ('1240x720', '825x605')):
			page_name = F.__name__
			frame = F(parent=self.container, controller=self)
			self.pages.append(frame)
			# almacena el frame y la geometria para este frame
			self.frames[page_name] = (frame, geometry)
			frame.grid(row=0, column=0, sticky="nsew")

		self.showFrame("UploadPage")

	def showFrame(self, page_name):
		'''Muestra un frame por el nombre de la página'''
		frame, geometry = self.frames[page_name]
		self.update_idletasks()
		self.geometry(geometry)
		frame.tkraise()


class DashboardPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# Scroll
		labelScrollListBox = tk.LabelFrame(self, text="Árboles")
		labelScrollListBox.grid(row=0, column=0, sticky="ENS", rowspan=45)
		self.listbox = tk.Listbox(labelScrollListBox, height=43, width=40)
		self.listbox.pack(side="left", fill="both")

		scrollbar = tk.Scrollbar(labelScrollListBox)
		scrollbar.pack(side="right", fill="both")

		self.listbox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.listbox.yview)

		# Labels
		self.labelFrameChrm = tk.LabelFrame(self, text="Cromosomas")
		self.labelFrameChrm.grid(row=0, column=1, sticky="N")

		self.labelFrameChrmP1 = tk.LabelFrame(self, text="Cromosomas Padre 1")
		self.labelFrameChrmP1.grid(row=0, column=2, sticky="N")

		self.labelFrameChrmP2 = tk.LabelFrame(self, text="Cromosomas Padre 2")
		self.labelFrameChrmP2.grid(row=0, column=3, sticky="N")

		# Cromosomas del padre 1
		self.ParentChromoStr = StringVar()
		self.labelParent1 = tk.Label(
			self.labelFrameChrmP1, textvariable=self.ParentChromoStr, anchor='w')
		self.labelParent1.pack()

		# Cromosomas del padre 2
		self.Parent2ChromoStr = StringVar()
		self.labelParent2 = tk.Label(
			self.labelFrameChrmP2, textvariable=self.Parent2ChromoStr, anchor='w')
		self.labelParent2.pack()

		# Cromosomas del árbol actual
		self.ChromosomeStr = StringVar()
		self.labelChromosomes = tk.Label(
			self.labelFrameChrm, textvariable=self.ChromosomeStr, justify="left")
		self.labelChromosomes.pack()

	# carga los datos del algoritmo genético
	def loadData(self):
		image = self.controller.imagePath
		self.controller.geneticApp.algoritmoGenetico(image)
		self.treeList = self.controller.geneticApp.FractalDict
		self.updateListBox(self.listbox, self.treeList)

	# Carga los datos del arbol seleccionado de la lista
	def callback(self, event):
		selection = event.widget.curselection()
		if selection:
			index = selection[0]
			data = event.widget.get(index)
			strChrm = self.formatChromosomes(self.treeList[index]["Parametros"])
			self.ChromosomeStr.set(strChrm)
	
	#Retorna un string con el significado de los parámetros de los cromosomas.
	def formatChromosomes(self, chromosomes):
		strFormated = ""
		labels = ["Ángulo:","Ángulo de inclinación:","Profundidad:","Largo de la base:",
				"Decrecimiento del largo:","Diámetro de la base:","Decrecimiento de la base:"]
		max_len = max(len(l) for l in labels)
		for i in range(len(chromosomes)):
			string = '{}'
			strFormated+= string.format(labels[i].ljust(max_len+1)+str(chromosomes[i]))+"\n"
		return strFormated
	# Actualiza la lista de árboles.
	def updateListBox(self, listbox, list):
		for key in list:
			listbox.insert("end", "Árbol " + str(key))
		listbox.bind("<<ListboxSelect>>", self.callback)


class UploadPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.isClicked = False
		self.uploadImageWindow()

	# Ventana con las opciones de subir una imagen
	def uploadImageWindow(self):
		tk.Label(self, text="Cargar una silueta", font=(
			"Segoe UI", 20)).grid(row=0, column=1, sticky="NE")
		defaultImg = tk.PhotoImage(file="Img.gif")			# imagen por defecto
		self.master.photo = defaultImg 						# Evita ser eliminado por el garbage colector
		# Label con la imagen por defecto
		self.imageLabel = tk.Label(self, image=defaultImg)
		self.imageLabel.grid(row=0, column=0, sticky="N")
		# boton de subir imagen
		tk.Button(self, text="Subir imágen", font=("Segoe UI", 10), command=lambda: self.uploadImage(
		), borderwidth=1, height=2, width=13).grid(row=0, column=1, sticky="SW")
		# boton de iniciar
		tk.Button(self, text="Iniciar", font=("Segoe UI", 10), command=lambda: self.checkImg(
		), borderwidth=1, height=2, width=13).grid(row=0, column=1, sticky="SE")

	# Esta funcion sube una imagen y actualiza el label que la contiene
	def uploadImage(self):
		pickedfiletypes = (('gif files', '*.gif'), ('png files', '*.png'))
		self.controller.imagePath = fd.askopenfilename(
			parent=self, title="Selecciona una silueta",   filetypes=pickedfiletypes)
		# Si no se seleccionó una imagen evita que se modifique
		if(self.controller.imagePath != ""):
			if(self.controller.geneticApp.checkImgResolution(self.controller.imagePath)):
				photo = tk.PhotoImage(file=self.controller.imagePath)
				self.master.photo = photo
				self.imageLabel.config(image=photo)
			else:
				mb.showinfo(
					"Resolución", "La resolución de la imagen debe ser 600x600")
				# Elimino el path de la imagen con resolución incorrecta.
				self.controller.imagePath = ""

	# Función que abre la interfaz para crear el arbol
	def checkImg(self):
		if(self.controller.imagePath != ""):
			self.controller.showFrame("DashboardPage")
			if(not self.isClicked):
				self.controller.pages[0].loadData()
				self.isClicked = True

		else:
			mb.showinfo("Imagen", "No se ha cargado una silueta")


if __name__ == "__main__":
	app = App()
	app.mainloop()
