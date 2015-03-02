import Tkinter as tk
import tkFileDialog
import tkMessageBox


class GUI(object):
    def __init__(self):

        self.UserData = {
            'Username':'',
            'Password':'',
            'KeepSignedIn':'99',
            'UserAttributes':{
                'IsOnline' : False,
                'PremiumUser': False,
                'PagerNumber': ''
            }
        }
        self.StatusVariables = {
            'UserLoggedIn':False,
            'Whatever':'mega'

        }

        if self.UserData['UserAttributes'].has_key('mega'):
            pass

        # Creating master tkinter window (root-window):
        self.master_frame = tk.Tk()
        self.master_frame.wm_title("Title")

        self.menubar = GUI_Menubar(self)
        self.toolbar = GUI_Toolbar(self)
        self.content = GUI_Content(self)

        self.statusbar = GUI_Statusbar(self)

        self.master_frame.mainloop()

    def UpdateStatus(self, status=""):
        self.statusbar.status_string.set(status)
        self.master_frame.update_idletasks()

    def EventUpdateStatus(self, event):
        self.statusbar.status_string.set(self.statusbar.e.get())
        self.master_frame.update_idletasks()

    def UserIsLoggedIn(self):
        if self.UserData['UserAttributes']['IsOnline']:
            print "User is online"
        else:
            print "User is offline"

    def Quit(self):
        answer = tkMessageBox.askyesno("Quit", "Are you sure to quit?")
        if answer:
            self.master_frame.quit()


class GUI_Menubar(tk.Menu):
    def __init__(self, gui, cnf={}, **kw):
        tk.Menu.__init__(self, gui.master_frame, cnf={}, **kw)

        gui.master_frame.option_add('*tearOff', False)  # dropdown wont begin with an additional line (linux / win)

        gui.master_frame.config(menu=self)  # assign menu as menu

        self.file_menu = tk.Menu(self, tearoff=0)  # create menu inside menu (dropdown File-Menu)
        self.edit_menu = tk.Menu(self)

        self.add_cascade(label="File", menu=self.file_menu)  # define dropdown (cascade) inside file_menu
        self.add_cascade(label="Edit", menu=self.edit_menu)

        self.file_menu.add_command(label="New Project...", command=doNothing)  # adding all items inside cascade
        self.file_menu.add_command(label="New...", command=choose_directory)
        self.file_menu.add_command(label="Open...", command=open_file)
        self.file_menu.add_separator()  # draw horitontal line as separator
        self.file_menu.add_command(label="Quit", command=gui.Quit)

        self.edit_menu.add_command(label="Edit", command=doNothing)
        self.edit_menu.add_command(label="Redo", command=doNothing)


class GUI_Toolbar(tk.Frame):
    def __init__(self, gui, cnf={}, **kw):
        tk.Frame.__init__(self, master=gui.master_frame, cnf={}, **kw)

        self.mastergui = gui
        self.pack(side=tk.TOP, fill=tk.X)

        self.insert_photo_icon = tk.PhotoImage(file="icons/cameraplus32.gif")
        self.print_icon = tk.PhotoImage(file="icons/printer32.gif")

        self.insert_button = tk.Button(self, image=self.insert_photo_icon, command=doNothing)
        self.print_button = tk.Button(self, image=self.print_icon, command=self.Print_Pressed)
        self.insert_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.print_button.pack(side=tk.LEFT, padx=2, pady=2)

    def Print_Pressed(self):
        self.mastergui.UpdateStatus("Print pressed..")

