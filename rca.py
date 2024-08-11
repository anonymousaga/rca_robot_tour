#!/usr/bin/env python3
import turtle as t
from random import randint
import time
import tkinter as tk
import _thread 
#from ast import literal_eval
import json
import os
import sys
from compileFile import *
from tkinter import font, ttk
from tkinter import *
import webbrowser


pyperclip_enable=True
if pyperclip_enable==True:
    import pyperclip
import toml







if getattr(sys, 'frozen', False):
    # The application is frozen
    __location__  = os.path.dirname(sys.executable)
    if not os.path.isfile(os.path.join(__location__,"config.json")):
        # The application is not frozen
        # Change this bit to match where you store your data files:
        __location__  = os.path.join(os.path.dirname(sys.executable),'../Resources')
        print(__location__)
else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    __location__  = os.path.dirname(__file__)

commands=[]
root=tk.Tk()
#scale is pixel = cm 

with open(os.path.join(__location__,"config.json"), "r") as f:
    vars = json.load(f)


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

def darkmode():
    global vars
    if vars['darkmode']=="yes":
        return True
    elif vars['darkmode']=="no":
        return False

def read_commandstk():
    global commands
    global root
    commands=text_box.get('1.0','end')
    commands, error = compileCommands(commands)
    if error == False:
        big_red_label.config(text="")
        root.quit()
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
    root.geometry('1000x800+0+0')


    
 





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

# Read the pyproject.toml file
with open(os.path.join(__location__,"pyproject.toml"), "r") as f:
    version = toml.load(f)["project"]["version"]

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






