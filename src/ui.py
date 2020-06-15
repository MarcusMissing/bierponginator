import sys
import tkinter as tk

font = ('Comic Sans MS', 36, 'bold')


class MainFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuPage, PageOne, PageTwo, PageThree, PageFour, PageFive, Console):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MenuPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Grid.columnconfigure(self, 2, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)

        tk.Button(self, text='btn1', font=font, command=lambda: controller.show_frame(PageOne)).grid(
            column=0, row=0, sticky='nsew')
        tk.Button(self, text='btn2', font=font, command=lambda: controller.show_frame(PageTwo)).grid(
            column=0, row=1, sticky='nsew')
        tk.Button(self, text='btn3', font=font, command=lambda: controller.show_frame(PageThree)).grid(
            column=1, row=0, sticky='nsew')
        tk.Button(self, text='btn4', font=font, command=lambda: controller.show_frame(PageFour)).grid(
            column=1, row=1, sticky='nsew')
        tk.Button(self, text='btn5', font=font, command=lambda: controller.show_frame(PageFive)).grid(
            column=2, row=0, sticky='nsew')
        tk.Button(self, text='Console', font=font, command=lambda: controller.show_frame(Console)).grid(
            column=2, row=1, sticky='nsew')

        for x in range(2):
            tk.Grid.columnconfigure(self, x, weight=1)

        for y in range(1):
            tk.Grid.rowconfigure(self, y, weight=1)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page One!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Two!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Two!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Three!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Four!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page Five!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class Console(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        toolbar = tk.Frame(self)
        toolbar.pack(side='top', fill='x')
        tk.Button(self, text='print to stdout', command=self.print_stdout).pack(in_=toolbar, side='left')
        tk.Button(self, text='print to stderr', command=self.print_stderr).pack(in_=toolbar, side='left')
        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack(in_=toolbar,
                                                                                                   side='right')
        self.text = tk.Text(self, wrap='word', bg='black')
        self.text.pack(side='top', fill='both', expand=True)
        self.text.tag_configure('stderr', foreground='red')
        self.text.tag_configure('stdout', foreground='white')

        sys.stdout = TextRedirector(self.text, 'stdout')
        sys.stderr = TextRedirector(self.text, 'stderr')

    def print_stdout(self):
        print('this is stdout')

    def print_stderr(self):
        sys.stderr.write('this is stderr\n')


class TextRedirector(object):
    def __init__(self, widget, tag='stdout'):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert('end', str, (self.tag,))
        self.widget.configure(state='disabled')


app = MainFrame()
app.title('Bierponginator')
app.geometry('800x450')  # 800x480 Pi display resolution
app.mainloop()
