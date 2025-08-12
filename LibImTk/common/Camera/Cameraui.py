#!/usr/bin/python3
import tkinter as tk
from pygubu.widgets.tkscrolledframe import TkScrolledFrame


class CameraUI:
    def __init__(self, master=None, data_pool=None):
        # build ui
        tkscrolledframe2 = TkScrolledFrame(master, scrolltype="both")
        tkscrolledframe2.innerframe.configure(width=350)
        tkscrolledframe2.configure(usemousewheel=False)
        self.btn_reload_settings = tk.Button(
            tkscrolledframe2.innerframe,
            name="btn_reload_settings")
        self.btn_reload_settings.configure(text='reload settings')
        self.btn_reload_settings.pack(
            fill="x", ipadx=4, ipady=4, padx=8, pady=4, side="top")
        self.frame_main = tk.Frame(
            tkscrolledframe2.innerframe,
            name="frame_main")
        self.frame_main.configure(height=200)
        frame1 = tk.Frame(self.frame_main)
        frame1.configure(height=200, width=200)
        labelframe1 = tk.LabelFrame(frame1)
        labelframe1.configure(height=200, text='camera devices', width=200)
        self.val_devices = tk.StringVar()
        __values = ['None']
        self.opt_devices = tk.OptionMenu(
            labelframe1, self.val_devices, *__values, command=None)
        self.opt_devices.pack(fill="x", padx=4, side="top")
        labelframe1.pack(fill="x", ipadx=4, padx=4, side="top")
        labelframe2 = tk.LabelFrame(frame1)
        labelframe2.configure(height=200, text='image size', width=200)
        self.val_image_size = tk.StringVar()
        __values = ['None']
        self.opt_image_size = tk.OptionMenu(
            labelframe2, self.val_image_size, *__values, command=None)
        self.opt_image_size.pack(fill="x", padx=4, side="top")
        labelframe2.pack(fill="x", ipadx=4, padx=4, side="top")
        labelframe3 = tk.LabelFrame(frame1)
        labelframe3.configure(height=200, text='view fps', width=200)
        label4 = tk.Label(labelframe3)
        label4.configure(text='fps')
        label4.pack(padx=4, side="left")
        self.entry_fps = tk.Entry(labelframe3, name="entry_fps")
        self.entry_fps.configure(justify="center")
        _text_ = '10'
        self.entry_fps.delete("0", "end")
        self.entry_fps.insert("0", _text_)
        self.entry_fps.pack(expand=True, fill="x", padx=4, side="left")
        labelframe3.pack(fill="x", ipadx=4, ipady=4, padx=4, side="top")
        frame1.pack(fill="x", ipadx=4, ipady=4, padx=4, pady=4, side="top")
        self.frame_main.pack(fill="x", side="top")
        tkscrolledframe2.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = tkscrolledframe2

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraUI(root)
    app.run()
