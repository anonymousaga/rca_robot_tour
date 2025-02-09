#!/usr/bin/env python3
import turtle as t
from random import randint
import time
import tkinter as tk
import _thread 
#_thread.start_new_thread(th_func, ())
import json
import os
import sys
#try:
#    from compileFile import *
#except:
#    def compileCommands(commandvar):
#        try:
#            return eval(commandvar), False
#        except Exception as e:
#            return [], e
from tkinter import font, ttk
from tkinter import *
import webbrowser
from tkinter import filedialog
from tkinter import filedialog

try:
    import pyperclip
    pyperclip_enable=True
except ImportError:
    pyperclip_enable=False
    print("Pyperclip not installed, copy to clipboard disabled")



if getattr(sys, 'frozen', False):
    __location__  = os.path.dirname(sys.executable)
    if not os.path.isfile(os.path.join(__location__,"pyproject.toml")):
        # The application is not frozen
        # Change this bit to match where you store your data files:
        __location__  = os.path.join(os.path.dirname(sys.executable),'../Resources')
        #print(__location__)
    if sys.platform == 'win32':
        config_dir = os.path.join(os.getenv('APPDATA'), 'Robot Coaching Assistant')
    elif sys.platform == 'darwin':
        config_dir = os.path.expanduser('~/Library/Application Support/Robot Coaching Assistant')
    else:  # Linux and other Unix-like
        config_dir = os.path.expanduser('~/.config/robot_coaching_assistant')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    __location2__ = config_dir
else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    __location__  = os.path.dirname(__file__)
    __location2__=__location__

commands=[]
root=tk.Tk()
#scale is pixel = cm 

try:
    with open(os.path.join(__location2__,"config.json"), "r") as f:
        vars = json.load(f)
except FileNotFoundError:
    vars = {"grid_x": 5, "grid_y": 4, "lineSpeed": 6, "cm_offset": 0}
    with open(os.path.join(__location2__,"config.json"), "w") as f:
        json.dump(vars, f)

try:
    import toml
    # Read the pyproject.toml file
    with open(os.path.join(__location__,"pyproject.toml"), "r") as f:
        version = toml.load(f)["project"]["version"]
except ImportError:
    version = "?"
    print("TOML not installed, version number disabled")



