import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageTk

# Global variables for dragging and resizing
drag_start_x = 0
drag_start_y = 0
image_start_x = 0
image_start_y = 0
resizing = False
image_width = 400
image_height = 600

# Function to update the preview based on user input
def update_preview(*args):
    # Get the input from the text box
    input_text = text_input.get("1.0", tk.END).strip()
    
    # Get the font size from the slider
    font_size = size_slider.get()
    
    # Get the selected color from the color variable
    color = color_var.get()
    
    # Get the selected background color if the option is selected
    if bg_var.get():  # If background option is selected
        bg_color = bg_color_var.get()
        preview_label.config(bg=bg_color)  # Set background color
    else:
        bg_color = "white"  # Default background color
        preview_label.config(bg=bg_color)  # Set default background color

    # Get the selected font style from the dropdown
    font_style = font_style_var.get()

    # Update the preview label with current styles and input text
    preview_label.config(text=input_text, font=(font_style, int(font_size)), fg=color)

# Function to open a color chooser dialog for text color
def choose_color():
    color_code = colorchooser.askcolor(title="Choose text color")[1]
    if color_code:
        color_var.set(color_code)
        color_button.config(bg=color_code)
        update_preview()

# Function to open a color chooser dialog for background color
def choose_bg_color():
    color_code = colorchooser.askcolor(title="Choose background color")[1]
    if color_code:
        bg_color_var.set(color_code)
        bg_color_button.config(bg=color_code)
        update_preview()

# Function to open a file dialog and set the background image
def choose_background_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        load_background_image(file_path)

# Function to load and display the selected background image
def load_background_image(file_path):
    global background_photo
    background_label.image_path = file_path
    background_image = Image.open(file_path)
    background_image = background_image.resize((image_width, image_height), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)

# Dragging functionality for text
def start_drag(event):
    global drag_start_x, drag_start_y
    drag_start_x = event.x
    drag_start_y = event.y

def drag(event):
    x = preview_label.winfo_x() + event.x - drag_start_x
    y = preview_label.winfo_y() + event.y - drag_start_y
    preview_label.place(x=x, y=y)

# Dragging functionality for image
def start_image_drag(event):
    global image_start_x, image_start_y
    image_start_x = event.x
    image_start_y = event.y

def drag_image(event):
    if not resizing:
        x = background_label.winfo_x() + event.x - image_start_x
        y = background_label.winfo_y() + event.y - image_start_y
        background_label.place(x=x, y=y)

# Resizing functionality
def start_resize(event):
    global resizing
    resizing = True
    background_label.bind("<B1-Motion>", resize_image)

def resize_image(event):
    global image_width, image_height
    new_width = max(10, event.x)
    new_height = max(10, event.y)

    background_image = Image.open(background_label.image_path)
    resized_image = background_image.resize((new_width, new_height), Image.LANCZOS)
    global background_photo
    background_photo = ImageTk.PhotoImage(resized_image)
    background_label.config(image=background_photo)
    background_label.image_width = new_width
    background_label.image_height = new_height

def stop_resize(event):
    global resizing
    resizing = False
    background_label.unbind("<B1-Motion>")

# Function to save the preview as an image
def save_preview():
    canvas = tk.Canvas(preview_frame, width=image_width, height=image_height)
    canvas.pack()

    if hasattr(background_label, 'image_path'):
        background_image = Image.open(background_label.image_path)
        background_image = background_image.resize((image_width, image_height), Image.LANCZOS)
        canvas_image = ImageTk.PhotoImage(background_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas_image)

    input_text = text_input.get("1.0", tk.END).strip()
    font_size = size_slider.get()
    color = color_var.get()
    font_style = font_style_var.get()
    
    if bg_var.get():
        bg_color = bg_color_var.get()
        canvas.create_rectangle(0, 0, image_width, image_height, fill=bg_color, outline=bg_color)  # Draw background rectangle

    canvas.create_text(20, 20, anchor="nw", text=input_text, font=(font_style, font_size), fill=color)

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"),
                                                          ("JPEG files", "*.jpg"),
                                                          ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path + ".eps")
        img = Image.open(file_path + ".eps")
        img.save(file_path)
        messagebox.showinfo("Success", "Preview saved successfully!")

# Create the main window
root = tk.Tk()
root.title("Live Text Styling with Background Image")
root.geometry("900x600")

# Create the left frame for inputs
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

