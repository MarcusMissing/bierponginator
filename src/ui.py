import os
import sys
import tkinter as tk

import numpy as np

import client_socket

font = ('Comic Sans MS', 36, 'bold')
possibilities = [[i, j, k, l, m, n, o, p, q, r] for r in range(2)
                 for q in range(2)
                 for p in range(2)
                 for o in range(2)
                 for n in range(2)
                 for m in range(2)
                 for l in range(2)
                 for k in range(2)
                 for j in range(2)
                 for i in range(2)]


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


class MainFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.difficulty = 1

        self.frames = {}

        for F in (MenuPage, Calibrate, Difficulty, PageFour, Console):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(MenuPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def get_difficulty(self):
        return self.difficulty


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Grid.columnconfigure(self, 2, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)

        tk.Button(self, text='Start/Stop', font=font, command=lambda: client_socket.start_classify()).grid(
            column=0, row=0, sticky='nsew')

        tk.Button(self, text='Calibrate', font=font, command=lambda: controller.show_frame(Calibrate)).grid(
            column=0, row=1, sticky='nsew')

        self.difficulty_button = tk.Button(self, text='Difficulty:\n' + str(controller.get_difficulty()) + "/10",
                                           font=font, command=lambda: controller.show_frame(Difficulty))
        self.difficulty_button.grid(column=1, row=0, sticky='nsew')
        self.refresh_difficulty()

        tk.Button(self, text='Reset?', font=font, command=lambda: controller.show_frame(PageFour)).grid(
            column=1, row=1, sticky='nsew')

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(column=2, row=0, sticky='nsew')

        cup_path = os.path.join("..", "resource", "cup.png")
        no_cup_path = os.path.join("..", "resource", "no_cup.png")
        self.cup = tk.PhotoImage(file=cup_path)
        self.no_cup = tk.PhotoImage(file=no_cup_path)

        self.button_flags = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=bool)
        self.counter = 0

        x_shift = 5
        y_shift = -15

        self.button0 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button0, 0))
        self.button0.place(in_=self.button_frame, x=x_shift + 95, y=y_shift + 185)

        self.button1 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button1, 1))
        self.button1.place(in_=self.button_frame, x=x_shift + 70, y=y_shift + 135)

        self.button2 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button2, 2))
        self.button2.place(in_=self.button_frame, x=x_shift + 120, y=y_shift + 135)

        self.button3 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button3, 3))
        self.button3.place(in_=self.button_frame, x=x_shift + 45, y=y_shift + 85)

        self.button4 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button4, 4))
        self.button4.place(in_=self.button_frame, x=x_shift + 95, y=y_shift + 85)

        self.button5 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button5, 5))
        self.button5.place(in_=self.button_frame, x=x_shift + 145, y=y_shift + 85)

        self.button6 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button6, 6))
        self.button6.place(in_=self.button_frame, x=x_shift + 15, y=y_shift + 35)

        self.button7 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button7, 7))
        self.button7.place(in_=self.button_frame, x=x_shift + 65, y=y_shift + 35)

        self.button8 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button8, 8))
        self.button8.place(in_=self.button_frame, x=x_shift + 115, y=y_shift + 35)

        self.button9 = tk.Button(self, image=self.cup, bg='white', command=lambda: self.click(self.button9, 9))
        self.button9.place(in_=self.button_frame, x=x_shift + 165, y=y_shift + 35)

        self.refresh_cups()

        tk.Button(self, text='Console', font=font, command=lambda: controller.show_frame(Console)).grid(
            column=2, row=1, sticky='nsew')

        for x in range(2):
            tk.Grid.columnconfigure(self, x, weight=1)

        for y in range(1):
            tk.Grid.rowconfigure(self, y, weight=1)

    def click(self, widget, pos):
        self.button_flags[pos]
        if self.button_flags[pos] == 1:
            widget.config(image=self.no_cup)
            self.button_flags[pos] = 0
        else:
            widget.config(image=self.cup)

            self.button_flags[pos] = 1

    def refresh_cups(self):
        self.button_flags = possibilities[self.counter]
        self.click(self.button0, 0)
        self.click(self.button1, 1)
        self.click(self.button2, 2)
        self.click(self.button3, 3)
        self.click(self.button4, 4)
        self.click(self.button5, 5)
        self.click(self.button6, 6)
        self.click(self.button7, 7)
        self.click(self.button8, 8)
        self.click(self.button9, 9)
        self.counter += 1
        self.after(1000, self.refresh_cups)

    def show_difficulty(self, widget, difficulty):
        widget.config(text='Difficulty:\n' + str(difficulty) + "/10")

    def refresh_difficulty(self):
        self.show_difficulty(self.difficulty_button, self.controller.get_difficulty())
        self.after(300, self.refresh_difficulty)


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
        label = tk.Label(self, text="Set difficulty:", font=font)
        label.pack()
        self.difficulty = tk.IntVar()
        scale = tk.Scale(self, from_=1, to=10, variable=self.difficulty, orient=tk.HORIZONTAL, length=600,
                         sliderlength=15, tickinterval=1, width=20, showvalue=False)
        scale.pack(pady=100)
        tk.Button(self, text='Back to Home', font=font,
                  command=lambda: combine_funcs(controller.show_frame(MenuPage),
                                                controller.set_difficulty(self.difficulty.get()))).pack(
            side=tk.BOTTOM)


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
        tk.Button(self, text='Back to Home', command=lambda: controller.show_frame(MenuPage)).pack(
            in_=toolbar, side='right')
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


if __name__ == "__main__":
    app = MainFrame()
    app.title('Bierponginator')
    app.geometry('800x450')  # 800x480 Pi display resolution
    app.mainloop()
