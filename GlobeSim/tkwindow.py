from math import *

import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

class EntryWindow():
    def __init__(self, master, item:str, min:int, max:int):
        self.master = master
        self.min = min
        self.max = max
        self.out = -1

        master.title("GlobeSim - Set " + item)
        master.bind("<Escape>", lambda event: master.destroy())
        master.bind("<Return>", lambda event: self.add())

        self.label = tk.Label(master, text = item + ":")
        self.label.grid(row=0, column=0)

        self.warning = tk.Label(master, text="")
        self.warning.grid(row=1, column=1)

        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1)
        self.entry.focus()

        self.btn1 = tk.Button(master, text="Confirm", command=self.add)
        self.btn1.grid(row=0, column=2)

        self.btn2 = tk.Button(master, text="Randomize", command=self._rand)
        self.btn2.grid(row=0, column=3)

    def add(self, event=None):
        try:
            out = int(self.entry.get())
            if out >= self.min and out <= self.max:
                self.out = out
                self.master.destroy()
            else:
                self.warning.config(text="Input must be between "+str(self.min)+" and "+str(self.max))
        except:
            self.warning.config(text="Input must be an integer.")

    def _rand(self, event=None):
        self.entry.delete(0,tk.END)
        self.entry.insert(0,random.randint(self.min, self.max))

class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
 
        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, 
                                width = 200, height = 300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command = self.canvas.yview)
 
        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
 
        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
    
    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
         
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

