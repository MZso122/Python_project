import tkinter as tk
# import alapok as alapok
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import meghivogato_main as main
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Run program\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        # fig = pyplot.figure()
        # ax = fig.add_subplot(111)
        # ax.plot(range(1, 20), range(1,20), marker='o')
        # ax.set_title('lkfdkjdslkfjsdkljfsldkfkjsdlkfj')
        # ax.set_xlabel('sdjkfhdskfheruoifher')
        # ax.set_ylabel('ldjfdslkfjkkdsfhewriufhiuwerfh')
        # # pyplot.show()
        # canvas = FigureCanvasTkAgg(fig, master=self)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # def say_hi(self):
    def say_hi(self):
        thread = threading.Thread(target=main.main, args=(self,))
        thread.start()

        

root = tk.Tk()
app = Application(master=root)
app.mainloop()