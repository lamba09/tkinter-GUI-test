# ---------------------- HelloUser.py ----------------------
# 
# This program demonstrates how to build a user-friendly GUI
# around the Blt Graph. The user can select grid colors, 
# cross hairs colors and numerous other options just by 
# selecting it from a menu. The user can also read a graph 
# from file, and store it as a postscript file.
#

from Tkinter import *        # The Tk package
import tkFileDialog          # To be able to ask for files
import Pmw                   # The Python MegaWidget package
import math                  # import the sin-function
import string

# Make a customized Combobox (used in graphSetup)
def cBox(f, label, items):
    box = Pmw.ComboBox(f, label_text = label, 
          labelpos = 'w', scrolledlist_items = items)
                
    box.pack(fill = 'both', expand = 1, padx = 8, pady = 8)
    return box


# Make a dialog, and ask for a specified graph's color, linewidth etc.
# This function is called when the graph is double-clicked.
def graphSetup(args):
    global dialog, colBox, symBox, scoBox, solBox, smtBox, linBox
    
    el = g.element_closest(args.x, args.y, interpolate=1)
    elName = el["name"]
    
    if dialog == None: # Don't create the dialog each time - waste of cpu-cycles!
        dialog = Pmw.Dialog(master)
        dialog.configure(
           buttons = ('OK',),
           title = 'Edit graph',
           command = dialog.deactivate)
        
        dialog.withdraw()
        f = Frame(dialog.interior())
        f.pack()
        
        colBox = cBox(f, "Color:",
                      ('red', 'yellow', 'blue', 'green', 'black', 'grey'))
        symBox = cBox(f, 'Symbols:',
                      ("", "square", "circle", "diamond", "cross", "triangle"))
        scoBox = cBox(f, 'Symbol color:',
                      ('defcolor', 'red', 'yellow', 'blue', 'green', 'black', ''))
        solBox = cBox(f, 'Symbol outline:',
                      ('defcolor', 'red', 'yellow', 'blue', 'green', 'black'))
        smtBox = cBox(f, 'Smootheness:',
                      ('step', 'linear', 'quadratic', 'natural'))
        linBox = cBox(f, 'Line thickness:', (0, 1, 2, 3, 4, 5))
                    
                    
    # Retrieve the current setup for the graph...
    colBox.selectitem(g.element_cget(elName, "color"))
    symBox.selectitem(g.element_cget(elName, "symbol"))
    scoBox.selectitem(g.element_cget(elName, "fill"))
    solBox.selectitem(g.element_cget(elName, "outline"))
    smtBox.selectitem(g.element_cget(elName, "smooth"))
    linBox.selectitem(g.element_cget(elName, "linewidth"))
            
    # Let the user interact
    dialog.activate()
    
    # Update any changes
    g.element_configure(elName, color=colBox.get(), symbol=symBox.get(), 
                        smooth=smtBox.get(), linewidth=linBox.get(),
                        fill=scoBox.get(), outline=solBox.get())
                         

# shows a FileDialog, and opens the selected file. The file must be
# a text file with each line on the form: 
# <whitespace><number><whitespace><comma><whitespace><number><whitespace>\n

def openFile():
    global vector_x
    global vector_y
    
    fname = tkFileDialog.Open().show()
    if fname <> "":
        file = open(fname, 'r')
        i = len(vector_x)
        vector_x.append([])
        vector_y.append([])

                
        for line in file.readlines():
            [x, y] = string.split(line, ',')
            vector_x[i].append(float(x))
            vector_y[i].append(float(y))
            
        graphName = "Graph " +str(i+1)
        g.line_create(graphName, xdata=tuple(vector_x[i]), 
                       ydata=tuple(vector_y[i]), color="blue", scalesymbols=1)
            
        g.element_bind(graphName, sequence="<Double-Button-1>",
                       func=graphSetup)

# Empties the plotting window
def newFile():
    for name in g.element_names():
        g.element_delete(name)
           
# Saves the plot as postscript file 'HelloUser.ps'
def postscript():
    g.postscript_output(fileName='HelloUser.ps', decorations='no')

# The next functions configure the axes
def showAxis(): 
   state = int(g.axis_cget("x", 'hide'))
   g.axis_configure(["x", "y"], hide = not state)
    
def xlogScale():
   state = int(g.xaxis_cget('logscale'))
   g.xaxis_configure(logscale = not state)
    
def ylogScale():
   state = int(g.yaxis_cget('logscale'))
   g.yaxis_configure(logscale = not state)
    
