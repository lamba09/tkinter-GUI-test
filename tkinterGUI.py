import Tkinter as tk
import tkFileDialog
import tkMessageBox


def print_something():
	print "something."

def print_nothing(event):
	print "nothing."

def doNothing():
	tkMessageBox.showinfo("Important","nothing..")

def open_file():
	file = tkFileDialog.askopenfile()
	print file.readlines()

def choose_directory():
	dirname = tkFileDialog.askdirectory()
	print dirname

def updatetext(event):
	status_string.set(e.get())
	master_frame.update_idletasks()

def askquit():
	answer = tkMessageBox.askyesno("Quit?", "Are you sure to quit?")
	if answer:
		master_frame.quit()

class TwoButtons():

	def __init__(self, master): # takes the object itself and the master frame in which it should be placed
		frame = tk.Frame(master)
		frame.pack()

		self.printButton = tk.Button(frame, text="Print", command=self.printMessage)
		self.printButton.pack(side=tk.LEFT)

		self.quitButton = tk.Button(frame, text="Exit", command=askquit)
		self.quitButton.pack(side=tk.LEFT)

	def printMessage(self):
		print "Entered Username: ", user_name.get()
		print "Entered Password: ", user_password.get()
		status_string.set(user_name.get())
		master_frame.update_idletasks()
		if check_log.get() == 1:
			print "I'd like to stay logged in.."



# Creating master tkinter window (root-window):
master_frame = tk.Tk()

# ----- Menu -----

master_frame.option_add('*tearOff', False) # dropdown wont begin with an additional line (linux / win)

menu = tk.Menu(master_frame) # create menu object from master_frame (root-frame)
master_frame.config(menu=menu) # assign menu as menu

file_menu = tk.Menu(menu,tearoff=0) # create menu inside menu (dropdown File-Menu)
edit_menu = tk.Menu(menu)

menu.add_cascade(label="File", menu=file_menu) # define dropdown (cascade) inside file_menu
menu.add_cascade(label="Edit", menu=edit_menu)

file_menu.add_command(label="New Project...",command=doNothing) # adding all items inside cascade
file_menu.add_command(label="New...", command=choose_directory)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_separator() # draw horitontal line as separator
file_menu.add_command(label="Quit", command=master_frame.quit)

edit_menu.add_command(label="Edit", command=doNothing)
edit_menu.add_command(label="Redo", command=doNothing)

# ----- Frame definitions -----
toolbar = tk.Frame(master_frame)
top_frame = tk.Frame(master_frame,width=500, height=50) # create Frame object
top_frame.pack_propagate(0) # prevent the frame from adjusting its size to the content's size by packing stuff in
middle_frame = tk.Frame(master_frame,bg="floral white", width=500, height=100) # bg:background color
middle_frame.pack_propagate(0)
bottom_frame = tk.Frame(master_frame,bg="mint cream",width=500, height=200)
bottom_frame.pack_propagate(0)
bottom_frame.grid_propagate(0)
lowest_frame = tk.Frame(master_frame,width=500, height=100, relief="sunken",borderwidth=5)

toolbar.pack(side=tk.TOP,fill=tk.X)
top_frame.pack(side=tk.TOP) # pack everything inside master_frame
middle_frame.pack(side=tk.TOP)
bottom_frame.pack(side=tk.TOP)
lowest_frame.pack(side=tk.TOP)

# ----- Toolbar -----
insert_photo_icon = tk.PhotoImage(file="icons/cameraplus32.gif")
print_icon = tk.PhotoImage(file="icons/printer32.gif")

insert_button = tk.Button(toolbar,image=insert_photo_icon, command=doNothing)
print_button = tk.Button(toolbar, image=print_icon, command=doNothing)
insert_button.pack(side=tk.LEFT, padx=2, pady=2)
print_button.pack(side=tk.LEFT, padx=2, pady=2)

# ----- Buttons and Labels -----

start_button = tk.Button(bottom_frame,text="Start",fg="blue", command=print_something)
nothing_button = tk.Button(bottom_frame,text="Nothing")
nothing_button.bind("<Button-1>",print_nothing) # bind event "leftklick" of button to function print_nothing

label1 = tk.Label(top_frame, text="red text, yellow bkg",fg="red",bg="yellow") # fg:foreground color (text color)
label2 = tk.Label(middle_frame, text="fill Y",fg="white",bg="blue")

user_name = tk.StringVar()
user_password = tk.StringVar()

label_name = tk.Label(bottom_frame, text="Name:")
label_password = tk.Label(bottom_frame, text="Password:")
name_entry = tk.Entry(bottom_frame, textvariable=user_name) # entry field to enter text (here: name)
password_entry = tk.Entry(bottom_frame, textvariable=user_password) # assign entered text to user_password

check_log = tk.IntVar()
check_box = tk.Checkbutton(bottom_frame,text="keep me logged in",variable=check_log) # checkbox with text

label1.pack(fill=tk.X)
label2.pack(side=tk.LEFT, fill=tk.Y)

label_name.grid(row=0, sticky=tk.E) # grid: pack label_name inside a grid on position row=0, column = 0 (auto)
label_password.grid(row=1, sticky=tk.E) # sticky: alignement of text to East (E), row = 1, column = 0 (auto)
name_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

check_box.grid(row=2, columnspan=2) # checkbox over two columns inside grid with columnspan = 2
start_button.grid(row=3,column=0)
nothing_button.grid(row=3, column=1)
two_buttons = TwoButtons(lowest_frame) # adding the two buttons from class inside lowest frame

# ----- Statusbar -----

status_string = tk.StringVar()
status_string.set("Prepairing to do nothing...")

status = tk.Label(master_frame,textvariable=status_string, bd=1, relief="sunken", anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)

e = tk.Entry(master_frame)
e.pack()
e.bind(sequence='<KeyRelease>', func=updatetext)




master_frame.mainloop()
