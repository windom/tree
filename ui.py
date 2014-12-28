import tkinter as tk


class DrawingUi(tk.Frame):

    def __init__(self, width, height, title):
        self.root = createRoot(width, height, title)

        super().__init__(master=self.root)

        self.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def run(self):
        self.root.mainloop()


def createRoot(width, height, title):
    root = tk.Tk()
    set_size_center(root, width, height)
    root.resizable(width=tk.FALSE, height=tk.FALSE)
    root.title(title)
    return root


def set_size_center(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry("{}x{}+{}+{}".format(width, height, x, y))
