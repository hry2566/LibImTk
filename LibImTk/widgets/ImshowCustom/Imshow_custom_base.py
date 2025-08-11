#!/usr/bin/python3
import tkinter as tk


class ImshowCustomBase:
    def __init__(self, master=None,mainwindow=None):
        if mainwindow is None:
            mainwindow = master
        # build ui
        self.frame_view = tk.Frame(master)
        self.frame_view.configure(height=200, width=200)
        self.img_view = tk.Canvas(self.frame_view)
        self.img_view.configure(relief="sunken")
        self.img_view.pack(expand=True, fill="both", side="top")
        frame2 = tk.Frame(self.frame_view)
        frame2.configure(height=200, width=200)
        self.statusbar = tk.Label(frame2)
        self.statusbar.configure(anchor="w", relief="sunken", text='label1')
        self.statusbar.pack(fill="x", side="top")
        frame2.pack(fill="x", side="top")
        self.frame_view.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = mainwindow

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImshowCustomBase(root)
    app.run()
