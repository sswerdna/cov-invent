from Tkinter import *
import sqlite3 as sql, main

filename = "./~invdb.db"
def go(root):	
	root.destroy()
	master = Tk()
	splash = Label(master,text = "Enter the lot number of the item you would like to delete.")
	splash.grid(row = 0, column = 0, columnspan = 2, padx = 3, pady = 3)
	del_label = Label(master,text = "Lot Number: ")
	del_label.grid(row = 1, column = 0, padx = 3, pady = 3)
	delbox = Entry(master)
	delbox.grid(row = 1, column = 1, padx = 3, pady = 3)
	def remove_item():
		conn = sql.connect(filename)
		curs = conn.cursor()
		curs.execute("DELETE FROM items WHERE lot_number=%s" % delbox.get())
		reset(master)
	del_button = Button(master, text = "Delete", command = remove_item)
	del_button.grid(row = 2, column = 1, padx = 3, pady = 3)
	master.mainloop()
def reset(master):
	master.destroy()
	main.go()
