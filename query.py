from Tkinter import *
import main, sqlite3 as sql,csv, tkMessageBox

class query:
	def __init__(self,type_flag,calling_tk=None,filename="./.invdb.db"):
		#safe removal of the previous window, to prevent clutter.
		if hasattr(calling_tk,"destroy"):
			calling_tk.destroy()
		# generate some classwide variables
		self.conn = sql.connect(filename)
		self.curs = self.conn.cursor()
		self.type_flag = type_flag
		#Create the shell of a GUI, with variable text for the splash
		self.root = Tk()
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
	def get_requests(self):
		# Grabs the text from the box and splits it by whitespace (not newlines, because the barcode scanner generates tabs)
		raw_text = self.request_box.get(1.0,END)
		self.root.destroy()
		self.queries = raw_text.split()
		self.gen_queries()
	def gen_queries(self):
		self.data = []#storage space for the list of results
		vartext = ["part_number","lot_number","location"]#this should probably be a global variable
		#Mild complexity ahead
		for query in self.queries:
			if query == '':#catch the accidental buggery from the split function catching weirdness
				continue
			if self.type_flag != 1:#subloop for the quoted variables, namely part number and location
				data =()
				self.curs.execute("SELECT * FROM items WHERE %(column)s='%(target)s'" % {"column":vartext[self.type_flag], "target":query})
				while 1:
					data = self.curs.fetchone()
					if data is None:# We hit the last one, terminate the loop
						break
					else:
						self.data.append(data) #jam some more data in
			else:# same thing again
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
		if len(self.data) == 0:#account for our lack of data, tell them we didn't find any results
			Label(self.report, text = "No Results Found").grid(row = 0, column = 0, columnspan = 2)
			Button(self.report, text = "Return", command = reset).grid(row = 1, column = 0, padx = 3)
			qcom = lambda tk_wrap = self.report: go(tk_wrap)
			Button(self.report, text = "Query Again", command = qcom).grid(row = 1, column = 1, padx = 3)
			self.report.mainloop()
		else: # generate static elements.
			Label(self.report, text = "Report"     ).grid(row = 0, column = 0, padx = 3, pady = 3, columnspan = 4)
			Label(self.report, text = "Part No."   ).grid(row = 1, column = 0, padx = 3, pady = 3)
			Label(self.report, text = "Lot No."    ).grid(row = 1, column = 1, padx = 3, pady = 3)
			Label(self.report, text = "Description").grid(row = 1, column = 2, padx = 3, pady = 3)
			Label(self.report, text = "Location"   ).grid(row = 1, column = 3, padx = 3, pady = 3)
		for x in self.data: # generate dynamic elements
			datarow = self.data.index(x)+2
			Label(self.report, text = str(x[2])).grid(row = datarow, column = 0, padx = 3, pady = 3)
			Label(self.report, text = str(x[1])).grid(row = datarow, column = 1, padx = 3, pady = 3)
			Label(self.report, text = str(x[4])).grid(row = datarow, column = 2, padx = 3, pady = 3)
			Label(self.report, text = str(x[3])).grid(row = datarow, column = 3, padx = 3, pady = 3)
		reporter = Button(self.report,text = "Generate Excel Report",command = self.create_csv)
		reporter.grid(row = len(self.data) + 2, column = 0)
		exit = Button(self.report, text = "Return",command = reset)
		exit.grid(row = len(self.data) + 2, column = 3)
	def create_csv(self):# relatively simple csv generation
		docwriter = csv.writer(open("export.csv",'w'))
		docwriter.writerow(["Part No.", "Lot No.", "Description", "Location"])
		for record in self.data:
			docwriter.writerow([record[2],record[1],record[4],record[3]])
		tkMessageBox.showinfo("File Location","The file is named export.csv, and is stored in the directory with your database")

def go(root=None):
	#safe destruction of the prior window, to prevent clutter in the window
	if hasattr(root,'destroy'):
		root.destroy()
	#all of this should most likely eventually be ported into the class
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
#returning to the main function
def go_back(master):
	if hasattr(master,"destroy"):
		master.destroy()
	main.go()
