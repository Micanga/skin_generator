# tkinter Imports
import tkinter
from tkinter import *

import os
import sys

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

# Main
if __name__ == "__main__":
	# 1. Starting root
	root = tkinter.Tk()

	# 2. Setting the commom features
	# a. window settings
	root.title('Skin Generator')
	root.resizable(width = False,height = False)
	root.configure(background='white')
	#root.iconbitmap('@logo.xmb')

	# b. setting full
	sw, sh = 800, 800
	wc, hc = 0, 0
	pad = 0

	root.geometry('%dx%d+%d+%d' % (sw-pad,sh-pad,wc,hc))
	root.focus_set()  # <-- move focus to this widget
	root.bind("<Escape>", lambda e: root.quit())

	# c. grid settings
	root.grid_rowconfigure(0,pad=0)
	root.grid_columnconfigure(0,pad=0)
	root.grid_rowconfigure(1,pad=0)
	root.grid_columnconfigure(1,pad=0)
	main_bg = None

	# 4. Starting app
	from Start import Start
	Start(root,None,None)
	root.mainloop()

	# 5. That's all folks :) ... 