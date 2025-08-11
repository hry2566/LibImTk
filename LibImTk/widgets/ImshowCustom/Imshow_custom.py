import platform
import tkinter
from time import sleep
import cv2
import numpy as np
import tkinter as tk

from LibImTk import ImageCommLib
from .Imshow_custom_base import ImshowCustomBase
from .event_manager import EventManager
from .io_helper import IOHelper
from .renderer import Renderer
from .ui_widget import UIWidget


class ImshowCustom(ImshowCustomBase):
    def __init__(self, master=None, mainwindow=None):
        self.__master = tkinter.Tk() if master is None else master
        self.__mainwindow = master if mainwindow is None else mainwindow
        super().__init__(self.__master, self.__mainwindow)

        self.__event_manager = EventManager(self)
        self.__renderer = Renderer(self)
        self.__io_helper = IOHelper(self)
        self.__ui_widget = UIWidget(self)

        self.__os_type = platform.system()
        self.__canvas_img = None
        self.__view_scale = 1.0
        self.__image_scale = 1
        self.__imgpos_x = 0
        self.__imgpos_y = 0
        self.__mouse_x = 0
        self.__mouse_y = 0
        self.__origin_img = None
        self.__func_onmouse = None
        self.__func_onkeyboard = None
        self.__key = 0
        self.__ctrl_key = False
        self.__key_flag = False
        self.__draw_event = tk.IntVar()
        self.__busy_flag = False
        self.__shape_size = 0
        self.init_events()

    @property
    def _origin_img(self): return self.__origin_img

    @property
    def _os_type(self): return self.__os_type

    @property
    def _canvas_img(self): return self.__canvas_img
    @_canvas_img.setter
    def _canvas_img(self, value): self.__canvas_img = value

    @property
    def _view_scale(self): return self.__view_scale
    @_view_scale.setter
    def _view_scale(self, value): self.__view_scale = value

    @property
    def _image_scale(self): return self.__image_scale
    @_image_scale.setter
    def _image_scale(self, value): self.__image_scale = value

    @property
    def _imgpos_x(self): return self.__imgpos_x
    @_imgpos_x.setter
    def _imgpos_x(self, value): self.__imgpos_x = value

    @property
    def _imgpos_y(self): return self.__imgpos_y
    @_imgpos_y.setter
    def _imgpos_y(self, value): self.__imgpos_y = value

    @property
    def _mouse_x(self): return self.__mouse_x
    @_mouse_x.setter
    def _mouse_x(self, value): self.__mouse_x = value

    @property
    def _mouse_y(self): return self.__mouse_y
    @_mouse_y.setter
    def _mouse_y(self, value): self.__mouse_y = value

    @property
    def _func_onmouse(self): return self.__func_onmouse
    @_func_onmouse.setter
    def _func_onmouse(self, value): self.__func_onmouse = value

    @property
    def _func_onkeyboard(self): return self.__func_onkeyboard
    @_func_onkeyboard.setter
    def _func_onkeyboard(self, value): self.__func_onkeyboard = value

    @property
    def _key(self): return self.__key
    @_key.setter
    def _key(self, value): self.__key = value

    @property
    def _ctrl_key(self): return self.__ctrl_key
    @_ctrl_key.setter
    def _ctrl_key(self, value): self.__ctrl_key = value

    @property
    def _key_flag(self): return self.__key_flag
    @_key_flag.setter
    def _key_flag(self, value): self.__key_flag = value

    @property
    def _busy_flag(self): return self.__busy_flag
    @_busy_flag.setter
    def _busy_flag(self, value): self.__busy_flag = value

    @property
    def _shape_size(self): return self.__shape_size
    @_shape_size.setter
    def _shape_size(self, value): self.__shape_size = value

    def init_events(self):
        if self.__mainwindow is None:
            self.mainwindow.protocol("WM_DELETE_WINDOW", self.__event_manager._click_close)
        self.mainwindow.bind('<Any-KeyPress>', self.__event_manager._on_key)
        self.mainwindow.bind('<Any-KeyRelease>', self.__event_manager._on_key_release)
        self.img_view.bind('<Configure>', self.__event_manager._on_resize)
        self.img_view.bind('<Motion>', self.__event_manager._on_mouse_move)
        self.img_view.bind('<Button-1>', self.__event_manager._on_mouse_left_down)
        self.img_view.bind('<Button-3>', self.__event_manager._on_mouse_right_down)
        self.img_view.bind('<ButtonRelease-1>', self.__event_manager._on_mouse_left_up)
        self.img_view.bind('<ButtonRelease-3>', self.__event_manager._on_mouse_right_up)
        if self.__os_type == 'Windows':
            self.img_view.bind("<MouseWheel>", self.__event_manager._mouse_wheel)
        elif self.__os_type == 'Linux':
            self.img_view.bind("<ButtonPress-4>", self.__event_manager._mouse_wheel)
            self.img_view.bind("<ButtonPress-5>", self.__event_manager._mouse_wheel)
        self.img_view.bind('<2>', self.__event_manager._mouse_wheel_down)
        self.img_view.bind('<ButtonRelease-2>', self.__event_manager._mouse_wheel_up)
        self.__draw_event.trace_add(('write'), self.__renderer._draw)

    def _draw(self, *args):
        self.__renderer._draw(*args)

    def _set_status_value(self):
        self.__ui_widget._set_status_value()

    def _calc_scale(self):
        if self.__origin_img is None:
            return
        width, height = self.__ui_widget._get_canvas_size()
        img_height, img_width, _ = self.__origin_img.shape
        scale = 1 / (img_width / width) if img_width / width > img_height / height else 1 / (img_height / height)
        self.__image_scale = scale

    def imshow(self, winname=None, mat=None, wnd_size=None):
        if self.__key_flag:
            self.__key = 0
        # self.mainwindow.deiconify()
        self.mainwindow.title(winname if winname else '')
        if wnd_size:
            self.mainwindow.geometry(f'{wnd_size[0]}x{wnd_size[1]}')
        self.__origin_img = mat if mat is not None else ImageCommLib.get_blank_image((320, 240), 3)
        self._set_status_value()
        self.__busy_flag = True
        self.__draw_event.set(0)
        while self.__busy_flag:
            sleep(0.001)

    def waitKey(self, delay=1):
        sleep(delay / 1000)
        return self.__key

    def bind(self, event, func):
        if event == '<mouse_action>':
            self.__func_onmouse = func
        elif event == '<keyboard_action>':
            self.__func_onkeyboard = func

    def activate(self):
        self.mainwindow.bind('<Any-KeyPress>', self.__event_manager._on_key)
        self.mainwindow.bind('<Any-KeyRelease>', self.__event_manager._on_key_release)
        self.mainwindow.after(100, self._calc_scale)

    def reset_view(self):
        self.__view_scale = 1.0
        self.__imgpos_x = 0
        self.__imgpos_y = 0
        self._calc_scale()
        self.__renderer._draw(None)

    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        return self.__io_helper.imread(filename, flags, dtype)

    def imwrite(self, filename, img, params=None):
        return self.__io_helper.imwrite(filename, img, params)