def open_preferences():
    global vars
    global preferences_is_open
    global preferences_window
    
    if preferences_is_open is False:
        preferences_is_open = True
        preferences_window = tk.Toplevel(root)
        preferences_window.title("Preferences")
        preferences_window.minsize(600,420)
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

        darkmode_label = ttk.Label(preferences_frame, text="Dark Mode for map:")
        darkmode_label.grid(row=3, column=0, sticky="e")

    


        github_link_button = ttk.Button(preferences_frame, text="Documentation/Help on Github")
        github_link_button.grid(row=0, column=0, columnspan=2, sticky='ew')
        github_link_button.bind("<Button-1>", open_docs_link)
        


        darkmode_frame = ttk.Frame(preferences_frame)
        darkmode_frame.grid(row=3, column=1)

        darkmode_var = tk.StringVar(value=vars['darkmode'])
        
        yes_radio = ttk.Radiobutton(darkmode_frame, text="Yes", variable=darkmode_var, value="yes")
        yes_radio.pack(side="left", padx=10)

        no_radio = ttk.Radiobutton(darkmode_frame, text="No", variable=darkmode_var, value="no")
        no_radio.pack(side="left", padx=10)

        vars['darkmode'] = darkmode_var.get()

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
        with open(os.path.join(__location__,"compileFile.py"), "r") as f:
            variable_entry.insert(1.0, f.read())
        variable_entry.bind("<<Modified>>", modified_flag_changed_prefs)
        variable_entry.grid(row=5, column=1,columnspan=3,sticky="news")
        
        def save_prefs():
            global vars
            vars['grid_y'] = round(float(rows_entry.get()))
            vars['darkmode'] = darkmode_var.get()
            vars['grid_x'] = round(float(cols_entry.get()))
            vars['lineSpeed'] = round(float(lineSpeed_slider.get()),2)
            vars['cm_offset'] = float(cm_offset_entry.get())
            with open(os.path.join(__location__,"config.json"), "w") as f:
                json.dump(vars,f)
            with open(os.path.join(__location__,"compileFile.py"), "w") as f:
                f.write(variable_entry.get('1.0','end'))
            preferences_frame.destroy()
            on_close_turtle()
        save_prefs_button = ttk.Button(preferences_frame, text="Save Preferences And Quit", command=save_prefs)
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
if True: # code for the radio button grid
    xvar=1
    yvar=0

    # Function to print the index of the selected radio button
    def print_selected_coordinates():
        global xvar,yvar
        index = radio_var.get()

        xvar = index % (vars['grid_x']+2)
        yvar = index // (vars['grid_x']+2)
        root.quit()

    selectframe=tk.Frame(bottomFrame)
    selectframe.grid(row=0,column=1)

    # Configure the grid
    for i in range(vars['grid_y']+2):
        selectframe.grid_rowconfigure(i, weight=1)
    for j in range(vars['grid_x']+2):
        selectframe.grid_columnconfigure(j, weight=1)

    # Create a variable to hold the value of the selected radio button
    radio_var = tk.IntVar(value=1)
    
    # Function to create a frame with a radio button on the edge
    def create_frame_with_radio(row, col, side,master):
        frame = tk.Frame(master)
        frame.grid(row=row, column=col, sticky="nsew")
        if side == "top":
            radio = tk.Radiobutton(frame, variable=radio_var, value=row*(vars['grid_x']+2)+col, command=print_selected_coordinates)
            radio.pack(side="top")
        elif side == "bottom":
            radio = tk.Radiobutton(frame, variable=radio_var, value=row*(vars['grid_x']+2)+col, command=print_selected_coordinates)
            radio.pack(side="bottom")
        elif side == "left":
            radio = tk.Radiobutton(frame, variable=radio_var, value=row*(vars['grid_x']+2)+col, command=print_selected_coordinates)
            radio.pack(side="left")
        elif side == "right":
            radio = tk.Radiobutton(frame, variable=radio_var, value=row*(vars['grid_x']+2)+col, command=print_selected_coordinates)
            radio.pack(side="right")

    # Create the 6x7 grid of frames with radio buttons on the edges
    for i in range(vars['grid_y']+2):
        for j in range(vars['grid_x']+2):
            if (i == 0 and j not in [0, vars['grid_x']+1]) or (i == vars['grid_y']+1 and j not in [0, vars['grid_x']+1]):
                create_frame_with_radio(i, j, "top" if i == 0 else "bottom",selectframe)
            elif (j == 0 and i not in [0, vars['grid_y']+1]) or (j == vars['grid_x']+1 and i not in [0, vars['grid_y']+1]):
                create_frame_with_radio(i, j, "left" if j == 0 else "right",selectframe)
            elif (i == 0 and j == 0) or (i == 0 and j == vars['grid_x']+1) or (i == vars['grid_y']+1 and j == 0) or (i == vars['grid_y']+1 and j == vars['grid_x']+1):
                create_frame_with_radio(i, j, "none",selectframe)
            else:
                frame = tk.Frame(selectframe, borderwidth=1, relief="solid")
                frame.grid(row=i, column=j, sticky="nsew")






title_label = ttk.Label(root, text=" Enter commands here:", justify='left')
radio_label = ttk.Label(bottomFrame, text=" Start\n Point", justify='right',padding=2)
radio_label.grid(row=0, column=0)
title_label.pack(expand=False, fill='x')
text_box.pack(expand=True, fill='both')
bottomFrame.pack(expand=False,fill='x')

text_box.configure(font=("Arial", 15))

def copy_text_func():
    pyperclip.copy(text_box.get('1.0','end'))

def robotmove_func():
    global showRobotMoving
    showRobotMoving=True
    root.quit()
def resize(a=None):
    global screensSizeMultiplier
    xe=t.window_width()
    ye=t.window_height()
    if xe/ye > vars['grid_x']/vars['grid_y']:
        screensSizeMultiplier = (ye/(50*vars['grid_y'])) * 0.8
    else:
        screensSizeMultiplier = (xe/(50*vars['grid_x'])) * 0.85

    root.quit()

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
copybutton = ttk.Button(buttonBox, text ="Copy Code", command = copy_text_func)
copybutton.grid(row=0,column=0,sticky="en")
if pyperclip_enable == False:
    copybutton.config(text="",state=tk.DISABLED)



