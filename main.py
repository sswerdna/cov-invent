#!/usr/bin/env python
#This is an inventory management system based on the use of a sqlite3
#db on a shared drive, intended for use in the Covidien irvine Warehouse
#this is the entry point, main.py

from Tkinter import *
import entry, mass_entry,query, delete

def go():
	root = Tk()
	se = lambda x=root: entry.go(x)
	me = lambda x=root: mass_entry.go(x)
	qu = lambda x=root: query.go(x)
	de = lambda x=root: delete.go(x)
	splash = Label(root,text = "Hello, welcome to Inventory")
	splash.pack(padx = 3, pady = 3)
	single_entry = Button(root,text="Enter items individually", command = se)
	single_entry.pack(padx = 3, pady = 3)
	mass_enter = Button(root,text = "Enter a large number of items in the same place.",command = me)
	mass_enter.pack(padx = 3, pady = 3)
	querier = Button(root, text = "Query the database",command = qu)
	querier.pack(padx = 3, pady = 3)
	deleter = Button(root,text = "Delete an object from the database",command = de)
	deleter.pack(padx = 3, pady = 3)
	root.mainloop()

if __name__ == "__main__":
	go()
