import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import meghivogato_main as main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Application(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Program Runner")
        self.geometry("600x400")
        
        self.create_menu()
        
        self.plot_tab = ttk.Frame(self)
        self.plot_tab.pack(fill="both", expand=True)

        self.create_plot_tab()
        
    def create_menu(self):
        menubar = tk.Menu(self)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Run", command=self.run_program)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)
        
        menubar.add_cascade(label="File", menu=file_menu)
        
        self.config(menu=menubar)
        
    def create_plot_tab(self):
        self.plot_frame = tk.Frame(self.plot_tab)
        self.plot_frame.pack(fill="both", expand=True)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run_program(self):
        try:
            main.main()
            messagebox.showinfo("Success", "Program executed successfully.")
            self.show_plot()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_plot(self):
        # Assuming you have data to plot, replace this with your actual plotting code
        X = np.random.rand(100, 2)  # Sample data for demonstration
        yhat = np.random.randint(0, 3, size=100)  # Sample cluster labels
        clusters = np.unique(yhat)
        
        self.subplot.clear()
        

if __name__ == "__main__":
    app = Application()
    app.mainloop()


# border_effects = {
#     "flat": tk.FLAT,
#     "sunken": tk.SUNKEN,
#     "raised": tk.RAISED,
#     "groove": tk.GROOVE,
#     "ridge": tk.RIDGE,
# }

# def button_click():
#     label.config(text="Button clicked! Text entered: " + entry.get())
#     text_output.insert(tk.END, entry.get() + "\n")

# # Create the main window
# window = tk.Tk()

# # Set the title of the window
# window.title("My Tkinter Window")

# # Set the size of the window
# window.geometry("400x300")

# # Create a frame to contain the grid of frames and labels
# grid_frame = tk.Frame(window)
# grid_frame.pack()

# # Create a grid of frames with labels inside
# for i in range(3):
#     for j in range(3):
#         frame = tk.Frame(
#             master=grid_frame,
#             relief=tk.RAISED,
#             borderwidth=1
#         )
#         frame.grid(row=i, column=j, padx=5, pady=5)
#         label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
#         label.pack()

# # Create a frame
# frame = tk.Frame(window, relief=tk.RIDGE, borderwidth=2)
# frame.pack(fill=tk.BOTH, expand=True)

# # Add a label to the frame with custom foreground and background colors
# label = tk.Label(frame, text="Hello, Tkinter!", 
#     foreground="white",  # Set the text color to white
#     background="black"  # Set the background color to black
#     )
# label.pack()

# # Add an entry widget to the frame
# entry = tk.Entry(frame)
# entry.pack()

# # Add a button to the frame
# button = tk.Button(frame, text="Click Me!", command=button_click)
# button.pack()

# # Add a textbox to the frame
# text_output = tk.Text(frame)
# text_output.pack()

# # Run the Tkinter event loop
# window.mainloop()

# #####################################################################################
# #####################################################################################
# # Function to handle the Submit button click event
# def submit():
#     # Get the values entered in the entry widgets
#     first_name = ent_first_name.get()
#     last_name = ent_last_name.get()
#     address1 = ent_address1.get()
#     address2 = ent_address2.get()
#     city = ent_city.get()
#     state = ent_state.get()
#     postal_code = ent_postal_code.get()
#     country = ent_country.get()
    
#     # Display the entered values in the text box
#     text_output.delete("1.0", tk.END)
#     text_output.insert(tk.END, f"First Name: {first_name}\n")
#     text_output.insert(tk.END, f"Last Name: {last_name}\n")
#     text_output.insert(tk.END, f"Address Line 1: {address1}\n")
#     text_output.insert(tk.END, f"Address Line 2: {address2}\n")
#     text_output.insert(tk.END, f"City: {city}\n")
#     text_output.insert(tk.END, f"State/Province: {state}\n")
#     text_output.insert(tk.END, f"Postal Code: {postal_code}\n")
#     text_output.insert(tk.END, f"Country: {country}\n\n")

# # Function to handle the Clear button click event
# def clear():
#     # Clear the entry widgets and the text box
#     ent_first_name.delete(0, tk.END)
#     ent_last_name.delete(0, tk.END)
#     ent_address1.delete(0, tk.END)
#     ent_address2.delete(0, tk.END)
#     ent_city.delete(0, tk.END)
#     ent_state.delete(0, tk.END)
#     ent_postal_code.delete(0, tk.END)
#     ent_country.delete(0, tk.END)
#     text_output.delete("1.0", tk.END)

# # Create the main window
# window = tk.Tk()
# window.title("Address Entry Form")

# # Create a new frame `frm_form` to contain the Label
# # and Entry widgets for entering address information
# frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# frm_form.pack()

# # Create the Label and Entry widgets for "First Name"
# lbl_first_name = tk.Label(master=frm_form, text="First Name:")
# ent_first_name = tk.Entry(master=frm_form, width=50)
# # Use the grid geometry manager to place the Label and
# # Entry widgets in the first and second columns of the
# # first row of the grid
# lbl_first_name.grid(row=0, column=0, sticky="e")
# ent_first_name.grid(row=0, column=1)

# # Create the Label and Entry widgets for "Last Name"
# lbl_last_name = tk.Label(master=frm_form, text="Last Name:")
# ent_last_name = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the second row of the grid
# lbl_last_name.grid(row=1, column=0, sticky="e")
# ent_last_name.grid(row=1, column=1)

# # Create the Label and Entry widgets for "Address Line 1"
# lbl_address1 = tk.Label(master=frm_form, text="Address Line 1:")
# ent_address1 = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the third row of the grid
# lbl_address1.grid(row=2, column=0, sticky="e")
# ent_address1.grid(row=2, column=1)

# # Create the Label and Entry widgets for "Address Line 2"
# lbl_address2 = tk.Label(master=frm_form, text="Address Line 2:")
# ent_address2 = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the fourth row of the grid
# lbl_address2.grid(row=3, column=0, sticky=tk.E)
# ent_address2.grid(row=3, column=1)

# # Create the Label and Entry widgets for "City"
# lbl_city = tk.Label(master=frm_form, text="City:")
# ent_city = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the fifth row of the grid
# lbl_city.grid(row=4, column=0, sticky=tk.E)
# ent_city.grid(row=4, column=1)

# # Create the Label and Entry widgets for "State/Province"
# lbl_state = tk.Label(master=frm_form, text="State/Province:")
# ent_state = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the sixth row of the grid
# lbl_state.grid(row=5, column=0, sticky=tk.E)
# ent_state.grid(row=5, column=1)

# # Create the Label and Entry widgets for "Postal Code"
# lbl_postal_code = tk.Label(master=frm_form, text="Postal Code:")
# ent_postal_code = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the seventh row of the grid
# lbl_postal_code.grid(row=6, column=0, sticky=tk.E)
# ent_postal_code.grid(row=6, column=1)

# # Create the Label and Entry widgets for "Country"
# lbl_country = tk.Label(master=frm_form, text="Country:")
# ent_country = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the eight row of the grid
# lbl_country.grid(row=7, column=0, sticky=tk.E)
# ent_country.grid(row=7, column=1)


# # Create a Text widget to display the submitted values
# text_output = tk.Text(frm_form, height=10, width=50)
# text_output.grid(row=8, columnspan=2)  # Span across two columns
# text_output.grid_propagate(False)  # Disable auto resizing

# # Create a new frame `frm_buttons` to contain the
# # Submit and Clear buttons. This frame fills the
# # whole window in the horizontal direction and has
# # 5 pixels of horizontal and vertical padding.
# frm_buttons = tk.Frame()
# frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# # Create the "Submit" button and pack it to the
# # right side of `frm_buttons`, binding the `submit` function
# btn_submit = tk.Button(master=frm_buttons, text="Submit", command=submit)
# btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

# # Create the "Clear" button and pack it to the
# # right side of `frm_buttons`, binding the `clear` function
# btn_clear = tk.Button(master=frm_buttons, text="Clear", command=clear)
# btn_clear.pack(side=tk.RIGHT, ipadx=10)

# # Start the application
# window.mainloop()

# ##################################################################################################
# ##################################################################################################


# # Create a window object
# window = tk.Tk()

# def increase():
#     value = int(lbl_value["text"])
#     lbl_value["text"] = f"{value + 1}"

# def decrease():
#     value = int(lbl_value["text"])
#     lbl_value["text"] = f"{value - 1}"

# btn_decrease = tk.Button(master=window, text="-", command=decrease)
# btn_decrease.grid(row=0, column=0, sticky="nsew")

# lbl_value = tk.Label(master=window, text="0")
# lbl_value.grid(row=0, column=1)

# btn_increase = tk.Button(master=window, text="+", command=increase)
# btn_increase.grid(row=0, column=2, sticky="nsew")

# # Run the event loop
# window.mainloop()