#!/usr/bin/python3
import tkinter as tk


class CrossLineUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        self.frame_cross_line = tk.LabelFrame(master, name="frame_cross_line")
        self.frame_cross_line.configure(
            height=200, text='cross line', width=200)
        checkbutton1 = tk.Checkbutton(self.frame_cross_line)
        self.val_enable = tk.DoubleVar()
        checkbutton1.configure(text='enable', variable=self.val_enable)
        checkbutton1.pack(anchor="w", ipadx=4, padx=4, side="top")
        self.frame_cross_line.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")

        # Main widget
        self.mainwindow = self.frame_cross_line

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = CrossLineUI(root)
    app.run()