class UndoableEntry(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Control-z>", self.undo)
        self.bind("<Command-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Command-Z>", self.redo) #command-shift-z
        self.bind("<Key>", self.on_key_press)

        self.undo_stack = []
        self.redo_stack = []

    def undo(self, event=None):
        if self.undo_stack:
            text = self.undo_stack.pop()
            self.redo_stack.append(self.get("1.0", "end"))
            self.delete("1.0", "end")
            self.insert("1.0", text)

    def redo(self, event=None):
        if self.redo_stack:
            text = self.redo_stack.pop()
            self.undo_stack.append(self.get("1.0", "end"))
            self.delete("1.0", "end")
            self.insert("1.0", text)
    def on_key_press(self, event):
        if event.keysym not in ["Control_L", "Control_R", "Meta_L", "Meta_R","z", "y"]:
            self.undo_stack.append(self.get("1.0", "end"))
            self.redo_stack.clear()



def read_commandstk():
    global commands
    global root
    commands=text_box.get('1.0','end')
    commands, error = compileCommands(commands)
    if error == False:
        big_red_label.config(text="")
        try:
            tupdate()
        except:
            pass
    else:
        big_red_label.config(text="Syntax Error in Commands!")






#Here I save the x and y position of the window to a file "root.conf"
#Here I see if the file exists.
if os.path.isfile(os.path.join(__location__,"root.conf")): 
    #Here I read the X and Y positon of the window from when I last closed it.
    with open(os.path.join(__location__,"root.conf"), "r") as conf: 
        root.geometry(conf.read())
else:
    #Default window position.
    root.geometry('800x800+0+0')






# setting the windows size

Grid.columnconfigure(root,0, weight=1)
Grid.rowconfigure(root,1, weight=1)
# declaring string variable
# for storing name and password



def modified_flag_changed(event=None):
    if text_box.edit_modified():
        read_commandstk()
        text_box.edit_modified(False)

        


text_box = UndoableEntry(root)
text_box.bind("<<Modified>>", modified_flag_changed)

default_code = '''
def compileCommands(commandvar):
    commandvar = commandvar.strip().splitlines()
    command2 = []
    try:
        for x in commandvar:
            if x=="u":
                command2.append((1,180))
            elif x=="-u":
                command2.append((1,-180))
            elif x=="l":
                command2.append((1,-90))
            elif x=="r":
                command2.append((1,90))
            elif x=="rd":
                command2.append((1,45))
            elif x=="ld":
                command2.append((1,-45))
            elif x.startswith("sd"):
                command2.append((0,float(x.strip("sd"))*1.414))
            elif x.startswith("s"):
                command2.append((0,float(x.strip("s"))))
            elif x.startswith("t"):
                command2.append((1,float(x.strip("t"))))
            elif x.strip()=="":
                pass # skip blank lines
            else:
                raise ValueError('command is incorrect')
        return command2, False
    except ValueError as e:
        return [], e
'''

try:
    with open(os.path.join(__location2__,"compileFile.py"), "r") as f:
        exec(f.read())
except FileNotFoundError:
    with open(os.path.join(__location2__,"compileFile.py"), "w") as f:
        f.write(default_code)
    exec(default_code)

lineWidth=2.5

bottomFrame=tk.Frame(root)
screensSizeMultiplier=1

root.minsize(500,600)

def open_docs_link(event=None):
    webbrowser.open("https://github.com/anonymousaga/rca_robot_tour/blob/main/README.md")

preferences_window=None
about_window=None
about_is_open = False

class BoldLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        bold_font = font.Font(self, self.cget("font"))
        bold_font.configure(weight="bold")
        self.configure(font=bold_font)

def open_about():
    global about_is_open
    global about_window
    
    if about_is_open is False:
        about_is_open = True
        about_window = tk.Toplevel(root)
        #about_window.title("About RCA")
        about_window.geometry("280x170")
        about_window.resizable(False, False) # make False, False to enable pop-out window on macOS
        about_window.title("")
        img = PhotoImage(file=(os.path.join(__location__,"icon.png")))
        img = img.subsample(13) #mechanically, here it is adjusted to 32 instead of 320
        panel = tk.Label(about_window, image = img)
        panel.pack(side='top', pady=3)
        label2=BoldLabel(about_window, text="Robot Coaching Assistant")

        label2.pack(side='top',pady=6)

        version_label = ttk.Label(about_window, text=f"Version: {version}")
        version_label.configure(font=("TkDefaultFont", 11))
        version_label.pack(side='top')
        fram2=tk.Frame(about_window)


        label1 = ttk.Label(fram2, text="Developed by")
        label1.configure(font=("TkDefaultFont", 11))
        label1.pack(side='left')

        label2 = ttk.Label(fram2, text="anonymousaga", foreground="#0099FF")
        label2.configure(font=("TkDefaultFont", 11))
        label2.pack(side='left')
        label2.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/anonymousaga"))

        label3 = ttk.Label(fram2, text="with ❤️")
        label3.configure(font=("TkDefaultFont", 11))
        label3.pack(side='left')
        fram2.pack(side='top')

        def _quitprefs():
            about_window.quit()
            about_window.destroy()
        about_window.protocol("WM_DELETE_WINDOW", _quitprefs)
        about_window.mainloop()
        about_is_open = False
    else:
        about_window.focus_force()

def tupdate(event=None):
    global showRobotMoving
    global screensSizeMultiplier
    writeROW=-1
    writeCOL=-1
    screen = t.Screen()
    #screen._root.lift()  # Bring window to front
    xe=t.window_width()
    ye=t.window_height()
    t.width(1*screensSizeMultiplier)
    if xe/ye > vars['grid_x']/vars['grid_y']:
        screensSizeMultiplier = (ye/(50*vars['grid_y'])) * 0.825
    else:
        screensSizeMultiplier = (xe/(50*vars['grid_x'])) * 0.75
    
    t.reset()
    
    t.speed("fastest")
    t.tracer(0,0)
    screen.delay(0)


    # Draw a grid with 4 rows and 5 columns
    for row in range(1,vars['grid_y']+1):
        for col in range(vars['grid_x']):
            # Calculate the x and y coordinates for each cell
            x = col * 50 *screensSizeMultiplier
            y = row * 50 *screensSizeMultiplier
            
            # Move the turtle to the starting position of the cell
            t.pencolor(pencolor)
            t.up()
            t.goto((x-(vars['grid_x']*25)*screensSizeMultiplier), (y-(vars['grid_y']*25)*screensSizeMultiplier))
            t.down()
            
            for index,zone in enumerate(gatezones):
                if row==zone[0] and col==zone[1]:
                    # set the fillcolor 
                    t.fillcolor(highlightcolorGate) 
                    # start the filling color 
                    t.begin_fill()
                    if index == len(gatezones)-1:
                        writeROW=row
                        writeCOL=col

            # Draw the cell
            for i in range(4):
                if ((i == 2 and row > 1) or (i == 3 and col>0)) and highlightOn == True:
                    t.forward(10*screensSizeMultiplier)
                    t.pencolor(highlightcolor)
                    t.width(7*screensSizeMultiplier)
                    t.forward(30*screensSizeMultiplier)
                    t.width(1*screensSizeMultiplier)
                    t.pencolor(pencolor)
                    t.forward(10*screensSizeMultiplier)
                elif ((i == 2 and row == 1) or (i == 3 and col == 0) or (i == 1 and col == (vars['grid_x']-1)) or (i == 0 and row == vars['grid_y'])) and highlightOn == True:
                    t.forward(25*screensSizeMultiplier)
                    t.pencolor(highlightcolorStart)
                    t.dot(10*screensSizeMultiplier)
                    t.pencolor(pencolor)
                    t.forward(25*screensSizeMultiplier)
                else:
                    t.pencolor(pencolor)
                    if gateSelect == True:
                        t.width(4*screensSizeMultiplier)
                        t.pencolor("#A9C503")
                    else:
                        t.width(1*screensSizeMultiplier)
                    t.forward(50*screensSizeMultiplier)
                t.right(90)
            t.end_fill()

            enddottrue=(enddotx == col and enddoty == row)
            if highlightOn == True or enddottrue: # draw the end points
                t.up()
                t.forward(25*screensSizeMultiplier)
                t.right(90)
                t.forward(25*screensSizeMultiplier)
                t.setheading(0)
                if enddottrue==True:
                    t.pencolor('red')
                else:
                    t.pencolor(highlightcolorDot)
                t.dot(8*screensSizeMultiplier)
                

    t.up()
    t.goto(((((50*writeCOL)+25)*screensSizeMultiplier)-(vars['grid_x']*25)*screensSizeMultiplier), ((50*writeROW*screensSizeMultiplier)-(vars['grid_y']*25)*screensSizeMultiplier))
    t.right(90)
    t.forward(17*screensSizeMultiplier)
    t.down()
    if writeCOL != -1:
        t.pencolor(pencolor)
        t.write("LAST", align="center", font=("Arial", int(8*screensSizeMultiplier), "normal"))
    t.up()
    t.right(180)
    t.forward(17*screensSizeMultiplier)
    t.left(90)
    t.forward(25*screensSizeMultiplier)
    t.setheading(0)
    for barrier in barrierList:
        t.up()
        if barrier[0] == 0: # column
            t.setheading(0)  # Reset heading to face east
            t.goto((((barrier[1]-1)*50*screensSizeMultiplier)-(vars['grid_x']*25)*screensSizeMultiplier), (((barrier[2])*50*screensSizeMultiplier)-(vars['grid_y']*25)*screensSizeMultiplier))
            t.forward(50*screensSizeMultiplier)
            t.right(90)
            t.forward(10*screensSizeMultiplier)
            t.pencolor(barrierColor)
            t.width(7*screensSizeMultiplier)
            t.down()
            t.forward(30*screensSizeMultiplier)
            t.up()
            t.width(1*screensSizeMultiplier)
            t.pencolor(pencolor)
            t.forward(10*screensSizeMultiplier)
        else: # row
            t.setheading(0)  # Reset heading to face east
            t.goto((((barrier[1])*50*screensSizeMultiplier)-(vars['grid_x']*25)*screensSizeMultiplier), (((barrier[2]-1)*50*screensSizeMultiplier)-(vars['grid_y']*25)*screensSizeMultiplier))
            t.forward(10*screensSizeMultiplier)
            t.pencolor(barrierColor)
            t.width(7*screensSizeMultiplier)
            t.down()
            t.forward(30*screensSizeMultiplier)
            t.up()
            t.width(1*screensSizeMultiplier)
            t.pencolor(pencolor)
            t.forward(10*screensSizeMultiplier)
    t.setheading(0)  # Reset heading to face east
    

    
    movetodot(xvar,yvar)
    t.width(lineWidth*screensSizeMultiplier)
    t.pencolor('green')
    t.dot(lineWidth*2.5*screensSizeMultiplier)
    size = t.turtlesize()
    increase = (screensSizeMultiplier*.6 * num for num in size)
    t.turtlesize(*increase)
    t.shape('arrow')
    if showRobotMoving == True:
        t.tracer(1, 0)
        t.delay(25)
        t.speed(vars['lineSpeed'])
    t.down()
    


    for index, command in enumerate(commands):
        t.pencolor(colorPallete[index % len(colorPallete)][0], colorPallete[index % len(colorPallete)][1], colorPallete[index % len(colorPallete)][2])
        #t.pencolor(randint(0,90)/120,randint(0,90)/120,randint(0,90)/120)
        if command[0] == 0: #straight moves
            t.forward(command[1]*screensSizeMultiplier)
        elif command[0] == 1: #turn moves
            if command[1] < 0:
                t.left(command[1]*-1)
            else:
                t.right(command[1])

    t.color('red')
    t.up()
    t.speed("fastest")
    t.tracer(0,0)
    screen.delay(0)
    t.update()
    showRobotMoving = False   


def selectStart(y1,x1):
    global xvar, yvar
    xvar = x1
    yvar = y1
    tupdate()

def open_preferences():
    global vars
    global preferences_is_open
    global preferences_window
    
    if preferences_is_open is False:
        preferences_is_open = True
        preferences_window = tk.Toplevel(root)
        preferences_window.title("Preferences")
        preferences_window.minsize(600,420)
        preferences_window.geometry('780x580')
        preferences_window.resizable(True, True) # make False, False to enable pop-out window on macOS

        preferences_scrollbar = ttk.Scrollbar(preferences_window)
        preferences_scrollbar.pack(side="right", fill="y")

        preferences_canvas = tk.Canvas(preferences_window, yscrollcommand=preferences_scrollbar.set)
        preferences_canvas.pack(side="left", fill="both", expand=True)
        

        
        preferences_scrollbar.config(command=preferences_canvas.yview)

        preferences_frame = ttk.Frame(preferences_canvas)
        preferences_canvas.create_window((0, 0), window=preferences_frame, anchor="nw")

        preferences_frame.bind("<Configure>", lambda e: preferences_canvas.configure(scrollregion=preferences_canvas.bbox("all")))

        version_label = ttk.Label(preferences_frame, text=f"  Version: {version}")
        #version_label.configure(font=("TkDefaultFont", 10))
        version_label.grid(row=0, column=2, sticky='w')

        def modified_flag_changed_prefs(event=None):
            if variable_entry.edit_modified():
                variable_entry.configure(height=len(variable_entry.get("1.0", "end").splitlines()))
                variable_entry.edit_modified(False)

        preferences_window.configure(padx=5, pady=5)
        Grid.columnconfigure(preferences_frame,3, weight=1)


    


        github_link_button = ttk.Button(preferences_frame, text="📖 Documentation/Help on Github")
        github_link_button.grid(row=0, column=0, columnspan=2, sticky='ew')
        github_link_button.bind("<Button-1>", open_docs_link)
        


      
        
       



        cm_offset_label = ttk.Label(preferences_frame, text="Starting Dot Offset:")
        cm_offset_label.grid(row=2, column=0, sticky="e")

        cm_offset_entry = ttk.Entry(preferences_frame)
        cm_offset_entry.grid(row=2, column=1)

        grid_label = ttk.Label(preferences_frame, text="Track Size (rows, columns):")
        grid_label.grid(row=1, column=0, sticky="e")

        rows_entry = ttk.Entry(preferences_frame)
        rows_entry.grid(row=1, column=1)

        cols_entry = ttk.Entry(preferences_frame)
        cols_entry.grid(row=1, column=2)

        rows_entry.insert(0, str(vars['grid_y']))
        cols_entry.insert(0, str(vars['grid_x']))
        cm_offset_entry.insert(0, str(vars['cm_offset']))

        lineSpeed_label = ttk.Label(preferences_frame, text="Robot Moving Speed:")
        lineSpeed_label.grid(row=4, column=0, sticky="e")

        lineSpeed_slider = ttk.Scale(preferences_frame, from_=1, to=10, orient="horizontal", length=400)
        lineSpeed_slider.grid(row=4, column=1,columnspan=2)

        lineSpeed_slider.set(vars['lineSpeed'])
        

        variable_label = ttk.Label(preferences_frame, text="compileCommands\nFunction:")
        variable_label.grid(row=5, column=0, sticky="e")


        Grid.rowconfigure(root,5, weight=1)


        variable_entry = UndoableEntry(preferences_frame)
        try:
            with open(os.path.join(__location2__,"compileFile.py"), "r") as f:
                compileCommandsNew=f.read()
                variable_entry.insert(1.0, compileCommandsNew)
                exec(compileCommandsNew)
        except FileNotFoundError:
            with open(os.path.join(__location2__,"compileFile.py"), "w") as f:
                f.write(default_code)
            def compileCommands(commandvar):
                try:
                    return eval(commandvar), False
                except Exception as e:
                    return [], e
            variable_entry.insert(1.0, default_code)
        variable_entry.bind("<<Modified>>", modified_flag_changed_prefs)
        variable_entry.grid(row=5, column=1,columnspan=3,sticky="news")
        
        def save_prefs():
            global vars
            vars['grid_y'] = round(float(rows_entry.get()))
            
            vars['grid_x'] = round(float(cols_entry.get()))
            vars['lineSpeed'] = round(float(lineSpeed_slider.get()),2)
            vars['cm_offset'] = float(cm_offset_entry.get())
            with open(os.path.join(__location2__,"config.json"), "w") as f:
                json.dump(vars,f)
            with open(os.path.join(__location2__,"compileFile.py"), "w") as f:
                f.write(variable_entry.get('1.0','end'))
            preferences_frame.destroy()
            on_close_turtle()
        save_prefs_button = ttk.Button(preferences_frame, text="💾 Save And Quit", command=save_prefs)
        save_prefs_button.grid(row=preferences_frame.grid_size()[1]+1, column=0, columnspan=2)
        
        preferences_canvas.config(yscrollincrement = 2)
        def on_mousewheel(event):
            preferences_canvas.yview_scroll(int(-1*(event.delta*6)), "units")
        
        preferences_window.bind("<MouseWheel>", on_mousewheel)
        def _quitprefs():
            preferences_window.quit()
            preferences_window.destroy()
        preferences_window.protocol("WM_DELETE_WINDOW", _quitprefs)
        preferences_window.mainloop()
        preferences_is_open = False
    else:
        preferences_window.focus_force()




showRobotMoving=False


title_label = ttk.Label(root, text=" Enter commands here:", justify='left')
title_label.pack(expand=False, fill='x')
text_box.pack(expand=True, fill='both')
bottomFrame.pack(expand=False,fill='x')

text_box.configure(font=("Arial", 15))

def copy_text_func():
    pyperclip.copy(text_box.get('1.0','end'))

def robotmove_func():
    global showRobotMoving
    showRobotMoving=True
    tupdate()


def movetodot(x,y):
    t.up()
    if x==0:
        x += .5 
        x -= (vars['cm_offset']/50)
    elif y==0:
        y += .5  
        y -= (vars['cm_offset']/50)
        t.right(90)
    elif y==vars['grid_y']+1:
        y -= .5
        y += (vars['cm_offset']/50)
        t.left(90)
    elif x==vars['grid_x']+1:
        x -= .5
        x += (vars['cm_offset']/50)
        t.right(180)
    t.goto(((50*x)-(vars['grid_x']*25)-25)*screensSizeMultiplier,((vars['grid_y']*25)+25-(50*y))*screensSizeMultiplier)
    t.down()

buttonBox = tk.Frame(bottomFrame)
buttonBox.grid(row=0,column=2, padx=20)
big_red_label = tk.Label(buttonBox, text="", fg="red", font=("Arial",18))
big_red_label.grid(row=1, column=0, columnspan=2)
root.title("Robot Coaching Assistant")
copybutton = ttk.Button(buttonBox, text ="📋 Copy Code", command = copy_text_func)
copybutton.grid(row=0,column=0,sticky="en")
if pyperclip_enable == False:
    copybutton.config(text="",state=tk.DISABLED)



preferences_button = ttk.Button(buttonBox,  text="⚙️ Settings", command=open_preferences)
preferences_button.grid(row=0, column=1, sticky="en")


text_box.insert('1.0', "3")
text_box.delete('1.0') 


t.title("Robot Path Map")

if os.path.isfile(os.path.join(__location2__,"root2.conf")): 
    with open(os.path.join(__location2__,"root2.conf"), "r") as conf: 
        tsetup=conf.read().split('+')
        tsize=tsetup[0].split('x')
        t.setup(width=int(tsize[0]),height=int(tsize[1]),startx=int(tsetup[1]),starty=int(tsetup[2])) 
else:
    #Default window position.
    t.setup(width=800,height=800,startx=200,starty=0)


preferences_is_open = False
root.createcommand('tkAboutDialog',open_about) #set about menu
root.createcommand('tk::mac::ShowPreferences',open_preferences) #set preferences menu
root.createcommand('tk::mac::ShowHelp',open_docs_link) #set help menu



    
canvas=t.getcanvas()
#canvas.bind("<Configure>", tupdate) # doesnt work

def on_close_turtle(a=None):
    with open(os.path.join(__location2__,"root.conf"), "w") as conf: 
        conf.write(root.geometry())
    with open(os.path.join(__location2__,"root2.conf"), "w") as conf: 
        conf.write(canvas.master.geometry())
    t.bye()
    root.destroy()
    #exit()

#def fxn(x,y): 
#    print(x,y)
#t.Screen().onclick(fxn)


pencolor="black"
highlightcolor="#99DAFF"
highlightcolorGate="#E7FD67"
highlightcolorStart="#AEFFB3"
highlightcolorDot="#FF8E8E"
t.Screen().bgcolor('white')  
colorPallete=[[0.058, 0.275, 0.117], [0.683, 0.683, 0.55], [0.092, 0.308, 0.525], [0.217, 0.742, 0.008], [0.2, 0.567, 0.75], [0.267, 0.517, 0.142], [0.6, 0.2, 0.508], [0.717, 0.45, 0.283], [0.133, 0.05, 0.567], [0.35, 0.717, 0.5], [0.292, 0.475, 0.742], [0.317, 0.117, 0.325], [0.15, 0.6, 0.192], [0.008, 0.108, 0.55], [0.483, 0.383, 0.75], [0.3, 0.383, 0.342], [0.683, 0.533, 0.308], [0.467, 0.158, 0.3], [0.475, 0.025, 0.517], [0.533, 0.242, 0.592], [0.467, 0.133, 0.617], [0.0, 0.617, 0.133], [0.133, 0.617, 0.4], [0.308, 0.233, 0.45], [0.592, 0.475, 0.267], [0.392, 0.417, 0.367], [0.55, 0.608, 0.642], [0.233, 0.592, 0.275], [0.275, 0.458, 0.342], [0.208, 0.258, 0.2], [0.217, 0.65, 0.242], [0.233, 0.108, 0.008], [0.275, 0.208, 0.333], [0.4, 0.167, 0.383], [0.492, 0.583, 0.517], [0.65, 0.05, 0.575], [0.275, 0.05, 0.058], [0.692, 0.717, 0.008], [0.617, 0.383, 0.617], [0.542, 0.742, 0.167], [0.525, 0.067, 0.4], [0.2, 0.25, 0.233], [0.4, 0.325, 0.358], [0.642, 0.717, 0.4], [0.392, 0.183, 0.233], [0.425, 0.075, 0.583], [0.25, 0.583, 0.283], [0.575, 0.25, 0.467], [0.467, 0.292, 0.008], [0.05, 0.6, 0.042], [0.258, 0.142, 0.092], [0.667, 0.367, 0.508], [0.233, 0.442, 0.05], [0.35, 0.15, 0.317], [0.65, 0.608, 0.317], [0.175, 0.717, 0.625], [0.625, 0.35, 0.408], [0.475, 0.208, 0.592], [0.25, 0.442, 0.25], [0.425, 0.3, 0.317], [0.592, 0.242, 0.217], [0.692, 0.717, 0.692], [0.383, 0.25, 0.508], [0.25, 0.4, 0.358], [0.617, 0.192, 0.142], [0.583, 0.225, 0.192], [0.5, 0.742, 0.0], [0.125, 0.208, 0.075], [0.267, 0.033, 0.142], [0.283, 0.567, 0.717], [0.075, 0.617, 0.408], [0.583, 0.642, 0.625], [0.325, 0.592, 0.342], [0.55, 0.742, 0.683], [0.25, 0.7, 0.458], [0.208, 0.075, 0.642], [0.283, 0.608, 0.525], [0.242, 0.217, 0.433], [0.3, 0.733, 0.033], [0.167, 0.75, 0.133], [0.75, 0.35, 0.225], [0.542, 0.4, 0.508], [0.558, 0.15, 0.608], [0.267, 0.167, 0.4], [0.033, 0.133, 0.467], [0.717, 0.683, 0.1], [0.283, 0.742, 0.55], [0.375, 0.417, 0.667], [0.017, 0.658, 0.233], [0.333, 0.075, 0.075], [0.35, 0.292, 0.408], [0.658, 0.642, 0.4], [0.492, 0.183, 0.633], [0.267, 0.117, 0.508], [0.425, 0.117, 0.292], [0.342, 0.15, 0.058], [0.317, 0.417, 0.25], [0.133, 0.658, 0.75], [0.683, 0.55, 0.583], [0.567, 0.567, 0.617], [0.65, 0.083, 0.708], [0.483, 0.533, 0.158], [0.658, 0.325, 0.258], [0.092, 0.533, 0.283], [0.025, 0.725, 0.717], [0.033, 0.442, 0.358], [0.058, 0.625, 0.517], [0.325, 0.742, 0.3], [0.233, 0.458, 0.717], [0.708, 0.2, 0.083], [0.292, 0.517, 0.275], [0.625, 0.192, 0.242], [0.575, 0.217, 0.267], [0.508, 0.725, 0.25], [0.708, 0.108, 0.175], [0.158, 0.542, 0.142], [0.55, 0.25, 0.542], [0.008, 0.267, 0.542], [0.067, 0.675, 0.2], [0.05, 0.492, 0.475], [0.333, 0.517, 0.225], [0.283, 0.492, 0.608], [0.567, 0.558, 0.733], [0.125, 0.567, 0.75], [0.633, 0.008, 0.492], [0.625, 0.142, 0.2], [0.525, 0.742, 0.133], [0.508, 0.567, 0.133], [0.35, 0.408, 0.6], [0.358, 0.15, 0.192], [0.492, 0.483, 0.167], [0.533, 0.35, 0.017], [0.283, 0.408, 0.042], [0.267, 0.65, 0.333], [0.108, 0.333, 0.725], [0.75, 0.008, 0.358], [0.158, 0.025, 0.467], [0.375, 0.725, 0.108], [0.517, 0.067, 0.7], [0.417, 0.442, 0.083], [0.467, 0.383, 0.392], [0.475, 0.733, 0.058], [0.117, 0.292, 0.542], [0.575, 0.3, 0.617], [0.458, 0.5, 0.042], [0.108, 0.15, 0.15], [0.042, 0.642, 0.258], [0.483, 0.358, 0.258], [0.717, 0.083, 0.3], [0.008, 0.55, 0.075], [0.0, 0.108, 0.175], [0.075, 0.642, 0.067], [0.433, 0.075, 0.608], [0.25, 0.358, 0.275], [0.125, 0.092, 0.317], [0.575, 0.733, 0.067], [0.142, 0.442, 0.458], [0.175, 0.4, 0.367], [0.3, 0.283, 0.208], [0.617, 0.558, 0.242], [0.625, 0.675, 0.542], [0.467, 0.4, 0.342], [0.733, 0.667, 0.425], [0.158, 0.275, 0.508], [0.1, 0.725, 0.408], [0.583, 0.067, 0.15], [0.175, 0.092, 0.733], [0.483, 0.667, 0.358], [0.292, 0.5, 0.583], [0.425, 0.633, 0.058], [0.417, 0.075, 0.233], [0.15, 0.258, 0.025], [0.75, 0.542, 0.192], [0.558, 0.2, 0.058], [0.242, 0.617, 0.683], [0.75, 0.658, 0.183], [0.242, 0.533, 0.192], [0.525, 0.642, 0.367], [0.608, 0.158, 0.333], [0.092, 0.083, 0.217], [0.325, 0.65, 0.592], [0.033, 0.333, 0.017], [0.658, 0.208, 0.283], [0.133, 0.675, 0.4], [0.425, 0.142, 0.225], [0.725, 0.567, 0.283], [0.675, 0.392, 0.258], [0.7, 0.25, 0.508], [0.375, 0.7, 0.125], [0.142, 0.625, 0.642], [0.617, 0.267, 0.208], [0.675, 0.075, 0.525], [0.7, 0.067, 0.25], [0.292, 0.125, 0.392], [0.283, 0.6, 0.425], [0.0, 0.408, 0.175], [0.217, 0.317, 0.475], [0.067, 0.7, 0.058], [0.275, 0.158, 0.042], [0.375, 0.575, 0.067]]
t.pencolor(pencolor)
barrierColor="#AE5800"
barrierList=[]
gatezones=[]
highlightOn=False
gateSelect=False
enddotx=0
enddoty=0
xvar=1
yvar=0

def toggleHighlight():
    global highlightOn
    global gateSelect
    if highlightOn == True:
        highlightOn=False
    else:
        highlightOn=True
        gateSelect=False
    tupdate()

canvas.master.minsize(500,600)
canvas.master.protocol("WM_DELETE_WINDOW", on_close_turtle)
root.protocol("WM_DELETE_WINDOW", on_close_turtle)
root.createcommand("::tk::mac::Quit", on_close_turtle)
movebutton = tk.Button(canvas.master, text ="▶", command = robotmove_func, width=1, height=1, font=('TkDefaultFont', 20),bg="white", fg="black")
movebutton_label = tk.Label(canvas.master, text="Animate", font=('TkDefaultFont', 10), bg="white", fg="black")
movebutton_label.place(x=3, y=40)
movebutton.place(x=0,y=0)

gatebutton = tk.Button(canvas.master, text ="🟩", command = lambda: toggleGateSelect(), width=1, height=1, font=('TkDefaultFont', 20),bg="white", fg="black")
gatebutton_label = tk.Label(canvas.master, text="Set\nGates", font=('TkDefaultFont', 10), bg="white", fg="black")
gatebutton.place(x=0,y=200)
gatebutton_label.place(x=3, y=240)

def toggleGateSelect():
    global gateSelect, gatezones, highlightOn
    if gateSelect:
        gateSelect = False
    else:
        gateSelect = True
        highlightOn = False
    tupdate()


barrierbutton = tk.Button(canvas.master, text ="📐", command = toggleHighlight, width=1, height=1, font=('TkDefaultFont', 20),bg="white", fg="black")
barrierbutton_label = tk.Label(canvas.master, text="Set\nCourse", font=('TkDefaultFont', 10), bg="white", fg="black")
barrierbutton.place(x=0,y=100)
barrierbutton_label.place(x=3, y=140)

barrier=[]

def on_canvas_click(event):  
    global barrierList
    global enddotx, enddoty
    turtlecol= (event.x - canvas.winfo_width()/2)  / (25*screensSizeMultiplier)
    turtlerow= -(event.y - canvas.winfo_height()/2) / (25*screensSizeMultiplier)
    if highlightOn == True:
        if (abs(turtlecol - round(turtlecol)) < 0.3) and round(turtlecol) % 2 == vars['grid_x'] % 2:
            turtlecol=int((round(turtlecol)+vars['grid_x'])/2)
            turtlerow=int(((turtlerow)+vars['grid_y'])/2)+1
            if turtlerow >= 1 and turtlerow <= vars['grid_y'] and turtlecol >= 1 and turtlecol <= (vars['grid_x']-1):
                #print("COL CLICKED")
                #print("row ",turtlerow)
                #print("col ",turtlecol)
                #print("")
                barrier = [0,turtlecol,turtlerow]
                if barrier in barrierList:
                    barrierList.remove(barrier)
                else:
                    barrierList.append(barrier)
            elif turtlecol == 0 or turtlecol == (vars['grid_x']):
                if turtlecol > 0:
                    turtlecol += 1
                selectStart((vars['grid_y']-(turtlerow-1)),turtlecol)
        elif (abs(turtlerow - round(turtlerow)) < 0.3) and round(turtlerow) % 2 == vars['grid_y'] % 2:
            turtlerow=int((round(turtlerow)+vars['grid_y'])/2)+1
            turtlecol=int(((turtlecol)+vars['grid_x'])/2)
            if turtlerow >= 2 and turtlerow <= vars['grid_y'] and turtlecol >= 0 and turtlecol <= (vars['grid_x']-1):
                #print("ROW CLICKED")
                #print("row ",turtlerow)
                #print("col ",turtlecol)
                #print("")
                barrier = [1,turtlecol,turtlerow]
                if barrier in barrierList:
                    barrierList.remove(barrier)
                else:
                    barrierList.append(barrier)
            elif turtlerow == 1 or turtlerow == (vars['grid_y']+1):
                turtlecol += 1
                if turtlerow > 1:
                    turtlerow += 1
                selectStart((vars['grid_y']-(turtlerow-2)),turtlecol)
        elif abs(turtlecol - round(turtlecol)) < 0.3 and abs(turtlerow - round(turtlerow)) < 0.3:
            turtlecol = int((round(turtlecol)+vars['grid_x'])/2)
            turtlerow = int(((turtlerow)+vars['grid_y'])/2)+1
            enddotx=turtlecol
            enddoty=turtlerow

        tupdate()
    elif gateSelect == True:
        turtlerow=(((turtlerow)+vars['grid_y'])/2)
        turtlecol=(((turtlecol)+vars['grid_x'])/2)
        if turtlerow > 0:
            turtlerow=int(turtlerow)
        else:
            turtlerow=-1
        if turtlecol > 0:
            turtlecol=int(turtlecol)
        else:
            turtlecol=-1
        if turtlerow >= 0 and turtlecol >= 0 and turtlerow < vars['grid_y'] and turtlecol < vars['grid_x']:
            #print(f"Cell clicked: column {turtlecol}, row {turtlerow}")
            gatezones.append([turtlerow+1,turtlecol])
            tupdate()

# Add near bottom of file, before mainloop
canvas.bind('<Button-1>', on_canvas_click)



def disable_space(event):
    if event.char == ' ':
        return 'break'

movebutton.bind('<space>', disable_space)
barrierbutton.bind('<space>', disable_space)
def clear_all():
    global barrierList, gatezones, enddotx, enddoty, xvar, yvar, highlightOn, gateSelect
    barrierList = []
    gatezones = []
    enddotx = 0
    enddoty = 0
    xvar = 1
    yvar = 0
    highlightOn=False
    gateSelect=False
    tupdate()

clearbutton = tk.Button(canvas.master, text ="🗑", command = clear_all, width=1, height=1, font=('TkDefaultFont', 20), bg="white", fg="black")
clearbutton_label = tk.Label(canvas.master, text="Clear\nAll", font=('TkDefaultFont', 10), bg="white", fg="black")
clearbutton.place(x=0,y=300)
clearbutton_label.place(x=3, y=340)
clearbutton.bind('<space>', disable_space)
def on_resize(event):
    tupdate()
        
#canvas.bind('<Configure>', on_resize)


def show_error_dialog(message):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("300x100")
    error_window.resizable(False, False)
    
    error_label = ttk.Label(error_window, text=message, wraplength=250)
    error_label.pack(pady=20)
    
    ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()
    
    error_window.transient(root)
    error_window.grab_set()
    error_window.wait_window()

def save_layout():
    global vars
    
    layout_data = {
        'grid_x': vars['grid_x'],
        'grid_y': vars['grid_y'],
        'start': {'x': xvar, 'y': yvar},
        'end': {'x': enddotx, 'y': enddoty},
        'barriers': barrierList,
        'gates': gatezones,
        'instructions': text_box.get('1.0', 'end').strip() # Add instructions from text box
    }
    
    filename = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        initialfile="RCA_layout.json"
    )
    
    if filename:
        with open(filename, "w") as f:
            json.dump(layout_data, f)

