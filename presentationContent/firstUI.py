import tkinter as tk
from tkinter import ttk

def increment_count():
    pass

def decrement_count():
    pass

# Create Tkinter window
root = tk.Tk()
root.title("People Counter")
root.configure(bg='#ffffff')

# Set window size and center the window
window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Create styled frame
frame = ttk.Frame(root, padding="20", style='TFrame')
frame.pack(expand=True)

# Create and configure the label
count_label = ttk.Label(frame, text="Total people in view: 0", font=("Arial", 20), style='TLabel')
count_label.grid(row=0, column=0, columnspan=2, pady=20)

# Create and configure the increment button
increment_button = ttk.Button(frame, text="Increment", command=increment_count, style='TButton', width=15)
increment_button.grid(row=1, column=0, padx=10, pady=10)

# Create and configure the decrement button
decrement_button = ttk.Button(frame, text="Decrement", command=decrement_count, style='TButton', width=15)
decrement_button.grid(row=1, column=1, padx=10, pady=10)

# Define custom styles for the frame, label, and buttons
style = ttk.Style()

style.configure('TFrame', background='#ffffff')
style.configure('TLabel', background='#ffffff', foreground='#ff0000')
style.configure('TButton', font=('Arial', 16), background='#ff0000', foreground='white', borderwidth=0, focuscolor='#ff0000', focusfill='#ff0000', focusthickness=3)
style.map('TButton', background=[('active', '#cc0000')], focuscolor=[('!active', '#ff0000')])

root.mainloop()
