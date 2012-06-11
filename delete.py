from Tkinter import *
import sqlite3 as sql, main

#should probably implement a delete function on the query box, for convenience, but this seems like an adequate stopgap for now
filename = "./.invdb.db"

def go(root=None):
	#same deal as all others, destroy previous shell in a safe manner
	if hasattr(root,"destroy"):	
		root.destroy()
	#generate a bunch of static elements. The three-deep nested scope is totes sweet,
	#but should probably be fixed.
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
		curs.execute("SELECT p_id FROM items WHERE lot_number=?",(delbox.get(),))
		data = curs.fetchone()

		if data is not None: #SAFETY!
			curs.execute("DELETE FROM items WHERE p_id=?" % (data[0],))
			reset(master)
		else:   #again with the nested scopes. obviously lambdas accept two arguments,
			#but i need to be sure both parts execute. perhaps xor will work for that.
			warn = Tk()
			Label(warn,text = "Record not found for that lot number").grid(row = 0, column = 0, columnspan = 2)

			def bcom(tk_wrap = warn, parent = master):
				tk_wrap.destroy()
				reset(parent)

			quit = Button(warn,text = "Continue",command = bcom)
			quit.grid(row = 1, column = 1)

			def acom(tk_wrap = warn,parent = master):
				tk_wrap.destroy()
				go(parent)
			try_again = Button(warn,text = "Try Again",command = acom)
			try_again.grid(row = 1,column = 0)

	del_button = Button(master, text = "Delete", command = remove_item)
	del_button.grid(row = 2, column = 1, padx = 3, pady = 3)
	master.mainloop()
#Go back to the start screen
def reset(master):
	master.destroy()
	main.go()