preferences_button = ttk.Button(buttonBox, text="Settings", command=open_preferences)
preferences_button.grid(row=0, column=1, sticky="en")


text_box.insert('1.0', "3")
text_box.delete('1.0') 

root.mainloop()
t.title("Robot Path Map")

if os.path.isfile(os.path.join(__location__,"root2.conf")): 
    with open(os.path.join(__location__,"root2.conf"), "r") as conf: 
        tsetup=conf.read().split('+')
        tsize=tsetup[0].split('x')
        t.setup(width=int(tsize[0]),height=int(tsize[1]),startx=int(tsetup[1]),starty=int(tsetup[2])) 
else:
    #Default window position.
    t.setup(width=1000,height=800,startx=0,starty=0)


preferences_is_open = False
root.createcommand('tkAboutDialog',open_about) #set about menu
root.createcommand('tk::mac::ShowPreferences',open_preferences) #set preferences menu
root.createcommand('tk::mac::ShowHelp',open_docs_link) #set help menu



    
canvas=t.getcanvas()
canvas.bind("<Configure>", resize)
resize()

def on_close_turtle(a=None):
    with open(os.path.join(__location__,"root.conf"), "w") as conf: 
        conf.write(root.geometry())
    with open(os.path.join(__location__,"root2.conf"), "w") as conf: 
        conf.write(canvas.master.geometry())
    t.bye()
    root.destroy()
    #exit()

#def fxn(x,y): 
#    print(x,y)
#t.Screen().onclick(fxn)
canvas.master.minsize(500,600)
canvas.master.protocol("WM_DELETE_WINDOW", on_close_turtle)
root.protocol("WM_DELETE_WINDOW", on_close_turtle)
root.createcommand("::tk::mac::Quit", on_close_turtle)
movebutton = ttk.Button(canvas.master, text ="Robot Moving Animation", command = robotmove_func)
movebutton.place(x=0,y=0)


while True:
    try:
        t.speed("fastest")
        t.tracer(0,0)
        #canvas.delete("all")
        #rect = canvas.create_rectangle(10*screensSizeMultiplier, 10*screensSizeMultiplier, 50*screensSizeMultiplier, 50*screensSizeMultiplier, fill="blue")

        t.reset()
        if darkmode() == True:
            t.color('white')
            t.Screen().bgcolor('black')
            t.pencolor('#888888')
        else:
            t.color('black')
            t.Screen().bgcolor('white')  
            t.pencolor("black")
        t.width(1*screensSizeMultiplier)

        # Draw a grid with 4 rows and 5 columns
        for row in range(1,vars['grid_y']+1):
            for col in range(vars['grid_x']):
                # Calculate the x and y coordinates for each cell
                x = col * 50 *screensSizeMultiplier
                y = row * 50 *screensSizeMultiplier
                
                # Move the turtle to the starting position of the cell
                t.up()
                t.goto((x-(vars['grid_x']*25)*screensSizeMultiplier), (y-(vars['grid_y']*25)*screensSizeMultiplier))
                t.down()
                
                # Draw the cell
                for _ in range(4):
                    t.forward(50*screensSizeMultiplier)
                    t.right(90)

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


        for command in commands:
            if darkmode() == True:
                t.pencolor(randint(40,115)/120,randint(40,115)/120,randint(40,115)/120)
            else:
                t.pencolor(randint(0,90)/120,randint(0,90)/120,randint(0,90)/120)
            if command[0] == 0: #straight moves
                t.forward(command[1]*screensSizeMultiplier)
            elif command[0] == 1: #turn moves
                if command[1] < 0:
                    t.left(command[1]*-1)
                else:
                    t.right(command[1])

        t.color('red')
        t.up()
        t.update()
        showRobotMoving = False   


        t.mainloop()
    except t.Terminator:
        break
t.done