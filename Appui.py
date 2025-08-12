#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


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
        labelframe1 = tk.LabelFrame(self.pane_main)
        labelframe1.configure(
            font="TkDefaultFont",
            height=200,
            text='menu',
            width=300)
        notebook1 = ttk.Notebook(labelframe1)
        notebook1.configure(height=200, width=200)
        frame1 = tk.Frame(notebook1)
        frame1.configure(height=200, relief="raised", width=200)
        labelframe2 = tk.LabelFrame(frame1)
        labelframe2.configure(height=200, text='camera', width=200)
        self.btn_save_image = tk.Button(labelframe2, name="btn_save_image")
        self.btn_save_image.configure(text='save image')
        self.btn_save_image.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        self.frame_cross_line = tk.LabelFrame(
            labelframe2, name="frame_cross_line")
        self.frame_cross_line.configure(
            height=200, text='cross line', width=200)
        self.chk_closs_line = tk.Checkbutton(
            self.frame_cross_line, name="chk_closs_line")
        self.chk_closs_line.configure(text='enable')
        self.chk_closs_line.pack(anchor="w", side="top")
        self.frame_cross_line.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        labelframe2.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        labelframe4 = tk.LabelFrame(frame1)
        labelframe4.configure(
            height=200,
            text='camera settings file',
            width=200)
        self.btn_load_settings = tk.Button(
            labelframe4, name="btn_load_settings")
        self.btn_load_settings.configure(text='load file')
        self.btn_load_settings.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        self.btn_save_settings = tk.Button(
            labelframe4, name="btn_save_settings")
        self.btn_save_settings.configure(text='save file')
        self.btn_save_settings.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        labelframe4.pack(
            fill="x",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        notebook1.add(frame1, text=' main ')
        self.frame_cam_settings = tk.Frame(
            notebook1, name="frame_cam_settings")
        self.frame_cam_settings.configure(
            height=200, relief="raised", width=200)
        notebook1.add(self.frame_cam_settings, text='camera settigs')
        notebook1.pack(
            expand=True,
            fill="both",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="top")
        labelframe1.pack(
            fill="y",
            ipadx=4,
            ipady=4,
            padx=4,
            pady=4,
            side="left")
        self.pane_main.add(labelframe1)
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
