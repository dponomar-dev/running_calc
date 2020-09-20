import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import re

def add_split():
    entry = tk.Entry(root)
    list = root.pack_slaves()
    #num = len(list) - num_buttons
    #text = tk.Label(root, text=str(num))
    if (len(list) < max_entries + num_buttons):
        entry.pack()
    #calc_avg()

def del_split():
    list = root.pack_slaves()
    if (len(list) > num_buttons):
        list[-1].destroy()
    #calc_avg()

def read_split(file_name):
    list = root.pack_slaves()
    i=0
    file = open(file_name,"w")
    for l in list:
        i+=1
        if i > num_buttons and getattr(l) == tk.Entry:
            file.write(l.get())
            file.write("\n")
    file.close()

def open_split():
    files = [('Text Document', '*.txt'),
                ('All Files', '*.*')]
    name = fd.askopenfilename(title="Open", filetypes=files)
    print(name)
    file = open(name, "r")
    primary_title = " - Running Calculator"
    file_title = os.path.basename(name)
    file_title += primary_title
    root.title(file_title)

    f = file.read()
    newline = f.count('\n')
    file.close()

    file = open(name, "r")

    for n in range(newline):
        split = file.readline()
        add_split()
        list = root.pack_slaves()
        list[-1].insert("insert",split)
    file.close()
#def save():
#    fd.SaveFileDialog
def save_as():
    files = [('Text Document', '*.txt'),
                ('All Files', '*.*')]
    saveas = fd.asksaveasfile(filetypes=files, defaultextension=files)
    print(saveas.name)
    read_split(saveas.name)

def quit():
    if mb.askyesno(title="Quit", message="Really quit?"):
        root.destroy()

def calc_avg():
    list = root.pack_slaves()
    avg_sec = 0.0
    avg_min = 0

    for l in list[num_buttons:]:
        pattern = re.compile(':')
        result = pattern.search(l.get())

        if result == None:
            avg_sec += float(l.get())
        else:
            min = ""
            sec = ""
            for j in range(result.span()[0]):
                min += l.get()[j]
            for j in range(len(l.get())):
                if j > result.span()[0]:
                    sec += l.get()[j]

            min = int(min)
            sec = float(sec)
            avg_min += min                      #indices 0 to result.span()[0] (exclusive) are MINUTES indices
            avg_sec += sec                      #indices result.span()[0] + 1 to l.get()[-1] (last index) are SECONDS indices
                                                # print(result.span()[0]) #returns position of ':'
    avg_min = int(avg_min / (len(list)-num_buttons))
    avg_min = str(avg_min)
    avg_sec /= (len(list)-num_buttons)

    if avg_sec < 10:
        avg_sec = "0" + str(avg_sec)
    else:
        avg_sec = str(avg_sec)

    if avg_min == "0":
        avg_pace = tk.Label(root, text="Average Pace: " + avg_sec)
        avg_pace.pack()
    else:
        avg_min = avg_min + ":" + avg_sec
        avg_pace = tk.Label(root, text="Average Pace: " + avg_min)
        avg_pace.pack()

def change_units():
    print("hi")
    #change between km, mi, or interval lengths. ability to select a standard distance
    # ie 12x400m workout, I select meters and 400. everything is 400m.
    # say I do 1k, 800, 600, 400, 400, 400. I select 400m to start and that makes everything 400m
    # then I should be able to modify everything else as I wish quickly
def change_format():
    print("hi")

max_entries = 20
num_buttons = 3
root = tk.Tk()
root.geometry('400x200')
root.title('Running Calculator')
image = tk.PhotoImage(file="Milkbot.png")
root.iconphoto(False, image)

add = tk.Button(root, text="Add", fg="black", command=add_split)
add.pack(side="left", ipadx=50, anchor="n", pady=10)

delete = tk.Button(root, text="Delete", fg="black", command=del_split)
delete.pack(side="left", ipadx=50, anchor="n", pady=10)

read = tk.Button(root, text="read", fg="black", command=calc_avg)
read.pack(side="left", ipadx=50, anchor="n", pady=10)

separator = tk.Button(root, text="f")
separator.pack(padx=0, pady=50)

#scrollbar = tk.Scrollbar(root)
#scrollbar.pack(side="right", fill="y")

#listbox = tk.Listbox(root)
#listbox.pack()

menubar = tk.Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=open_split) #fd.open_file_dir
filemenu.add_command(label="Save", command=save_as) #fd.save_current_proj
filemenu.add_command(label="Save as", command=save_as) #fd.save_current_proj
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

optionsmenu=tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=optionsmenu)
optionsmenu.add_command(label="Units", command=change_units)

aboutmenu=tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=aboutmenu)
#aboutmenu.add_command(label="About the Creator",)


root.config(menu=menubar)
root.mainloop()

#TODO - HIGH TO LOW PRIORITY

#DONE - Calculate average pace
#       Parse through strings that have ':' to separate between hours, minutes, and seconds

#TODO - Modify add_entry() to add another entry to the second to last index
#       switching to grid_slaves instead of pack_slaves might make this easier

#TODO - Save average pace in file, will be easier if indices of non-textbox grid/pack slaves are nice

#TODO - Ignore average pace in file when opening a .txt file that was saved
# append '#' to beginning of string, search for '#', and then don't populate the program with that dat
# program should calculate average pace IF there is not a empty Entrybox
# it should do this in real-time. If I enter '6' and then '5', it should have done calculations for '6' and '65'

#TODO - restrict entry of non-numerical chars (except : and ./,)


#TODO - SCROLLBAR - Implement scrollbar widget so splits don't disappear when you
#                    enter beyond the window boundaries

#TODO - Save button
#TODO - Keyboard shortcuts (Ctrl+O, Ctrl+S, etc.)
#TODO - Upper left icon and taskbar icon
#TODO - dropdown menus to select distance
#TODO - configuration: default distance, custom distance
