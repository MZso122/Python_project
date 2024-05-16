import tkinter as tk
# import alapok as alapok
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import meghivogato_main as main
import threading
import string


cluster_num2:int = 6
obj_path:string = 'raw_features_1st_q'
obj_path_for_red:string = 'tomoritett_pirosak'


class Application(tk.Frame):



    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def on_quit(self):
        if hasattr(self, 'thread') and self.thread.is_alive():
        # Do any necessary cleanup or stop signals for the thread here
        # For example, if your main function has a loop, you might set a flag to exit the loop
        # Then join the thread to wait for it to finish
            self.thread.join()

        self.master.quit()
        self.master.destroy()

    def create_widgets(self):
        # Container frame for widgets
        widget_frame = tk.Frame(self)
        widget_frame.pack(side="left", fill="y", padx=10)
        
        self.hi_there = tk.Button(widget_frame, text = 'Run program\n(click me)', command = self.say_hi).pack(side="top", pady=5)
        # self.hi_there["text"] = "Run program\n(click me)"
        # self.hi_there["command"] = self.say_hi()
        # self.hi_there.pack(side="top")

        self.quit = tk.Button(widget_frame, text="QUIT", fg="red",
                              command=self.on_quit)
        self.quit.pack(side="bottom", pady=5)

        self.abrak = tk.BooleanVar()
        self.show_inertia_KMeans = tk.BooleanVar()
        self.print_extra_info = tk.BooleanVar()
        self.show_KMeans_pelda = tk.BooleanVar()

        self.checkbutton = tk.Checkbutton(widget_frame, text="Show extra figures", variable=self.abrak, onvalue = True, offvalue = False)
        self.checkbutton.pack(pady=10, anchor="w")
        self.checkbutton2 = tk.Checkbutton(widget_frame, text="Show inertia", variable=self.show_inertia_KMeans, onvalue = True, offvalue = False)
        self.checkbutton2.pack(pady=10, anchor="w")
        self.checkbutton3 = tk.Checkbutton(widget_frame, text="Print extra info to consol", variable=self.print_extra_info, onvalue = True, offvalue = False)
        self.checkbutton3.pack(pady=10, anchor="w")
        self.checkbutton4 = tk.Checkbutton(widget_frame, text="Give KMeans Exsample", variable=self.show_KMeans_pelda, onvalue = True, offvalue = False)
        self.checkbutton4.pack(pady=10, anchor="w")


        self.path_label = tk.Label(widget_frame, text="Object Path:")
        self.path_label.pack(pady=5, anchor="w")
        self.obj_path_entry = tk.Entry(widget_frame)
        self.obj_path_entry.pack(pady=5)
        self.obj_path_entry.insert(0, obj_path)
        self.path_label2 = tk.Label(widget_frame, text="Curve path:")
        self.path_label2.pack(pady=5, anchor="w")
        self.obj_path_entry2 = tk.Entry(widget_frame)
        self.obj_path_entry2.pack(pady=5)
        self.obj_path_entry2.insert(0, obj_path_for_red)

        self.scale = tk.Scale(widget_frame, from_=1, to=12, orient="horizontal", label= "Cluster_num: ", variable=cluster_num2)
        self.scale.pack(pady=5)

        self.status_label = tk.Label(widget_frame, text="", fg="green")
        self.status_label.pack(pady=5, anchor="w")


        plot_frame = tk.Frame(self)
        plot_frame.pack(side="right", fill="both", expand=True)
        self.fig = pyplot.figure()
        # ax = fig.add_subplot(111)
        # ax.plot(range(1, 20), range(1,20), marker='o')
        # ax.set_title('lkfdkjdslkfjsdkljfsldkfkjsdlkfj')
        # ax.set_xlabel('sdjkfhdskfheruoifher')
        # ax.set_ylabel('ldjfdslkfjkkdsfhewriufhiuwerfh')
        # # pyplot.show()
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # def say_hi(self):
    def say_hi(self):   # self, cluster_num2:int = 6, print_extra_info:bool = False, abrak:bool = False, show_inertia_KMeans:bool = True,
                        # show_KMeans_pelda:bool = False, obj_path:string = 'raw_features_1st_q', obj_path_for_red:string = 'tomoritett_pirosak'):
        obj_path = self.obj_path_entry.get()
        thread = threading.Thread(target=main.main, args=(self, self.canvas, self.fig, cluster_num2 , self.print_extra_info.get() , self.abrak.get() ,self.show_inertia_KMeans.get(),
                                  self.show_KMeans_pelda.get(), obj_path, obj_path_for_red))
        thread.start()  

        

root = tk.Tk()
app = Application(master=root)
app.mainloop()