import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import re

max_entries = 20
num_buttons = 3

class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_UI()

    def init_UI(self):
        self.parent.geometry('400x200')
        self.parent['bg'] = "#39cced"
        self.parent.minsize(width=400, height=200)
        self.parent.maxsize(width=400, height=200)
        self.parent.title('Running Calculator')
        image = tk.PhotoImage(file="Milkbot.png")
        #self.parent.iconphoto(True, image)

        self.mode_convert()
        menubar = tk.Menu(self.parent)

        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New" + "                 Ctrl+N", command=self.new_window)  # fd.open_file_dir
        filemenu.add_command(label="Open" + "               Ctrl+O", command=self.open_window)  # fd.open_file_dir
        filemenu.add_command(label="Save As" + "            Ctrl+S", command=self.save_as)  # fd.save_current_proj
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        optionsmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modes", menu=optionsmenu)
        optionsmenu.add_command(label="Split", command=self.mode_split)
        optionsmenu.add_command(label="Convert", command=self.mode_convert)
        optionsmenu.add_command(label="Pacing", command=self.mode_pacing)

        aboutmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=aboutmenu)
        # aboutmenu.add_command(label="About the Creator",)

        self.parent.config(menu=menubar)
        self.bind("<Key>", self.event_root)

    def del_avg(self):
        list = self.parent.grid_slaves()
        if (type(list[0]) == tk.Label):
            list[0].destroy()

    def add_split(self):
        self.del_avg()
        entry = tk.Entry(self.parent)
        list = self.parent.grid_slaves()
        # num = len(list) - num_buttons
        # text = tk.Label(root, text=str(num))
        if (len(list) < max_entries + num_buttons):
            entry.grid()
        if (len(list) > (num_buttons + 5)) and len(list) < max_entries + num_buttons:
            self.parent.minsize(width=400, height=200 + (20 * (len(list) - (num_buttons + 5))))
            self.parent.maxsize(width=400, height=500)

    def del_split(self):
        self.del_avg()
        list = self.parent.grid_slaves()
        if (len(list) > num_buttons):
            list[0].destroy()
        # calc_avg()
        if len(list) > (num_buttons + 5):
            self.parent.minsize(width=400, height=200 + (20 * (len(list) - (num_buttons + 7))))
        else:
            self.parent.minsize(width=400, height=200)

    def read_split(self, file_name):
        list = self.parent.grid_slaves()
        if (type(list[0]) == tk.Label):
            list[0].destroy()  # kinda jank, but this runs the first part of the function that checks if the first item
        file = open(file_name, "w")  # in the array is a Label. If you don't have the print statement here, the first part of
        file.write("SPLIT MODE\n")
        for l in reversed(list):  # the function doesn't run
            if type(l) == tk.Entry:
                file.write(l.get())
                file.write("\n")
            elif type(l) == tk.Label:
                file.write(self.calc_avg())
                file.write("\n")
        file.close()

    def open_split(self, file_title, file, name):
        f = file.read()
        newline = f.count('\n')
        file.close()

        new_wind = self.new_window()
        new_wind.parent.title(file_title)
        new_wind.mode_split()
        file = open(name, "r")
        file.readline()
        for n in range(newline):
            split = file.readline()
            split = split[:-1]  # removes the newline character
            pace_str = re.compile("Average Pace")
            result = pace_str.search(split)
            if result is None:
                new_wind.add_split()
                list = new_wind.parent.grid_slaves()
                list[0].insert("insert", split)
            else:
                avg_pace = tk.Label(new_wind.parent, text=split)
                avg_pace.grid()
        file.close()

    def read_convert(self, file_name):
        list = self.parent.grid_slaves()
        file = open(file_name, "w")
        entry_list = []
        for i, l in enumerate(reversed(list)):
            if type(l) == tk.Entry:
                entry_list += [i]
                print(list[1].get())
                print(entry_list)

        file.write("CONVERT MODE\n")
        for i, l in enumerate(reversed(list)):
            print(i, type(l))
            if type(l) == tk.Entry:
                print(i, l.get())
                if i == 2:
                    file.write(l.get())
                    file.write(" mi in\n")
                elif i == 4:
                    file.write(l.get())
                    file.write(":")
                elif i == 6:
                    if float(l.get()) < 10:
                        file.write("0" + l.get())
                    else:
                        file.write(l.get())
                    file.write("\n")
                elif i == 8:
                    file.write("Equivalent to:\n")
                    # if entry_cnt == 4:
                    #     file.write("200m in\n")
                    # else:
                    #     file.write("1km in\n")

                    #TODO need to have method for getting output minutes and having it write nicely =)
                    file.write(l.get())
                    file.write("s\n")
        file.close()

    def open_convert(self, file_title, file, name):
        pass

    def read_pace(self, file_name):
        list = self.parent.grid_slaves()
        file = open(file_name, "w")
        file.write("PACE MODE\n")
        for i, l in enumerate(reversed(list)):
            if type(l) == tk.Label and i > 8:
                print(i, l["text"])
                file.write(l["text"])
                file.write("\n")
            else:
                print(i, type(l))
        file.close()

    def open_pace(self, file_title, name):
        input_choices = ["200m", "400m", "800m", "1mi", "2mi", "3mi", "5k", "4mi", "5mi"]
        report_choices = input_choices[:4]
        min_choices = input_choices[2:]
        file = open(name, "r")
        f = file.read()
        newline = f.count('\n') - 1
        file.close()

        new_wind = self.new_window()
        new_wind.parent.title(file_title)
        new_wind.mode_pacing()
        list = new_wind.parent.grid_slaves()

        file = open(name, "r")
        file.readline()
        pace_dist = ""
        time = ""
        for n in range(newline):
            split = file.readline()
            split = split[:-1]  # removes the newline character
            if n == 0:
                if split[3] == "m":
                    first_char_line_1 = split[0:3]
                else:
                    first_char_line_1 = split[0]

                #print(first_char_line_1)
            elif n == 1:
                if split[3] == "m":
                    first_char_line_2 = split[0:3]
                elif split[1] == "m":
                    first_char_line_2 = split[0]
                else:
                    first_char_line_2 = split[0:4]

                #print(first_char_line_2)
            if n == newline - 1:
                pattern = re.compile(':')
                result = pattern.search(split)

                for j in range(result.span()[0]):
                    pace_dist += split[j]
                for j in range(len(split)):
                    if j > result.span()[0] + 1:
                        time += split[j]
                #print(pace_dist)
                #print(time)
            pace = tk.Label(new_wind.parent, text=split)
            pace.grid(column=2)
        try:
            if int(first_char_line_2) - int(first_char_line_1) > 1:
                interval = str((int(first_char_line_2) - int(first_char_line_1))) + "m"
        except(ValueError):
            interval = "1mi"
        #print(pace_dist)
        for i, l in enumerate(list):
            if type(l) == tk.Entry:
                input_seconds = l
                #print("hello")
            elif type(l) == tk.Label and i == 1:
                seconds_label = l
                #print("yo")
            elif type(l) == tk.OptionMenu and i == 3:
                interval_option = l
                for k, dist in enumerate(report_choices):
                    if dist == interval:
                        interval_option.children["menu"].invoke(k)
                        #print(k)
            elif type(l) == tk.OptionMenu and i == 4:
                dist_option = l
                for k, dist in enumerate(input_choices):
                    if dist == pace_dist:
                        dist_option.children["menu"].invoke(k)
                        #print(k)
                #TODO make the invoke method not hard coded
            #print(i, type(l))
        list = new_wind.parent.grid_slaves()

        for i, l in enumerate(list):
            if type(l) == tk.Entry and i == 3:
                input_minutes = l

        time_min = ""
        time_sec = ""
        pattern = re.compile(':')
        result = pattern.search(time)
        # print(result)
        if result is None:
            try:
                input_seconds.insert("insert", time)
            except:
                input_seconds.delete(0, tk.END)
                input_seconds.insert("insert", "0")
        else:
            try:
                for j in range(result.span()[0]):
                    time_min += time[j]
                for j in range(len(time)):
                    if j > result.span()[0]:  # position of semicolon
                        time_sec += time[j]
                input_minutes.insert("insert", time_min)
                input_seconds.insert("insert", time_sec)
            except:
                input_minutes.delete(0, tk.END)
                input_minutes.insert("insert", "0")
                input_seconds.delete(0, tk.END)
                input_seconds.insert("insert", "0")
            #print(time_min)
            #print(time_sec)
            #print(input_minutes.get())
        file.close()
        new_wind.parent.minsize(width=400, height=200 + newline*20)

    def new_window(self):
        wind = tk.Tk()

        created_wind = Window(wind)
        wind.focus_force()
        return created_wind

    def open_window(self):
        list = self.parent.grid_slaves()
        button_cnt = 0
        entry_cnt = 0
        for l in list:
            if type(l) == tk.Button:
                button_cnt += 1
            elif type(l) == tk.Entry:
                entry_cnt += 1

        files = [('Text Document', '*.txt'), ('All Files', '*.*')]
        name = fd.askopenfilename(title="Open", filetypes=files)
        print(name)
        file = open(name, "r")
        primary_title = " - Running Calculator"
        file_title = os.path.basename(name)
        file_title += primary_title
        f = file.readline()

        if str(f) == "SPLIT MODE\n":
            self.open_split(file_title, file, name)
            print("1")
        elif str(f) == "CONVERT MODE\n":
            self.open_convert(file_title, file, name)
            print("2")
        elif str(f) == "PACE MODE\n":
            self.open_pace(file_title, name)

    def save_as(self, *args):
        files = [('Text Document', '*.txt'),
                 ('All Files', '*.*')]
        saveas = fd.asksaveasfile(filetypes=files, defaultextension=files)
        print(saveas.name)
        list = self.parent.grid_slaves()
        button_cnt = 0
        entry_cnt = 0
        for l in list:
            if type(l) == tk.Button:
                button_cnt += 1
            elif type(l) == tk.Entry:
                entry_cnt += 1

        if button_cnt == 3:
            self.read_split(saveas.name)
        elif entry_cnt > 2:
            self.read_convert(saveas.name)
        else:
            self.read_pace(saveas.name)

    def check_changes(self):
        # if anything has been changed since the file was last saved, detect a change
        # append an asterisk to the front of the window title

        # start with easily detectable changes -> harder
        name = ""

        # something with re.compile to find the spot in root.title before "-"

        # EASY: NUMBER OF WIDGETS MISMATCH
        file = open(name, "r")

        f = file.read()
        newline = f.count('\n')
        file.close()

        file = open(name, "r")
        non_button_widgets = 0
        for n in range(newline):
            non_button_widgets += 1

        if self.grid_slaves != non_button_widgets:
            self.title = "*" + self.title

        elif self.grid_slaves == non_button_widgets:
            pass
        else:
            pass  # no changes

        # HARD: Widget Modification

    # def new_window(*args):
    #     root_new = tk.Tk()
    #
    #     root_new.geometry('400x200')
    #
    #     root_new['bg'] = "#39cced"
    #     root_new.minsize(width=400, height=200)
    #     root_new.maxsize(width=400, height=200)
    #     root_new.title('Running Calculator')
    #     # image = tk.PhotoImage(file="Milkbot.png")
    #     # root.iconphoto(False, image)
    #     self.mode_split(root_new)
    #
    #     menubar = tk.Menu(root_new)
    #
    #     # create a pulldown menu, and add it to the menu bar
    #     filemenu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="File", menu=filemenu)
    #     filemenu.add_command(label="New" + "                 Ctrl+N", command=new_window)  # fd.open_file_dir
    #     filemenu.add_command(label="Open" + "               Ctrl+O", command=open_split)  # fd.open_file_dir
    #     filemenu.add_command(label="Save" + "                 Ctrl+S", command=save_as)  # fd.save_current_proj
    #     filemenu.add_command(label="Save as", command=save_as)  # fd.save_current_proj
    #     filemenu.add_separator()
    #     filemenu.add_command(label="Exit", command=quit)
    #
    #     optionsmenu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="Modes", menu=optionsmenu)
    #     optionsmenu.add_command(label="Split", command=mode_split)
    #     optionsmenu.add_command(label="Convert", command=mode_convert)
    #     optionsmenu.add_command(label="Pacing", command=mode_pacing)
    #
    #     aboutmenu = tk.Menu(menubar, tearoff=0)
    #     menubar.add_cascade(label="About", menu=aboutmenu)
    #     # aboutmenu.add_command(label="About the Creator",)
    #
    #     root_new.config(menu=menubar)
    #     root_new.bind("<Key>", event_root)
    #
    #     # def event_newfile():
    #     #     new_file()
    #     #     print('hello')
    #     # root.bind("<Control-c>", event_newfile)
    #
    #     root_new.mainloop()

    def new_file(self):
        list = self.grid_slaves()
        result = ""

        if self.title != "Running Calculator":  # check for changes have been made to entry by comparing to file
            # get file name from current path, can just look at the title

            # open file name

            # detecting changes to a saved file should be its own function

            file_name = self.title

        # print("Not in FOR")
        for l in list:
            print("Not in IF")
            print(type(l))
            if type(l) == tk.Entry:
                result += l.get()
                print(result)
            if result == "":
                self.del_split()
            elif self.title == "Running Calculator":  # not a loaded file
                # ask to save file file_dialog
                self.save_as()

                # if you get numerical values back, ask to save file as
                # if you have loaded a file and there have been changes to it, ask to save to file

    def quit(self):
        if mb.askyesno(title="Quit", message="Really quit?"):
            self.parent.destroy()

    def calc_avg(self):
        list = self.parent.grid_slaves()
        if (type(list[0]) == tk.Label):
            list[0].destroy()
            if len(list) > (num_buttons + 5):
                self.parent.minsize(width=400, height=self.parent.winfo_height() - 20)
            return 0
        avg_sec = 0.0
        avg_min = 0

        for l in list[:len(list) - num_buttons]:
            pattern = re.compile(':')
            result = pattern.search(l.get())
            # print(result)
            if result == None:
                try:
                    avg_sec += float(l.get())
                except:
                    l.delete(0, tk.END)
                    l.insert("insert", "0")
                    avg_sec += float(l.get())
            else:
                try:
                    min = ""
                    sec = ""
                    for j in range(result.span()[0]):
                        min += l.get()[j]
                    for j in range(len(l.get())):
                        if j > result.span()[0]:  # position of semicolon
                            sec += l.get()[j]
                    min = int(min)
                    sec = float(sec)
                    avg_min += min  # indices 0 to result.span()[0] (exclusive) are MINUTES indices
                    avg_sec += sec
                except:
                    l.delete(0, tk.END)
                    l.insert("insert", "0")
                    avg_sec += float(
                        l.get())  # indices result.span()[0] + 1 to l.get()[-1] (last index) are SECONDS indices
                    # print(result.span()[0]) #returns position of ':'
        if (avg_min > 1):
            avg_min = int(avg_min / (len(list) - num_buttons))

        avg_min = str(avg_min)
        avg_sec /= (len(list) - num_buttons)
        avg_sec = round(avg_sec, 2)  # truncates to two decimal places

        if avg_sec < 10:
            avg_sec = "0" + str(avg_sec)
        else:
            avg_sec = str(avg_sec)

        if avg_min == "0":
            title = "Average Pace: " + avg_sec
            avg_pace = tk.Label(self.parent, text=title)
            avg_pace.grid()
        else:
            avg_min = avg_min + ":" + avg_sec
            title = "Average Pace: " + avg_min
            avg_pace = tk.Label(self.parent, text=title)
            avg_pace.grid()
        if len(list) > (num_buttons + 5):
            self.parent.minsize(width=400, height=self.parent.winfo_height() + 20)
        return title

    def event_add_split(self, event):
        self.add_split()

    def event_del_split(self, event):
        self.del_split()

    def event_calc_avg(self, event):
        self.calc_avg()

    def event_root(self, event):  # https://web.archive.org/web/20190515021108id_/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
        list = self.parent.grid_slaves()
        print(event.char)
        print(event.keycode)
        # http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
        # if event.char == "+": #KP_Add, ie the plus symbol on the keypad
        #     query = "\+" #backslash so re doesn't interpret the "+" as a special char
        #     pattern = re.compile(query)
        #
        #     try:
        #         for l in list:
        #             result = pattern.search(l.get())
        #             if result != "None":
        #                 l.delete(-1)
        #         add_split()
        #     except:
        #         add_split()
        #
        # elif event.char == "-": #KP_Subtract, ie the minus symbol on the keypad
        #     query = "\+" #backslash so re doesn't interpret the "+" as a special char
        #     pattern = re.compile(query)
        #
        #     try:
        #         for l in list:
        #             result = pattern.search(l.get())
        #             if result != "None":
        #                 l.delete(-1)
        #         del_split()
        #     except:
        #         del_split()
        if event.keycode == 78:  # N
            self.new_file()
        elif event.keycode == 83:  # S
            self.save_as()
        elif event.keycode == 79:  # O
            self.open_split()

    def del_all(self):
        list = self.parent.grid_slaves()
        for l in list:
            list[0].destroy()
            list = self.parent.grid_slaves()

    def mode_split(self):
        self.del_all()
        self.parent.minsize(width=400, height=200)
        self.parent.maxsize(width=400, height=200)

        add = tk.Button(self.parent, text="Add", fg="black", command=self.add_split)
        add.bind("<Return>", self.event_add_split)
        add.grid(padx=180)

        delete = tk.Button(self.parent, text="Delete", fg="black", command=self.del_split)
        delete.bind("<Return>", self.event_del_split)
        delete.grid()

        calc = tk.Button(self.parent, text="Calculate Average", fg="black", command=self.calc_avg)
        calc.bind("<Return>", self.event_calc_avg)
        calc.grid()

    def mode_convert(self):
        self.del_all()
        self.parent.minsize(width=400, height=200)
        self.parent.maxsize(width=400, height=200)

        label_input = tk.Label(self.parent, text="Input:").grid(row=0, sticky="W")
        label_output = tk.Label(self.parent, text="Output:").grid(row=1, sticky="W")

        entry_input = tk.Entry(self.parent, width=10)
        entry_input.grid(row=0, column=1)

        dist_choices = ["200m", "1km"]
        input_option = tk.StringVar(self.parent)
        input_option.set("mi")

        input_menu = tk.OptionMenu(self.parent, input_option, "mi")
        input_menu.grid(row=0, column=2)

        input_minutes = tk.Entry(self.parent, width=10)
        input_minutes.grid(row=0, column=3)
        minutes_label = tk.Label(self.parent, text="m")
        minutes_label.grid(row=0, column=4)
        input_seconds = tk.Entry(self.parent, width=10)
        input_seconds.grid(row=0, column=5)
        seconds_label = tk.Label(self.parent, text="s")
        seconds_label.grid(row=0, column=6)

        output_minutes = tk.Entry(self.parent, width=10)
        output_minutes_label = tk.Label(self.parent, text="m")
        output_seconds = tk.Entry(self.parent, width=10)
        output_seconds.grid(row=1, column=5)
        output_seconds_label = tk.Label(self.parent, text="s")
        output_seconds_label.grid(row=1, column=6)
        output_option = tk.StringVar(self.parent)
        output_option.set("200m")

        output_menu = tk.OptionMenu(self.parent, output_option, *dist_choices)  # asterisk makes the choices vertical instead of horizontal
        output_menu.grid(row=1, column=2)

        def change_distance_dropdown(*args):
            if output_option.get() == "200m":

                output_minutes.grid_forget()
                output_minutes_label.grid_forget()
            else:
                output_minutes.grid(row=1, column=3)
                output_minutes_label.grid(row=1, column=4)

        output_option.trace("w", change_distance_dropdown)

        def convert(*args):
            input_unit = input_option.get()
            print(input_unit)
            output_unit = output_option.get()
            print(output_unit)

            try:
                if input_unit == "mi":
                    if output_unit == "1km":
                        output_minutes.delete(0, tk.END)
                        output_seconds.delete(0, tk.END)
                        tot_sec = float(input_seconds.get()) + float(input_minutes.get()) * 60
                        calc_secs = 1000 / (float(entry_input.get()) * 1609) * tot_sec
                        calc_mins = int(calc_secs / 60)
                        calc_secs = calc_secs % 60
                        calc_secs = round(calc_secs, 2)


                        output_minutes.insert("insert", calc_mins)
                        output_seconds.insert("insert", calc_secs)
                    elif output_unit == "200m":
                        output_minutes.delete(0, tk.END)
                        output_seconds.delete(0, tk.END)
                        tot_sec = float(input_seconds.get()) + float(input_minutes.get()) * 60
                        calc_secs = 200 / (float(entry_input.get()) * 1609) * tot_sec
                        calc_secs = round(calc_secs, 2)

                        output_seconds.insert("insert", calc_secs)
            except ValueError:
                entry_input.delete(0, tk.END)
                input_seconds.delete(0, tk.END)
                input_minutes.delete(0, tk.END)
                output_seconds.delete(0, tk.END)
                output_minutes.delete(0, tk.END)

                entry_input.insert("insert", "0")
                input_seconds.insert("insert", "0")
                input_minutes.insert("insert", "0")
                output_seconds.insert("insert", "0")
                output_minutes.insert("insert", "0")
            except ZeroDivisionError:
                output_seconds.insert("insert", "0")
                output_minutes.insert("insert", "0")

        conversion = tk.Button(self.parent, text="Convert", fg="black", command=convert)
        conversion.grid(row=2, column=2)

    def mode_pacing(self):
        self.del_all()
        self.parent.minsize(width=400, height=200)
        self.parent.maxsize(width=400, height=200)

        label_input = tk.Label(self.parent, text="Distance").grid(row=0, sticky="W")
        label_output = tk.Label(self.parent, text="Reporting Interval").grid(row=1, sticky="W")

        input_choices = ["200m", "400m", "800m", "1mi", "2mi", "3mi", "5k", "4mi", "5mi"]
        report_choices = input_choices[:4]
        min_choices = input_choices[2:]

        input_option = tk.StringVar(self.parent)
        input_option.set("200m")
        report_option = tk.StringVar(self.parent)
        report_option.set("200m")

        self.init_dropdown(self, "200m", input_option, "200m", report_option, input_choices, report_choices)

        input_seconds = tk.Entry(self.parent, width=10)
        input_seconds.grid(row=0, column=4)
        seconds_label = tk.Label(self.parent, text="s")
        seconds_label.grid(row=0, column=5)
        input_minutes = tk.Entry(self.parent, width=10)
        minutes_label = tk.Label(self.parent, text="m")

        def change_distance_dropdown(*args):
            if any(input_option.get() in i for i in min_choices):

                input_seconds.grid_forget()
                seconds_label.grid_forget()
                input_minutes.grid(row=0, column=2)
                minutes_label.grid(row=0, column=3)
                input_seconds.grid(row=0, column=4)
                seconds_label.grid(row=0, column=5)
            else:
                input_minutes.grid_forget()
                minutes_label.grid_forget()
                input_seconds.grid(row=0, column=4)
                seconds_label.grid(row=0, column=5)
            input_minutes.delete(0, tk.END)
            input_seconds.delete(0, tk.END)
            clear_splits()

        def clear_splits(*args):
            list = self.parent.grid_slaves()
            for j in range(len(list)):
                if type(list[j]) == tk.Label:
                    pattern = re.compile(':')
                    result = pattern.search(list[j]["text"])
                    if result != None:
                        list[j].destroy()

        input_option.trace("w", change_distance_dropdown)
        report_option.trace("w", clear_splits)

        def pace_splits(i, j):
            if 3 <= i <= 5:
                dist = 1609 * (i - 2)
            elif i == 6:
                dist = 5000
            elif 7 <= i <= 8:
                dist = 1609 * (i - 3)
            else:
                dist = 2 ** i * 200

            if j == 3:
                report_interval = 1609
            else:
                report_interval = 2 ** (j) * 200

            num_splits = int(dist / report_interval)
            approx_dist = num_splits * report_interval

            min = int(input_minutes.get())
            sec = float(input_seconds.get())
            total_sec = min * 60 + sec
            approx_total_sec = total_sec * approx_dist / dist

            split_sec = approx_total_sec / num_splits
            split_min = int(split_sec / 60)
            split_sec = split_sec % 60
            split_sec = round(split_sec, 2)

            for split in range(num_splits):
                if split != 0:
                    s = split_sec * (split + 1)
                    m = split_min * (split + 1)

                    total_sec = m * 60 + s

                    min = int(total_sec / 60)
                    sec = round(total_sec % 60, 2)

                    if j != 3:
                        if sec < 10:
                            tk.Label(self.parent, text="{}m: {}:0{}".format(report_interval * (split + 1), min, sec)).grid(
                                row=3 + split, column=2)
                        else:
                            tk.Label(self.parent, text="{}m: {}:{}".format(report_interval * (split + 1), min, sec)).grid(
                                row=3 + split, column=2)
                    else:
                        if sec < 10:
                            tk.Label(self.parent, text="{}mi: {}:0{}".format(split + 1, min, sec)).grid(row=3 + split, column=2)
                        else:
                            tk.Label(self.parent, text="{}mi: {}:{}".format(split + 1, min, sec)).grid(row=3 + split, column=2)
                else:
                    if j != 3:
                        if split_sec < 10:
                            tk.Label(self.parent,text="{}m: {}:0{}".format(report_interval * (split + 1), split_min, split_sec)).grid(row=3 + split, column=2)
                        else:
                            tk.Label(self.parent, text="{}m: {}:{}".format(report_interval * (split + 1), split_min, split_sec)).grid( row=3 + split, column=2)
                    else:
                        if split_sec < 10:
                            tk.Label(self.parent, text="{}mi: {}:0{}".format(split + 1, split_min, split_sec)).grid(row=3 + split, column=2)
                        else:
                            tk.Label(self.parent, text="{}mi: {}:{}".format(split + 1, split_min, split_sec)).grid(
                                row=3 + split,
                                column=2)

            if j != 0 and dist == 5000:
                if float(input_seconds.get()) < 10:
                    tk.Label(self.parent, text="5000m: {}:0{}".format(input_minutes.get(), float(input_seconds.get()))).grid(
                        row=3 + (split + 1), column=2)
                else:
                    tk.Label(self.parent, text="5000m: {}:{}".format(input_minutes.get(), float(input_seconds.get()))).grid(
                        row=3 + (split + 1), column=2)

            elif j != 3 and (dist % 1609 == 0):
                if float(input_seconds.get()) < 10:
                    tk.Label(self.parent, text="{}mi: {}:0{}".format(round(dist / 1609), input_minutes.get(),
                                                              float(input_seconds.get()))).grid(row=3 + (split + 1),
                                                                                                column=2)
                else:
                    tk.Label(self.parent, text="{}mi: {}:{}".format(round(dist / 1609), input_minutes.get(),
                                                             float(input_seconds.get()))).grid(row=3 + (split + 1),
                                                                                               column=2)

            if i == 8 and j == 0:
                self.parent.minsize(width=400, height=950)
            else:
                self.parent.minsize(width=400, height=200 + (num_splits - 3) * 20)

        def pacing():
            try:
                input_dist = input_option.get()
                report_dist = report_option.get()

                for i, dist in enumerate(input_choices):
                    if input_dist == dist:
                        break
                for j, dist in enumerate(input_choices):
                    if report_dist == dist:
                        break

                print("this is i:", i)
                print("this is j:", j)

                if i < j:
                    report_option.set(input_choices[i])
                    pace_splits(i, j)
                else:
                    pace_splits(i, j)

            except ValueError:

                input_seconds.delete(0, tk.END)
                input_minutes.delete(0, tk.END)

                input_seconds.insert("insert", "0")
                input_minutes.insert("insert", "0")
            return [i, j]
        pace = tk.Button(self.parent, text="Get Splits!", fg="black", command=pacing)
        pace.grid(row=2, column=2)

    def init_dropdown(self, new_wind, input_str, input_option, report_str, report_option, input_choices, report_choices):
        input_option.set(input_str)
        input_menu = tk.OptionMenu(new_wind.parent, input_option, *input_choices)
        input_menu.grid(row=0, column=1)

        report_option.set(report_str)
        report_menu = tk.OptionMenu(new_wind.parent, report_option, *report_choices)  # asterisk makes the choices vertical instead of horizontal
        report_menu.grid(row=1, column=1)

root = tk.Tk()
w1=Window(root)
w1.mainloop()

#TODO - HIGH TO LOW PRIORITY

#DO NOT IMPACT FUNCTIONALITY OF PROGRAM
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

#TODO - Upper left icon and taskbar icon
#TODO - when you save a file, the title of the window should update to the name you named the file
#TODO - Keyboard shortcuts (Ctrl+O OPEN, Ctrl+S SAVE, enter - Calculate Average)