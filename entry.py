from Tkinter import *
import main, sqlite3 as sql

filename = "/home/stephen/inventory/~invdb.db"
def go(root=None):
	if hasattr(root,"destroy"):
		root.destroy()
	master = Tk()
	splash = Label(master,text = "Please scan your item, starting with location, and then part number, and the lot number.")
	splash.grid(row = 0, column = 0, padx = 3, pady = 3, columnspan = 2)
	loc_label = Label(master, text = "Location Code: ")
	loc_label.grid(row = 1, column = 0, padx = 5, pady = 3,)
	loc_box = Entry(master, highlightcolor = "yellow")
	loc_box.grid(row = 1, column = 1)
	pn_label = Label(master, text = "Part Number: ")
	pn_label.grid(row = 2, column = 0, padx = 5, pady = 3)
	pn_box = Entry(master, highlightcolor="yellow")
	pn_box.grid(row = 2, column = 1)
	ln_label = Label(master, text = "Lot Number: ")
	ln_label.grid(row = 3, column = 0, padx = 5, pady = 3)
	ln_box = Entry(master,highlightcolor = "yellow")
	ln_box.grid(row = 3, column = 1)
#	insert = lambda x=master:insertx(x) # for Debugging

	def insert(tk_wrap):
		loc = loc_box.get() 
		pn  = pn_box.get()
		ln  = ln_box.get()
		restart(tk_wrap)
		conn = sql.connect(filename)
		curs = conn.cursor()
		curs.execute("SELECT * FROM items WHERE lot_number=?", (ln,))
		if curs.fetchone() is None: 
			curs.execute("INSERT INTO items (lot_number,part_number,location) VALUES (?,?,?)",(ln,pn,loc))
		else:
			curs.execute("UPDATE items SET location=? WHERE lot_number=?", (loc,ln))

	insertcom = lambda tk_wrap = master:insert(tk_wrap)
	finish = Button(master,text = "Enter item", command = insertcom)
	finish.grid(row = 4, column = 1)
	loc_box.focus_set()
	master.mainloop()
def insertx(master): # for Debugging
	master.destroy()
	root = Tk()
	button_com = lambda x = root: restart(x)
	d_but = Button(root,text = "good",command = button_com)
	d_but.pack()
	root.mainloop()

def restart(root=None):
	if hasattr(root,"destroy"):
		root.destroy()
#	main.go()
	main.go()

