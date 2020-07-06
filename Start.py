# Interface Imports
import tkinter
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

# Protocol, Plots and utils imports

class Start:

	def __init__(self, master, prev_sc, main_bg):
		# 1. Initilising GUI Components
		# a. screen and log components
		self.master = master
		self.main_bg = main_bg
		sw, sh = 800, 800

		# b. setting background
		self.set_bg('local/wallpaper_acnh.jpg')

		# c. creating start button
		self.start_button = self.create_button('START',self.start_button_click,250,330)

	def set_bg(self,path):
		from PIL import Image, ImageTk
		image = Image.open(path)
		img_copy = image.copy()

		bg_img = ImageTk.PhotoImage(image)
		sw, sh = 800, 800
		image = img_copy.resize((sw, sh), Image.ANTIALIAS)
		bg_img = ImageTk.PhotoImage(image)

		self.main_bg = tkinter.Label(self.master, image=bg_img, text = '\n\nWelcome to\nSKIN GENERATOR',\
			font = Font(family='Italic Helvetica', size=36, weight='bold', underline = True),\
			fg = 'white', anchor = 'center', compound = 'bottom')
		self.main_bg.image= bg_img
		self.main_bg.place(x=sw/2,y=sh/2,relwidth=1,relheight=1,anchor='center')

	def create_button(self,text,func,x,y):
		button = Button(self.master, text = text,\
			font = Font(family='Helvetica', size=36, weight='bold'),\
			fg = 'white', bg = "#%02x%02x%02x" % (30, 30, 30), \
			anchor = 'center', compound = 'center', 
			command = func,
			highlightthickness = 0, 
			bd = 0, padx=0, pady=0, height=2, width=13)
		button.place(x = x, y = y, anchor= 'center')
		return button

	def start_button_click(self):
		self.destroyWidgets()
		from Generator import Generator
		Generator(self.master,self,self.main_bg)

	def destroyWidgets(self):
		self.start_button.destroy()