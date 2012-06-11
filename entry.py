from Tkinter import *
import main, sqlite3 as sql

filename = "./.invdb.db"
class go:
	def __init__(self,root = None):
		#destroy the old window in a safe manner
		if hasattr(root,"destroy"):
			root.destroy()
 
		#generate splash Text
		self.master = Tk()
		splash = Label(self.master,text = "Please scan your item, starting with location, and then part number, and the lot number.")
		splash.grid(row = 0, column = 0, padx = 3, pady = 3, columnspan = 2)

		#create the labele and entry box for the location
		loc_label = Label(self.master, text = "Location Code: ")
		loc_label.grid(row = 1, column = 0, padx = 5, pady = 3,)
		self.loc_box = Entry(self.master, highlightcolor = "yellow")
		self.loc_box.grid(row = 1, column = 1)
	
		#create the label and entry box for the part number
		pn_label = Label(self.master, text = "Part Number: ")
		pn_label.grid(row = 2, column = 0, padx = 5, pady = 3)
		self.pn_box = Entry(self.master, highlightcolor="yellow", name = "pnbox")
		self.pn_box.grid(row = 2, column = 1)
		self.pn_box.bind("<FocusOut>",self.__handle_pn_unfocus)

		#create the label and entry box for the lot number
		ln_label = Label(self.master, text = "Lot Number: ")
		ln_label.grid(row = 3, column = 0, padx = 5, pady = 3)
		self.ln_box = Entry(self.master,highlightcolor = "yellow")
		self.ln_box.grid(row = 3, column = 1)
	
		#"" description
		desc_label = Label(self.master,text = "Description")
		desc_label.grid(row = 4, column = 0)
		self.desc_var = StringVar()
		self.desc_box = Entry(self.master,highlightcolor="yellow", textvariable = self.desc_var)
		self.desc_box.grid(row = 4, column = 1)

		#create the label and checkbox for overstock
		ov_label = Label(self.master, text = "Overstock?")
		ov_label.grid(row = 5,column = 0)
		self.ov_var = IntVar()
		self.ov_box = Checkbutton(self.master, var=self.ov_var)
		self.ov_box.grid(row = 5,column = 1)

		finish = Button(self.master,text = "Enter item", command = self.insert)
		finish.grid(row = 6, column = 1)
		self.loc_box.focus_set()
		self.master.mainloop()


	def insert(self):
		loc = self.loc_box.get()
		pn  = self.pn_box.get()
		ln  = self.ln_box.get()
		desc = self.desc_var.get()
		over = self.ov_var.get()
		conn = sql.connect(filename)
		curs = conn.cursor()
		curs.execute("SELECT * FROM items WHERE lot_number=?", (ln,))
		if curs.fetchone() is None: 
			curs.execute("INSERT INTO items (lot_number,part_number,location,description,overstock) VALUES (?,?,?,?,?)",(ln,pn,loc,desc,over))
		else:
			curs.execute("UPDATE items SET location=? WHERE lot_number=?", (loc,ln))

		conn.commit()
		conn.close()
		restart(self.master)

	# an event handler that autofills the description box if a
	# description already exists in the system.
	def __handle_pn_unfocus(self,event):
		pn = self.pn_box.get()
		conn = sql.connect(filename)
		curs = conn.cursor()
		curs.execute("SELECT description FROM items WHERE part_number=?",(pn,))
		data = curs.fetchone()
		if data is not None:
			if data[0] != "":
				self.desc_var.set(data[0])
				self.desc_box['state'] = 'disabled'
			else:
					return
		else:
			return

def restart(root=None):
	if hasattr(root,"destroy"):
		root.destroy()
	main.go()