def load_layout():
    global xvar, yvar, enddotx, enddoty, barrierList, gatezones
    
    filename = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )
    
    if filename:
        try:
            with open(filename, "r") as f:
                layout_data = json.load(f)
                if layout_data['grid_x'] != vars['grid_x'] or layout_data['grid_y'] != vars['grid_y']:
                    show_error_dialog(f"Course size mismatch!\nFile is {layout_data['grid_y']}x{layout_data['grid_x']}\nCurrent size is {vars['grid_y']}x{vars['grid_x']}")
                    return
                    
                xvar = layout_data['start']['x']
                yvar = layout_data['start']['y']
                enddotx = layout_data['end']['x']
                enddoty = layout_data['end']['y']
                barrierList = layout_data['barriers']
                gatezones = layout_data['gates']
                # Load instructions into text box
                text_box.delete('1.0', 'end')
                text_box.insert('1.0', layout_data['instructions'])
                tupdate()
        except Exception as e:
            show_error_dialog(f"Error loading layout file:\n{str(e)}")
#load_layout()
savebutton = tk.Button(canvas.master, text ="💾", command = save_layout, width=1, height=1, font=('TkDefaultFont', 20),bg="white", fg="black")
savebutton_label = tk.Label(canvas.master, text="Save\nLayout", font=('TkDefaultFont', 10), bg="white", fg="black")
savebutton.place(x=0,y=400)
savebutton_label.place(x=3, y=440)
savebutton.bind('<space>', disable_space)
loadbutton = tk.Button(canvas.master, text ="📂", command = load_layout, width=1, height=1, font=('TkDefaultFont', 20),bg="white", fg="black")
loadbutton_label = tk.Label(canvas.master, text="Load\nLayout", font=('TkDefaultFont', 10), bg="white", fg="black")
loadbutton.place(x=0,y=500)
loadbutton_label.place(x=3, y=540)
loadbutton.bind('<space>', disable_space)

# Animate button
movebutton.place(x=0,y=0)
movebutton_label.place(x=3, y=40)

# Set Course button
barrierbutton.place(x=0,y=70)
barrierbutton_label.place(x=3, y=110)

# Set Gates button
gatebutton.place(x=0,y=150)
gatebutton_label.place(x=3, y=190)

# Clear All button
clearbutton.place(x=0,y=230)
clearbutton_label.place(x=3, y=270)

# Save Layout button
savebutton.place(x=0,y=310)
savebutton_label.place(x=3, y=350)

# Load Layout button
loadbutton.place(x=0,y=390)
loadbutton_label.place(x=3, y=430)




tupdate()
_thread.start_new_thread(t.mainloop,())
root.mainloop()

#t.done