def descending():
   state = int(g.axis_cget("x", 'descending'))
   g.axis_configure(["x", "y"], descending = not state)

# The next functions configures the Crosshairs
def mouseMove(event):
    g.crosshairs_configure(position="@" +str(event.x) +","+str(event.y))
    
def showCrosshairs():
   hide = not int(g.crosshairs_cget('hide'))
   g.crosshairs_configure(hide = hide, dashes="1")
   if(hide):
       g.unbind("<Motion>")
   else:
       g.bind("<Motion>", mouseMove)
       
    
def redCross():   g.crosshairs_configure(color = "red")
def blueCross():  g.crosshairs_configure(color = "blue")
def greenCross(): g.crosshairs_configure(color = "green")
def blackCross(): g.crosshairs_configure(color = "black")

# The next functions configures the Grid
def showGrid():
   g.grid_toggle()
    
def redGrid():   g.grid_configure(color = "red")
def blueGrid():  g.grid_configure(color = "blue")
def greenGrid(): g.grid_configure(color = "green")
def blackGrid(): g.grid_configure(color = "black")

# The next functions configures the Legend
def showLegend():
   state = int(g.legend_cget('hide'))
   g.legend_configure(hide = not state)
    
def raiseLegend():   g.legend_configure(relief="raised")
def flattenLegend(): g.legend_configure(relief="flat")
def sinkLegend():    g.legend_configure(relief="sunken")

# The next two functions are customized functions for making menus.
def myaddmenu(menuBar, owner, label, command):
    menuBar.addmenuitem(owner, 'command', '<help context>', 
                         label = label, command = command)

def mychkmenu(menuBar, owner, label, command):
    menuBar.addmenuitem(owner, 'checkbutton', '<help context>', 
            label = label, command = command, variable=IntVar())
    
vector_x = []
vector_y = []

master = Tk()                  # build Tk-environment
dialog = None

# Create and pack the MenuBar.        
menuBar = Pmw.MenuBar(master, hull_relief = 'raised', hull_borderwidth = 1)        
menuBar.pack(fill = 'x')

# Make the File menu
menuBar.addmenu('File', 'helptxt')
myaddmenu(menuBar, 'File', 'New', newFile)
myaddmenu(menuBar, 'File', 'Open...',    openFile)
myaddmenu(menuBar, 'File', 'Save as ps', postscript)
menuBar.addmenuitem('File', 'separator')
myaddmenu(menuBar, 'File', 'Quit',       master.quit)
   
# Make the Axis menu                
menuBar.addmenu('Axis', '')
mychkmenu(menuBar, 'Axis', 'hide',       showAxis  )
mychkmenu(menuBar, 'Axis', 'x logscale', xlogScale )
mychkmenu(menuBar, 'Axis', 'y logscale', ylogScale )
mychkmenu(menuBar, 'Axis', 'descending', descending)

# Make the Crosshairs menu
menuBar.addmenu('Crosshairs', '')
mychkmenu(menuBar, 'Crosshairs', 'show', showCrosshairs)
menuBar.addcascademenu('Crosshairs', 'Color', '')
myaddmenu(menuBar, 'Color', 'red',   redCross  )
myaddmenu(menuBar, 'Color', 'blue',  blueCross )
myaddmenu(menuBar, 'Color', 'green', greenCross)
myaddmenu(menuBar, 'Color', 'black', blackCross)

# Make the Grid menu
menuBar.addmenu('Grid', '')
mychkmenu(menuBar, 'Grid', 'show', showGrid)
menuBar.addcascademenu('Grid', 'Color ', '')
myaddmenu(menuBar, 'Color ', 'red',   redGrid  )
myaddmenu(menuBar, 'Color ', 'blue',  blueGrid )
myaddmenu(menuBar, 'Color ', 'green', greenGrid)
myaddmenu(menuBar, 'Color ', 'black', blackGrid)

# Make the Legend menu
menuBar.addmenu('Legend', '')
mychkmenu(menuBar, 'Legend', 'hide', showLegend)
menuBar.addcascademenu('Legend', 'Relief', '')
myaddmenu(menuBar, 'Relief', 'raised', raiseLegend   )
myaddmenu(menuBar, 'Relief', 'flat',   flattenLegend )
myaddmenu(menuBar, 'Relief', 'sunken', sinkLegend    )

# Make the graph area
g = Pmw.Blt.Graph(master)    
g.pack(expand=1, fill='both')
g.configure(title='Hello User!')     # enter a title

master.mainloop()                    # ...and wait for input



