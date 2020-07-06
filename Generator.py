import os

from image_processing import ImageProcessor

# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font
from tkinter import ttk

# Protocol, Plots and utils imports

class Generator:

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initilising GUI Components
		# a. screen and log components
		self.master = master
		self.main_bg = main_bg
		self.sw, self.sh = 800, 800

		self.counter = 0
		self.side = ['FRONT','BACK','LEFT','RIGHT']

		# b. generating
		self.main_bg.destroy()
		self.main_bg = tkinter.Label(self.master, text = 'Select a '+self.side[self.counter]+' image\nto generate the '+self.side[self.counter]+' wear',\
			font = Font(family='Italic Helvetica', size=36, weight='bold'),\
			fg = 'black', bg = 'white', anchor = 'center', compound = 'center')
		self.main_bg.place(x=self.sw/2,y=self.sh/2-200,relwidth=1,relheight=1,anchor='center')

		self.image = filedialog.askopenfilename(initialdir = "./")
		m = re.search('skin_generator/(.+?)$', self.image)
		if m:
			self.image = m.group(1)
		else:
			exit(1)

		print('Image path:',self.image)

		self.master.after(100,self.selectCloth)

	def selectCloth(self):
		self.main_bg.destroy()
		self.main_bg = tkinter.Label(self.master, text = 'Select the cloth type',\
			font = Font(family='Italic Helvetica', size=36, weight='bold'),\
			fg = 'black', bg = 'white', anchor = 'center', compound = 'center')
		self.main_bg.place(x=self.sw/2,y=self.sh/2-200,relwidth=1,relheight=1,anchor='center')

		self.cloth_type = StringVar(self.master)
		self.cloth_type.set("T-Shirt") # default value
		self.w = tkinter.OptionMenu(self.master, self.cloth_type, "T-Shirt", 'Tank Top', 'Long-Sleeve')
		self.w.place(x=self.sw/2,y=self.sh/2,anchor='center')
		self.button = tkinter.Button(self.master, text ="OK", command = self.goSegmentation)	
		self.button.place(x=self.sw/2,y=self.sh/2+200,anchor='center')

	def goSegmentation(self):
		self.main_bg.destroy()
		self.main_bg = tkinter.Label(self.master, text = 'Wait a moment.\nWe are processing your cloth.',\
			font = Font(family='Italic Helvetica', size=28, weight='bold'),\
			fg = 'black', bg = 'white', anchor = 'center', compound = 'center')
		self.main_bg.place(x=self.sw/2,y=self.sh/2-200,relwidth=1,relheight=1,anchor='center')
		self.w.destroy()
		self.button.destroy()

		self.var_barra = tkinter.DoubleVar()
		self.var_barra.set(0)
		self.minha_barra = ttk.Progressbar(self.master, variable=self.var_barra, maximum=100)
		self.minha_barra.place(x=self.sw/2,y=self.sh/2+200,anchor='center')
		self.master.after(100,self.segmentation)

	def segmentation(self):
		# 1. Segmentation
		print('Segmentation')
		self.master.after(100,os.system("python3 Fashion-AI-segmentation/run.py "+self.image))
		self.var_barra.set(20) # k é um número entre 0 e o máximo 
						  # (definido como 30 no exemplo acima)
		self.master.update()

		self.master.after(100,self.goPrep)

	def goPrep(self):
		# 2. Pre-processing the Fashion-AI output
		print('Pre-processing')
		self.processor = ImageProcessor(self.image)
		self.processor.cloth_type = self.cloth_type.get()
		self.processor.side = self.side[self.counter].lower()
		self.master.after(100,self.processor.prep_run)
		self.var_barra.set(40) # k é um número entre 0 e o máximo 
						  # (definido como 30 no exemplo acima)
		self.master.update()
		self.master.after(100,self.goRPersp)

	def goRPersp(self):
		# 3. Removing the perspective
		self.main_bg.destroy()
		self.main_bg = tkinter.Label(self.master, text = 'Select the '+self.side[self.counter]+' side inner area.\n'+
			'Get the perspective in your cut.\nUse the mouse to wrap the area.\nPress \"c\" to cut, \"r\"" to reset and \"y\" to confirm.',\
			font = Font(family='Italic Helvetica', size=18, weight='bold'),\
			fg = 'black', bg = 'white', anchor = 'center', compound = 'center')
		self.main_bg.place(x=self.sw/2,y=self.sh/2-200,relwidth=1,relheight=1,anchor='center')

		print('Removing perspective')
		self.master.after(100,self.processor.remove_perspective)
		self.var_barra.set(60) # k é um número entre 0 e o máximo 
						  # (definido como 30 no exemplo acima)
		self.master.update()
		self.master.after(100,self.goFilter)

	def goFilter(self):
		# 4. Filtering the image
		print('Filtering')
		self.master.after(100,self.processor.filter)
		self.var_barra.set(80) # k é um número entre 0 e o máximo 
						  # (definido como 30 no exemplo acima)
		self.master.update()
		self.master.after(100,self.goResize)

	def goResize(self):
		# 4. Resizing the image
		print('Resizing')
		self.master.after(100,self.processor.resize)
		self.var_barra.set(99) # k é um número entre 0 e o máximo 
						  # (definido como 30 no exemplo acima)
		self.master.update()
		self.master.after(100,self.goMapping)

	def goMapping(self):
		# 4. Resizing the image
		print('Color Mapping')
		self.master.after(100,self.processor.color_mapping)
		self.var_barra.set(100) # k é um número entre 0 e o máximo 
						  # (definido como 30 no exemplo acima)
		self.master.update()
		self.counter += 1
		self.master.after(100,self.next)
		
	def next(self):
		if self.counter < 4:
			# b. generating
			self.main_bg.destroy()
			self.main_bg = tkinter.Label(self.master, text = 'Select a '+self.side[self.counter]+' image\nto generate the '+self.side[self.counter]+' wear',\
				font = Font(family='Italic Helvetica', size=36, weight='bold'),\
				fg = 'black', bg = 'white', anchor = 'center', compound = 'center')
			self.main_bg.place(x=self.sw/2,y=self.sh/2-200,relwidth=1,relheight=1,anchor='center')

			self.image = filedialog.askopenfilename(initialdir = "./")
			m = re.search('skin_generator/(.+?)$', self.image)
			if m:
				self.image = m.group(1)
			else:
				exit(1)

			print('Image path:',self.image)

			self.wait_msg = tkinter.Label(self.master, text = 'Wait a moment, we are processing your cloth.',\
				font = Font(family='Italic Helvetica', size=18, weight='bold'),\
				fg = 'black', bg = 'white', anchor = 'center', compound = 'center')
			self.wait_msg.place(x=self.sw/2,y=self.sh/2,anchor='center')

			self.var_barra = tkinter.DoubleVar()
			self.minha_barra = ttk.Progressbar(self.master, variable=self.var_barra, maximum=100)
			self.minha_barra.place(x=self.sw/2,y=self.sh/2+200,anchor='center')
			self.master.after(100,self.goSegmentation)
		else:
			self.master.after(100,os.system("rm results/1-*"))
			self.master.after(100,os.system("rm results/2-*"))
			self.master.after(100,os.system("rm results/3-*"))
			self.master.after(100,os.system("rm results/4-*"))
			self.master.after(100,os.system("rm results/5-*"))
			self.master.after(100,os.system("rm results/6-*"))
			self.master.after(100,os.system("rm results/7-*"))
			exit(1)

	def destroyWidgets(self):
		self.start_button.destroy()