class GUI_Content(tk.Frame):
    def __init__(self, gui, cnf={}, **kw):
        tk.Frame.__init__(self, gui.master_frame, cnf={}, **kw)
        self.ContentData = {
            'asdf':'d',

        }
        self.pack(side=tk.TOP)

        # --- Frames ---
        top_frame = tk.Frame(self, width=500, height=50)  # create Frame object
        top_frame.pack_propagate(0)  # prevent the frame from adjusting its size to the content's size by packing stuff in
        middle_frame = tk.Frame(self, bg="floral white", width=500, height=100)  # bg:background color
        middle_frame.pack_propagate(0)
        bottom_frame = tk.Frame(self, bg="mint cream", width=500, height=200)
        bottom_frame.pack_propagate(0)
        bottom_frame.grid_propagate(0)
        lowest_frame = tk.Frame(self, width=500, height=100, relief="sunken", borderwidth=5)

        top_frame.pack(side=tk.TOP)  # pack everything inside master_frame
        middle_frame.pack(side=tk.TOP)
        bottom_frame.pack(side=tk.TOP)
        lowest_frame.pack(side=tk.TOP)

        # --- Frame content ---
        start_button = tk.Button(bottom_frame, text="Start", fg="blue", command=print_something)
        nothing_button = tk.Button(bottom_frame, text="Nothing")
        nothing_button.bind("<Button-1>", print_nothing)  # bind event "leftklick" of button to function print_nothing

        label1 = tk.Label(top_frame, text="red text, yellow bkg", fg="red", bg="yellow")  # fg:foreground color (text color)
        label2 = tk.Label(middle_frame, text="fill Y", fg="white", bg="blue")


        label1.pack(fill=tk.X)
        label2.pack(side=tk.LEFT, fill=tk.Y)

        GUI_Login(gui,bottom_frame)

        start_button.grid(row=4, column=0)
        nothing_button.grid(row=4, column=1)

        TwoButtons(gui,lowest_frame)


class GUI_Login(object):
    def __init__(self, gui, parent=None):

        self.MasterGUI = gui
        if parent==None:
            parent = self.MasterGUI.master_frame

        self.usr_name = tk.StringVar()
        self.usr_pw = tk.StringVar()
        self.usr_checkbox = tk.IntVar()

        self.label_name = tk.Label(parent, text="Name:")
        self.label_password = tk.Label(parent, text="Password:")

        self.name_entry = tk.Entry(parent, textvariable=self.usr_name)  # entry field to enter text (here: name)
        self.password_entry = tk.Entry(parent, textvariable=self.usr_pw)  # assign entered text to password
        self.check_box = tk.Checkbutton(parent, text="keep me logged in", variable=self.usr_checkbox)  # checkbox with text
        self.apply_button = tk.Button(parent,text="Apply",command=self.ApplyLogin)

        self.label_name.grid(row=0, sticky=tk.E)  # grid: pack label_name inside a grid on position row=0, column = 0 (auto)
        self.label_password.grid(row=1, sticky=tk.E)  # sticky: alignement of text to East (E), row = 1, column = 0 (auto)
        self.name_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.check_box.grid(row=2, columnspan=2)  # checkbox over two columns inside grid with columnspan = 2
        self.apply_button.grid(row=3, columnspan=2)

    def ApplyLogin(self):
        self.MasterGUI.UserData['Username'] = self.usr_name.get()
        self.MasterGUI.UserData['Password'] = self.usr_pw.get()
        self.MasterGUI.UserData['KeepSignedIn'] = self.usr_checkbox.get()
        self.MasterGUI.UpdateStatus("Logging in..")


class GUI_Statusbar(object):
    def __init__(self, gui):

        self.MasterGUI = gui

        self.status_string = tk.StringVar()
        self.status_string.set("Status OK")
        self.MasterGUI.StatusString = self.status_string

        self.status = tk.Label(gui.master_frame, textvariable=self.MasterGUI.StatusString, bd=1, relief="sunken", anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.e = tk.Entry(gui.master_frame)
        self.e.pack()
        self.e.bind(sequence='<KeyRelease>', func=gui.EventUpdateStatus)


class TwoButtons(object):
    def __init__(self, gui, parent=None):  # takes the object itself and the master frame in which it should be placed

        self.MasterGUI = gui

        if parent == None:
            parent = gui.master_frame
        frame = tk.Frame(parent)
        frame.pack()

        self.printButton = tk.Button(frame, text="Print", command=self.printMessage)
        self.printButton.pack(side=tk.LEFT)

        self.quitButton = tk.Button(frame, text="Exit", command=gui.Quit)
        self.quitButton.pack(side=tk.LEFT)

    def printMessage(self):
        print "Entered Username: ", self.MasterGUI.UserData['Username']
        print "Entered Password: ", self.MasterGUI.UserData['Password']
        self.MasterGUI.UpdateStatus(self.MasterGUI.UserData['Username'])

        if self.MasterGUI.UserData['KeepSignedIn'] == 1:
            print "I'd like to stay logged in.."


def print_something():
    print "something."


def print_nothing(event):
    print "nothing."


def doNothing():
    tkMessageBox.showinfo("Important", "nothing..")


def open_file():
    file = tkFileDialog.askopenfile()
    print file.readlines()


def choose_directory():
    dirname = tkFileDialog.askdirectory()
    print dirname



MyGUI = GUI()

print MyGUI.UserData['Username']


