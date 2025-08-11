#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import Appui as baseui
from LibImTk import ImshowCustom, CameraGUI, CameraSettings


class App(baseui.AppUI):
    # ***************************************
    # init function
    # ***************************************
    def __init__(self, master=None):
        super().__init__(master)
        self.__draw_flag:bool=True
        self.__cv2c:ImshowCustom = None
        self.__cam:CameraGUI = None
        self.__image_size=(0,0)

        self.__init_gui()
        self.__init_cam()
        self.__init_events()
        
    def __init_gui(self):
        self.__cv2c=ImshowCustom(self.frame_view, self.mainwindow)
        self.pane_main.sash_place(0,280,0)

    def __init_events(self):
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.__on_close_window)
        self.__cv2c.bind('<mouse_action>', self.__on_mouse_action)
        self.__cv2c.bind('<keyboard_action>', self.__on_keyboard_action)
        self.__cam.bind("open_cam", self.__on_open_cam)
        self.__cam.bind("read_frame", self.__on_read_frame)
        
    def __init_cam(self):
        settings = CameraSettings()
        settings.device_number = 1
        # settings.resolution = (3840, 2160)
        settings.resolution = (1920, 1080)
        settings.framerate = 10
        self.__cam = CameraGUI(settings,self.frame_menu)
        
        
    # ***************************************
    # events function
    # ***************************************
    def __on_mouse_action(self, event, x, y):
        # print(event, x, y)
        pass

    def __on_keyboard_action(self, event):
        # print(event)
        pass        

    def __on_close_window(self):
        self.__cam.close()
        self.mainwindow.after(100,self.mainwindow.destroy)

    def __on_open_cam(self):
        self.__cam.start_get_frame()

    def __on_read_frame(self, img):
        if self.__draw_flag:
            self.__cv2c.imshow(f'FPS:{self.__cam.fps}', img)
            if img.shape[:2] != self.__image_size:
                self.__image_size = img.shape[:2]
                self.__cv2c.reset_view()

    # ***************************************
    # public function
    # ***************************************


    # ***************************************
    # private function
    # ***************************************


if __name__ == "__main__":
    app = App()
    app.run()
