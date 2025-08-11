#!/usr/bin/python3
import tkinter as tk


class AppUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, width=200)
        toplevel1.geometry("640x480")
        self.pane_main = tk.PanedWindow(
            toplevel1, orient="horizontal", name="pane_main")
        self.pane_main.configure(
            handlesize=4,
            height=200,
            sashrelief="raised",
            sashwidth=4,
            showhandle=True,
            width=200)
        self.frame_menu = tk.LabelFrame(self.pane_main, name="frame_menu")
        self.frame_menu.configure(
            font="TkDefaultFont",
            height=200,
            text='menu',
            width=300)
        self.frame_menu.pack(
            fill="y",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="left")
        self.pane_main.add(self.frame_menu)
        self.frame_view = tk.LabelFrame(self.pane_main, name="frame_view")
        self.frame_view.configure(height=200, text='view', width=200)
        self.frame_view.pack(
            expand=True,
            fill="both",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="left")
        self.pane_main.add(self.frame_view)
        self.pane_main.pack(
            expand=True,
            fill="both",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = AppUI()
    app.run()
