from Tkinter import *
import main, sqlite3 as sql

filename = "./~invdb.db"
class go:
	def __init__(self,root=None,num_entries = 10):
		if hasattr(root,'destroy'):
			root.destroy()
		self.master = Tk()
		splash = Label(self.master, text = "Enter your location, then scan items, part number first, then lot number.")
		splash.grid(row = 0,column = 0, columnspan = 2)

		self.pns = []
		self.lns = []
		self.descs = []
		self.pn_boxes = []
		self.ln_boxes = []
		self.desc_boxes = []
		self.num_entries = 0
		self.generate_boxes()
		self.loc_label = Label(self.master, text = "Location: ")
		self.loc_label.grid(row = 1, column = 0, padx = 3, pady = 3)
		self.loc_box = Entry(self.master, highlightcolor = "yellow")
		self.loc_box.grid(row = 1, column = 1, padx = 3, pady = 3)
		self.loc_box.focus_set()

		Label(self.master, text = "Part Numbers").grid(row = 2, column = 0, padx = 3, pady = 3)
		Label(self.master, text = "Lot Numbers" ).grid(row = 2, column = 1, padx = 3, pady = 3)
		Label(self.master, text = "Description" ).grid(row = 2, column = 2, padx = 3, pady = 3)
		self.master.mainloop()

	def generate_boxes(self):
		for x in range(10):
			self.pn_boxes.append(Entry(self.master, highlightcolor = "yellow"))
			self.ln_boxes.append(Entry(self.master, highlightcolor = "yellow",))
			self.desc_boxes.append(Entry(self.master,highlightcolor = "yellow",takefocus=0))
			self.pn_boxes[self.num_entries].grid(row = self.num_entries + 3, column = 0)
			self.ln_boxes[self.num_entries].grid(row = self.num_entries + 3, column = 1)
			self.desc_boxes[self.num_entries].grid(row = self.num_entries + 3, column =2)

			self.pn_boxes[self.num_entries].bind("<FocusOut>",self.__uf_handler)
			self.num_entries += 1
		self.more_boxes = Button(self.master, text = "Add more lots", command = self.add_pls)
		self.log_button = Button(self.master, text = "Log lots",      command = self.log)
		self.more_boxes.grid(row = self.num_entries + 4, column = 0, padx = 3, pady = 3)
		self.log_button.grid(row = self.num_entries + 4, column = 1, padx = 3, pady = 3)
	def add_pls(self):
		self.more_boxes.destroy()
		self.log_button.destroy()
		for j in range(5):
			self.pn_boxes.append(Entry(self.master, highlightcolor = "yellow"))
			self.ln_boxes.append(Entry(self.master, highlightcolor="yellow"))
			self.desc_boxes.append(Entry(self.master,highlightcolor = "yellow",takefocus=0))
			self.pn_boxes[self.num_entries].grid(row = self.num_entries + 3,column = 0)
			self.ln_boxes[self.num_entries].grid(row = self.num_entries + 3,column = 1)
			self.desc_boxes[self.num_entries].grid(row = self.num_entries + 3, column =2)
			self.num_entries += 1
		self.more_boxes = Button(self.master,text = "Add more lots",command = self.add_pls)
		self.more_boxes.grid(row = self.num_entries + 4,column = 0,padx = 3,pady = 3)
		self.log_button = Button(self.master, text = "Log lots",command = self.log)
		self.log_button.grid(row = self.num_entries + 4, column = 1,padx = 3,pady = 3)
	def log(self):
		self.loc = self.loc_box.get()
		self.data = [(self.ln_boxes[x].get(),self.pn_boxes[x].get()) for x in range(self.num_entries) if self.ln_boxes[x].get() != "" and self.pn_boxes[x].get() != ""]
		#print self.data # for debugging
		conn = sql.connect(filename)
		curs = conn.cursor()
		for x in self.data:
			curs.execute("SELECT * FROM items WHERE lot_number=?",(x[0],))
			if curs.fetchone() is None:
				curs.execute("INSERT INTO items (lot_number,part_number,location) VALUES (?,?,?)",(x[0],x[1],self.loc))
			else:
				curs.execute("UPDATE items SET location=? WHERE lot_number=?",(self.loc,x[0]))
		conn.commit()
		conn.close()		
		self.master.destroy()
		main.go()
	def __uf_handler(self, event):
		index = self.pn_boxes.index(event.widget)
		print "Called on box",index
		conn = sql.connect(filename)
		curs = conn.cursor()
		curs.execute("SELECT description FROM items WHERE part_number=?",(self.pn_boxes[index].get(),))
		data = curs.fetchone()
		if data is not None:
			self.desc_boxes[index].insert(0,data[0])
			self.desc_boxes[index]['state']='disabled'
		else:
			pass
