import sys
import tkinter as tk

import numpy as np

font = ('Comic Sans MS', 36, 'bold')


class MainFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuPage, Start, Calibrate, Difficulty, PageFour, Console):
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

        tk.Button(self, text='Start/Stop', font=font, command=lambda: controller.show_frame(Start)).grid(
            column=0, row=0, sticky='nsew')
        tk.Button(self, text='Calibrate', font=font, command=lambda: controller.show_frame(Calibrate)).grid(
            column=0, row=1, sticky='nsew')
        tk.Button(self, text='Difficulty', font=font, command=lambda: controller.show_frame(Difficulty)).grid(
            column=1, row=0, sticky='nsew')
        tk.Button(self, text='Reset?', font=font, command=lambda: controller.show_frame(PageFour)).grid(
            column=1, row=1, sticky='nsew')

        button_frame = tk.Frame(self)
        button_frame.grid(column=2, row=0, sticky='nsew')
        self.cup = tk.PhotoImage(file="../resource/cup.png")
        self.no_cup = tk.PhotoImage(file="../resource/no_cup.png")

        self.button_flag = np.array([True, True, True, True, True, True, True, True, True, True], dtype=bool)

        x_shift = 5
        y_shift = -15

        self.button0 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button0, 0))
        self.button0.place(in_=button_frame, x=x_shift+95, y=y_shift+185)

        self.button1 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button1, 1))
        self.button1.place(in_=button_frame, x=x_shift+70, y=y_shift+135)

        self.button2 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button2, 2))
        self.button2.place(in_=button_frame, x=x_shift+120, y=y_shift+135)

        self.button3 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button3, 3))
        self.button3.place(in_=button_frame, x=x_shift+45, y=y_shift+85)

        self.button4 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button4, 4))
        self.button4.place(in_=button_frame, x=x_shift+95, y=y_shift+85)

        self.button5 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button5, 5))
        self.button5.place(in_=button_frame, x=x_shift+145, y=y_shift+85)

        self.button6 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button6, 6))
        self.button6.place(in_=button_frame, x=x_shift+15, y=y_shift+35)

        self.button7 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button7, 7))
        self.button7.place(in_=button_frame, x=x_shift+65, y=y_shift+35)

        self.button8 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button8, 8))
        self.button8.place(in_=button_frame, x=x_shift+115, y=y_shift+35)

        self.button9 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button9, 9))
        self.button9.place(in_=button_frame, x=x_shift+165, y=y_shift+35)

        tk.Button(self, text='Console', font=font, command=lambda: controller.show_frame(Console)).grid(
            column=2, row=1, sticky='nsew')

        for x in range(2):
            tk.Grid.columnconfigure(self, x, weight=1)

        for y in range(1):
            tk.Grid.rowconfigure(self, y, weight=1)

    def click(self, widget, pos):
        self.button_flag[pos]
        if self.button_flag[pos]:
            widget.config(bg="white", image=self.no_cup)
            self.button_flag[pos] = False
        else:
            widget.config(bg="green", image=self.cup)
            self.button_flag[pos] = True


class Start(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Page One!!!', font=font)
        label.pack(pady=10, padx=10)

        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack()


class Calibrate(tk.Frame):

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


class Difficulty(tk.Frame):

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
        self.widget.see("end")
        self.widget.configure(state='disabled')


app = MainFrame()
app.title('Bierponginator')
app.geometry('800x450')  # 800x480 Pi display resolution
app.mainloop()