# Text input widget
tk.Label(input_frame, text="Enter Text:").pack(anchor="w")
text_input = tk.Text(input_frame, height=5, width=30)
text_input.pack(pady=10)

# Update preview when the user types
text_input.bind("<KeyRelease>", update_preview)

# Font size slider
tk.Label(input_frame, text="Font Size:").pack(anchor="w")
size_slider = tk.Scale(input_frame, from_=10, to=72, orient=tk.HORIZONTAL)
size_slider.set(20)  # Default size
size_slider.pack(pady=10)
size_slider.bind("<Motion>", update_preview)

# Display current font size
size_label = tk.Label(input_frame, text=f"Current Size: {size_slider.get()}")
size_label.pack(anchor="w")

# Update size label when the slider is moved
def update_size_label(event):
    size_label.config(text=f"Current Size: {size_slider.get()}")
    update_preview()
def reset():
    text_input.delete("1.0", tk.END)  # Clear the text input
    size_slider.set(20)  # Reset font size to default
    color_var.set("black")  # Reset text color to black
    bg_color_var.set("white")  # Reset background color to white
    bg_var.set(False)  # Uncheck the background color option
    font_style_var.set("Arial")  # Reset font style to Arial
    color_button.config(bg="black")  # Update color button
    bg_color_button.config(bg="white")  # Update background color button
    preview_label.config(text="Your text will appear here.", font=("Arial", 20), fg="black", bg="SystemButtonFace")  # Reset preview

size_slider.bind("<Motion>", update_size_label)

# Font color picker
tk.Label(input_frame, text="Font Color:").pack(anchor="w")
color_var = tk.StringVar(value="black")
color_button = tk.Button(input_frame, text="Choose Text Color", bg="black", command=choose_color)
color_button.pack(pady=10)

# Background color option
bg_var = tk.BooleanVar(value=False)  # Checkbox variable
bg_checkbox = tk.Checkbutton(input_frame, text="Enable Background Color", variable=bg_var, command=update_preview)
bg_checkbox.pack(anchor="w", pady=5)

# Background color picker
bg_color_var = tk.StringVar(value="white")  # Default background color
bg_color_button = tk.Button(input_frame, text="Choose Background Color", bg="white", command=choose_bg_color)
bg_color_button.pack(pady=10)

# Font style dropdown
tk.Label(input_frame, text="Font Style:").pack(anchor="w")
font_style_var = tk.StringVar(value="Arial")  # Default font
font_style_dropdown = ttk.Combobox(input_frame, textvariable=font_style_var)
font_style_dropdown['values'] = ('Arial', 'Courier', 'Helvetica', 'Times', 'Comic Sans MS')
font_style_dropdown.current(0)  # Set default font to Arial
font_style_dropdown.pack(pady=10)
font_style_dropdown.bind("<<ComboboxSelected>>", update_preview)

# Button to choose background image
bg_button = tk.Button(input_frame, text="Choose Background Image", command=choose_background_image)
bg_button.pack(pady=10)

# Button to save the preview
save_button = tk.Button(input_frame, text="Save Preview", command=save_preview)
save_button.pack(pady=10)

# Create the right frame for the live preview
preview_frame = tk.Frame(root)
preview_frame.pack(side=tk.RIGHT, padx=20, pady=20, expand=True, fill=tk.BOTH)

# Label for background image
background_label = tk.Label(preview_frame)
background_label.pack(fill=tk.BOTH, expand=True)

# Label for live preview with text wrapping
preview_label = tk.Label(preview_frame, text="Your text will appear here.", font=("Arial", 20), anchor="nw", justify="left")
preview_label.place(x=20, y=20)  # Set initial position
preview_label.pack_propagate(False)

# Bind mouse events for dragging the text
preview_label.bind("<Button-1>", start_drag)
preview_label.bind("<B1-Motion>", drag)

# Bind mouse events for dragging the background image
background_label.bind("<Button-1>", start_image_drag)
background_label.bind("<B1-Motion>", drag_image)  # Mouse dragged while button is pressed
background_label.bind("<Button-3>", start_resize)  # Right-click to start resizing
root.bind("<ButtonRelease-1>", stop_resize)  # Release mouse button to stop resizing
reset_button = tk.Button(input_frame, text="Reset", command=reset)
reset_button.pack(pady=10)

# Start the main loop
root.mainloop()