class MovementTableWindow():
    def __init__(self, master, plate, data):
        self.master = master
        self.plate = plate
        self.data = data
        self.initialized = False
        master.title("GlobeSim - Plate " + str(plate) + " Data")
        master.bind("<Escape>", lambda event: master.destroy())

        self.main_frame = VerticalScrolledFrame(master)
        self.main_frame.bind('<Configure>', self._configure_cells)
        self.main_frame.pack(expand = True, fill = tk.BOTH)

        self.cells = []
        self.cells.append(tk.Button(self.main_frame.interior, text="Time (my)", width=16))
        self.cells.append(tk.Button(self.main_frame.interior, text="Pole x", width=16))
        self.cells.append(tk.Button(self.main_frame.interior, text="Pole y", width=16))
        self.cells.append(tk.Button(self.main_frame.interior, text="Pole z", width=16))
        self.cells.append(tk.Button(self.main_frame.interior, text="Speed", width=16))
        for a in range(len(data[0])):
            for b in range(5):
                self._new_cell(-1)
            self.cells[-5].insert(0,data[0][a])
            self.cells[-4].insert(0,data[1][a][0])
            self.cells[-3].insert(0,data[1][a][1])
            self.cells[-2].insert(0,data[1][a][2])
            self.cells[-1].insert(0,data[2][a])
        self._reload_cells()

        self.button_frame = tk.Frame(master)
        self.btn1 = tk.Button(self.button_frame, text="New Row", command=lambda: self._new_row('Button'))
        self.btn1.grid(row=0,column=0, padx=4)
        self.btn2 = tk.Button(self.button_frame, text="Delete Row", command=self._delete_row)
        self.btn2.grid(row=0,column=1, padx=4)
        self.btn3 = tk.Button(self.button_frame, text="Import", command=self.load_file)
        self.btn3.grid(row=0,column=2, padx=4)
        self.btn4 = tk.Button(self.button_frame, text="Export", command=self.save_file)
        self.btn4.grid(row=0,column=3, padx=4)
        self.btn5 = tk.Button(self.button_frame, text="Save Changes", command=self.save_changes)
        self.btn5.grid(row=0,column=4, padx=4)
        self.btn6 = tk.Button(self.button_frame, text="Close", command=master.destroy)
        self.btn6.grid(row=0,column=5, padx=4)
        self.button_frame.pack(pady=5)

    def _debug_print(self, event=None):
        out = ""
        for row in range(len(self.cells) // 5 - 1):
            out += " ".join((self.cells[row*5+5].get(), self.cells[row*5+6].get(), self.cells[row*5+7].get())) + "\n"
        print(out)

    def _configure_cells(self, event=None):
        if not self.initialized:
            self.initialized = True
            return
        for cell in self.cells:
            if type(cell).__name__ == 'Button':
                cell.config(width = self.main_frame.canvas.winfo_width() * 2 // 73)
            else:
                cell.config(width = self.main_frame.canvas.winfo_width() // 30)
    
    def _reload_cells(self, start=0):
        for a in range(start, len(self.cells)):
            self.cells[a].forget()
            self.cells[a].grid(row=a//5, column=a%5)

    def _get_focus(self):
        if self.main_frame.focus_get() == self.master:
            return -1
        else:
            return self.cells.index(self.main_frame.focus_get())

    def _up_row(self, event=None):
        focus = self._get_focus()
        if focus >= 10:
            self.cells[focus - 5].focus_set()

    def _down_row(self, event=None):
        focus = self._get_focus()
        if focus != -1 and focus + 5 < len(self.cells):
            self.cells[focus + 5].focus_set()
    
    def _left_row(self, event=None):
        focus = self._get_focus()
        if focus > 5 and self.cells[focus].index(tk.INSERT) == 0:
            self.cells[focus - 1].focus_set()

    def _right_row(self, event=None):
        focus = self._get_focus()
        if focus + 1 < len(self.cells) and self.cells[focus].index(tk.INSERT) == len(self.cells[focus].get()):
            self.cells[focus + 1].focus_set()
            self.cells[focus + 1].icursor(0)

    def _new_cell(self, index):
        if index == -1:
            self.cells.append(tk.Entry(self.main_frame.interior))
        else:
            self.cells.insert(index, tk.Entry(self.main_frame.interior))
        cell = self.cells[index]
        cell.bind("x", self._delete_row)
        cell.bind("<Return>", self._new_row)
        cell.bind("<Up>", self._up_row)
        cell.bind("<Down>", self._down_row)
        cell.bind("<Left>", self._left_row)
        cell.bind("<Right>", self._right_row)

    def _new_row(self, event=None):
        focus = self._get_focus()
        if focus != -1:
            a = focus//5*5 + 5
            for i in range(5):
                self._new_cell(a)
            self._reload_cells(a-10)
            self._configure_cells()
            self.cells[focus + 5].focus_set()
        elif event == 'Button':
            for i in range(5):
                self._new_cell(-1)
            self._reload_cells(len(self.cells) - 5)
            self._configure_cells()

    def _delete_row(self, event=None):
        focus = self._get_focus()
        if focus != -1:
            for i in range(5):
                self.cells[focus//5*5].destroy()
                del self.cells[focus//5*5]
            if focus < len(self.cells):
                self.cells[focus].focus_set()
            elif focus - 5 > 4:
                self.cells[focus - 5].focus_set()

    def _normalize(self, v:tuple):
        l = sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
        return (v[0]/l, v[1]/l, v[2]/l)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", ("*.txt")), ("All files", "*.*")])

        if file_path:
            content = ""
            try:
                for row in range(1, len(self.cells) // 5):
                    for col in range(5):
                        content += str(float(self.cells[row*5 + col].get())) + " "
                    content += "\n"
            except ValueError:
                messagebox.showerror("GlobeSim - Parse Error", f"Error parsing data on line {row}: Value must be an integer or float.")
                print(f"Error parsing data on line {row}: Value must be an integer or float")
                return
            except Exception as e:
                messagebox.showerror("GlobeSim - Parse Error", f"Error parsing data: {e}")
                print(f"Error parsing data: {e}")
                return

            try:
                with open(file_path, 'w') as file:
                    file.write(content)
                    print(f"File saved successfully at: {file_path}")
            except Exception as e:
                messagebox.showerror("GlobeSim - Export Error", f"Error saving file: {e}")
                print(f"Error saving file: {e}")

    def load_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text File", ("*.txt")), ("All files", "*.*")])
        
        if file_path:
            try:
                while type(self.cells[-1]).__name__ == "Entry":
                    self.cells[-1].destroy()
                    del self.cells[-1]

                with open(file_path, 'r') as file:
                    content = file.readlines()
                    for line in content:
                        for b in line.split():
                            self._new_cell(-1)
                            self.cells[-1].insert(0,b)
                    file.close()
                    
                self._reload_cells()

                print(f"File loaded successfully from: {file_path}")
            except Exception as e:
                messagebox.showerror("GlobeSim - Import Error", f"Error loading file: {e}")
                print(f"Error loading file: {e}")

    def save_changes(self):
        self.data = [[],[],[]]
        try:
            for row in range(1, len(self.cells) // 5):
                self.data[0].append(int(float(self.cells[row*5].get())))    # append time
                self.data[1].append(self._normalize((float(self.cells[row*5+1].get()), float(self.cells[row*5+2].get()), float(self.cells[row*5+3].get())))) # append pole
                self.data[2].append(float(self.cells[row*5+4].get()))    # append speed
        except ValueError:
            messagebox.showerror("GlobeSim - Parse Error", f"Error parsing data on line {row}: Value must be an integer or float.")
            print(f"Error parsing data on line {row}: Value must be an integer or float")
        except Exception as e:
            messagebox.showerror("GlobeSim - Export Error", f"Error saving file: {e}")
            print(f"Error saving data: {e}")