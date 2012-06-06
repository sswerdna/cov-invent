from Tkinter import *
import main, sqlite3 as sql

class query:
	def __init__(self,type_flag,calling_tk,filename="/home/stephen/inventory/~invdb.db"):
		calling_tk.destroy()
		self.conn = sql.connect(filename)
		self.curs = self.conn.cursor()
		self.root = Tk()
		self.type_flag = type_flag
		vartext = ["part numbers or numbers","lot number or numbers","location or locations"]
		self.splash_text = "Please enter the %s you would like to query." % vartext[type_flag]
		self.splash = Label(self.root,text = self.splash_text)
		self.splash.grid(row = 0,column = 0, padx = 3,pady = 3)
		self.request_box = Text(self.root)
		self.request_box.grid(row = 1, column = 0)
		self.qu = Button(self.root,text = "Query", command = self.get_requests)
		self.qu.grid(row = 2,column = 0)
		self.request_box.focus_set()
		self.root.mainloop()
		self.curs.execute("SELECT * from items where location='M-1'")
	def get_requests(self):
		raw_text = self.request_box.get(1.0,END)
		self.root.destroy()
		self.queries = raw_text.split()
		self.gen_queries()
	def gen_queries(self):
		self.data = []
		vartext = ["part_number","lot_number","location"]
		for query in self.queries:
			if query == '':
				continue
			if self.type_flag != 1:	
				data =()
				self.curs.execute("SELECT * FROM items WHERE %(column)s='%(target)s'" % {"column":vartext[self.type_flag], "target":query})
				while 1:
					data = self.curs.fetchone()
					if data is None:
						break
					else:
						self.data.append(data)
			else:
				data = ()
				self.curs.execute("SELECT * FROM items WHERE %(column)s=%(target)s" % {"column":vartext[self.type_flag], "target":query})
				while 1:
					data = self.curs.fetchone()
					if data is None:
						break
					else:
						self.data.append(data)
		self.gen_report()
	def gen_report(self):
		self.report = Tk()
		reset = lambda x=self.report: go_back(x)
		if len(self.data) == 0:
			Label(self.report, text = "No Results Found").pack()
			Button(self.report, text = "Return", command = reset).pack()
		else:
			Label(self.report, text = "Report"  ).grid(row = 0, column = 1, padx = 3, pady = 3)
			Label(self.report, text = "Part No.").grid(row = 1, column = 0, padx = 3, pady = 3)
			Label(self.report, text = "Lot No." ).grid(row = 1, column = 1, padx = 3, pady = 3)
			Label(self.report, text = "Location").grid(row = 1, column = 2, padx = 3, pady = 3)
		for x in self.data:
			datarow = self.data.index(x)+2
			Label(self.report, text = str(x[1])).grid(row = datarow, column = 0, padx = 3, pady = 3)
			Label(self.report, text = str(x[0])).grid(row = datarow, column = 1, padx = 3, pady = 3)
			Label(self.report, text = str(x[2])).grid(row = datarow, column = 2, padx = 3, pady = 3)
		exit = Button(self.report, text = "Return",command = reset)
		exit.grid(row = len(self.data) + 2, column = 2)

def go(root):
	root.destroy()
	master = Tk()
	part_no_query = lambda type_flag = 0: query(type_flag,calling_tk = master)
	lot_no_query =  lambda type_flag = 1: query(type_flag,calling_tk = master)
	loc_query =     lambda type_flag = 2: query(type_flag,calling_tk = master)
	splash = Label(master, text = "Please choose the type of query you wouldlike.")
	splash.grid(row = 0,column = 0,columnspan = 2)
	pnq = Button(master,text = "Query for a part number or numbers.",command = part_no_query)
	pnq.grid(row = 1,column = 0, padx = 3,pady = 3)
	lnq = Button(master, text = "Query for a lot number or numbers.",command = lot_no_query)
	lnq.grid(row = 2,column = 0,padx = 3,pady = 3)
	lq = Button(master, text = "Query the lots in a location or locations.",command = loc_query)
	lq.grid(row = 3,column = 0,pady = 3,padx = 3)
	reset = lambda x=master: go_back(x)
	return_button  = Button(master, text = "Return to home page",command = reset)
	return_button.grid(row = 4,column = 0,padx = 3, pady = 3)
	master.mainloop()

def go_back(master):
	master.destroy()
	main.go()
