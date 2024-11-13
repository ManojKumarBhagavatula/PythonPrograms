import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from PIL import ImageGrab, Image, ImageTk


class TimetableMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Activity Timetable Maker")

      
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_pane = tk.Frame(self.main_frame, width=200, bg="#f0f0f0", padx=10, pady=10)
        self.left_pane.pack(side=tk.LEFT, fill=tk.Y)

        self.right_pane = tk.Frame(self.main_frame, padx=10, pady=10)
        self.right_pane.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        
        self.default_data = [
            ["Time/Day", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["", "", "", "", "", ""]
        ]
        self.current_data = [row[:] for row in self.default_data]
        
        self.history = []  

        self.create_timetable_grid()

        
        self.add_row_button = tk.Button(self.left_pane, text="Add Row", command=self.add_row)
        self.add_row_button.pack(pady=5, fill=tk.X)

        self.remove_row_button = tk.Button(self.left_pane, text="Remove Row", command=self.remove_row)
        self.remove_row_button.pack(pady=5, fill=tk.X)

        self.add_column_button = tk.Button(self.left_pane, text="Add Column", command=self.add_column)
        self.add_column_button.pack(pady=5, fill=tk.X)

        self.remove_column_button = tk.Button(self.left_pane, text="Remove Column", command=self.remove_column)
        self.remove_column_button.pack(pady=5, fill=tk.X)

        self.revert_button = tk.Button(self.left_pane, text="Revert", command=self.revert_changes)
        self.revert_button.pack(pady=5, fill=tk.X)

        self.reset_button = tk.Button(self.left_pane, text="Reset", command=self.reset_timetable)
        self.reset_button.pack(pady=5, fill=tk.X)

        self.color_button = tk.Button(self.left_pane, text="Pick Color", command=self.pick_color)
        self.color_button.pack(pady=5, fill=tk.X)

        
        self.save_table_button = tk.Button(self.left_pane, text="Save Table as PNG", command=self.save_table_as_png)
        self.save_table_button.pack(pady=5, fill=tk.X)

        self.selected_cell = None  

    def create_timetable_grid(self):
       
        self.entries = []  
        self.refresh_grid()

    def refresh_grid(self):
      
        for widget in self.right_pane.grid_slaves():
            widget.grid_forget()

        self.entries.clear() 

        for row_idx, row_data in enumerate(self.current_data):
            row_entries = []
            for col_idx, cell_data in enumerate(row_data):
                entry = tk.Entry(self.right_pane, width=20, justify='center', font=('Arial', 12),
                                 relief='flat', borderwidth=1) 
                entry.grid(row=row_idx, column=col_idx, padx=1, pady=1)  
                entry.insert(tk.END, cell_data)
                entry.config(font=('Helvetica', 10, 'bold'))

                
                if row_idx == 0 or col_idx == 0:
                    entry.config(bg='#d1e7fd') 

                
                entry.bind("<Button-1>", lambda e, row=row_idx, col=col_idx: self.select_cell(row, col))
                row_entries.append(entry)
            self.entries.append(row_entries)

    def select_cell(self, row, col):
       
        self.selected_cell = (row, col)

    def pick_color(self):
       
        if self.selected_cell:
            color = colorchooser.askcolor(title="Choose a color")
            if color[1]: 
                row, col = self.selected_cell
                self.entries[row][col].config(bg=color[1])  
        else:
            messagebox.showinfo("Info", "Select a cell first to pick a color.")

    def update_current_data(self):
        
        self.current_data = [[entry.get() for entry in row] for row in self.entries]

    def add_row(self):
        
        self.save_state()  
        new_row = [""] * len(self.current_data[0])  
        self.current_data.append(new_row)
        self.refresh_grid()

    def remove_row(self):
       
        if len(self.current_data) > 2:  
            self.save_state() 
            self.current_data.pop()
            self.refresh_grid()
        else:
            messagebox.showinfo("Info", "You can't remove all rows.")

    def add_column(self):
       
        self.save_state()  
        for row in self.current_data:
            row.append("")  
        self.refresh_grid()

    def remove_column(self):
        if len(self.current_data[0]) > 2:  
            self.save_state() 
            for row in self.current_data:
                row.pop()
            self.refresh_grid()
        else:
            messagebox.showinfo("Info", "You can't remove all columns.")

    def save_state(self):
        self.history.append([row[:] for row in self.current_data])

    def revert_changes(self):
        if self.history:
            self.current_data = self.history.pop()  
            self.refresh_grid()
        else:
            messagebox.showinfo("Info", "No changes to revert.")

    def reset_timetable(self):
        self.current_data = [row[:] for row in self.default_data]
        self.refresh_grid()



    def save_table_as_png(self):
   
        self.update_current_data()

        x = self.right_pane.winfo_rootx()
        y = self.right_pane.winfo_rooty()
        width = self.right_pane.winfo_width()
        height = self.right_pane.winfo_height()

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")],
                                                title="Save Table As")
        if file_path:
            ImageGrab.grab(bbox=(x, y, x + width, y + height)).save(file_path)
            messagebox.showinfo("Saved", f"Table saved as {file_path}")

# ... (Rest of the code)
    def upload_image(self):
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                self.image = Image.open(file_path)
                self.photo = ImageTk.PhotoImage(self.image)
                self.canvas = tk.Canvas(self.right_pane, width=self.image.width, height=self.image.height)
                self.canvas.pack()
                self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
                self.canvas.bind("<Button-1>", self.modify_image)

    def modify_image(self, event):
        x, y = event.x, event.y
        cell_x = x // self.image.width
        cell_y = y // self.image.height
        self.image.putpixel((cell_x, cell_y), (255, 0, 0))  
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')



if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableMaker(root)
    root.mainloop()
