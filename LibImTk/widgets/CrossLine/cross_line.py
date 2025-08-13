#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

import cv2
from LibImTk.widgets.CrossLine.cross_lineui import CrossLineUI
from LibImTk.widgets.ScaleEx.scale_ex import ScaleEx

class CrossLine(CrossLineUI):

    # ****************************************
    # init function
    # ****************************************
    def __init__(self, master=None):
        self.__scale_x: ScaleEx = None
        self.__scale_y: ScaleEx = None
        self.__has_gui: bool = master is not None

        if self.__has_gui:
            super().__init__(master)
            self.__init_gui()
            self.__init_events()

    def __init_gui(self):
        self.__scale_x = ScaleEx(self.frame_cross_line)
        self.__scale_x.configure(
            padx=4,
            pady=4,
            label='x',
            side='top',
            from_=0,
            to=100,
            default=0,
            resolution=1)
        self.__scale_y = ScaleEx(self.frame_cross_line)
        self.__scale_y.configure(
            padx=4,
            pady=4,
            label='y',
            side='top',
            from_=0,
            to=100,
            default=0,
            resolution=1)

    def __init_events(self):
        pass

    # ****************************************
    # public function
    # ****************************************
    def get_cross_line_image(self, img: cv2.Mat, param: tuple = (-1, -1), color:tuple=(0, 0, 255), thickness:int=2):
        height, width = img.shape[:2]
        x = param[0]
        y = param[1]

        if self.__has_gui:
            if self.__scale_x['to'] != width:
                self.__scale_x['to'] = width
                self.__scale_x['default'] = int(width / 2)
                self.__scale_x.set(int(width / 2))
            if self.__scale_y['to'] != height:
                self.__scale_y['to'] = height
                self.__scale_y['default'] = int(height / 2)
                self.__scale_y.set(int(height / 2))

            if not self.val_enable.get() and param == (-1, -1):
                return img
            
            if param == (-1, -1):
                x = self.__scale_x.get()
                y = self.__scale_y.get()
        else:
            if param == (-1, -1):
                x = int(width / 2)
                y = int(height / 2)

        cv2.line(img, (x, 0), (x, height), color, thickness)
        cv2.line(img, (0, y), (width, y), color, thickness)
        return img

