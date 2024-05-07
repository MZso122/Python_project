import tkinter as tk
# import alapok as alapok
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import meghivogato_main as main
import threading
import string


cluster_num2:int = 6
print_extra_info:bool = False
abrak:bool = False
show_inertia_KMeans:bool = False
show_KMeans_pelda:bool = False
obj_path:string = 'raw_features_1st_q'
obj_path_for_red:string = 'tomoritett_pirosak'


class Application(tk.Frame):



    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self, text = 'Run program\n(click me)', command = self.say_hi).pack(side="top")
        # self.hi_there["text"] = "Run program\n(click me)"
        # self.hi_there["command"] = self.say_hi()
        # self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.checkbutton = tk.Checkbutton(self, text="abrak", variable=abrak, onvalue = True, offvalue = False)
        self.checkbutton.pack(pady=10)

        self.path_label = tk.Label(self, text="Object Path:")
        self.path_label.pack()
        self.obj_path_entry = tk.Entry(self)
        self.obj_path_entry.pack()
        self.obj_path_entry.insert(0, obj_path)

        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.pack()

        self.fig = pyplot.figure()
        # ax = fig.add_subplot(111)
        # ax.plot(range(1, 20), range(1,20), marker='o')
        # ax.set_title('lkfdkjdslkfjsdkljfsldkfkjsdlkfj')
        # ax.set_xlabel('sdjkfhdskfheruoifher')
        # ax.set_ylabel('ldjfdslkfjkkdsfhewriufhiuwerfh')
        # # pyplot.show()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # def say_hi(self):
    def say_hi(self):   # self, cluster_num2:int = 6, print_extra_info:bool = False, abrak:bool = False, show_inertia_KMeans:bool = True,
                        # show_KMeans_pelda:bool = False, obj_path:string = 'raw_features_1st_q', obj_path_for_red:string = 'tomoritett_pirosak'):
        obj_path = self.obj_path_entry.get()
        thread = threading.Thread(target=main.main, args=(self, self.canvas, self.fig, cluster_num2 , print_extra_info , abrak ,show_inertia_KMeans,
                                  show_KMeans_pelda, obj_path, obj_path_for_red))
        thread.start()  

        

root = tk.Tk()
app = Application(master=root)
app.mainloop()