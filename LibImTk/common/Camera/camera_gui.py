import copy
from LibImTk.common.Camera.camera import Camera
from LibImTk.common.Camera.Cameraui import CameraUI
from LibImTk.common.Camera.camera_settings import CameraSettings
from LibImTk.common.timer_ex import TimerEx
from LibImTk.widgets.ScaleEx.scale_ex import ScaleEx
import tkinter as tk

class CameraGUI(Camera):
    # *******************************
    # init function
    # *******************************
    def __init__(self, settings: CameraSettings, master: tk.Frame=None):
        super().__init__(settings)

        self.__ui = CameraUI(master)
        self.__settings = settings
        self.__setting_scales = []

        self.__init_gui()
        self.__init_events()

    def __init_gui(self):
        self.__update_ctls_menus()
        self.__update_devices()
        self.__update_formats()
    
    def __init_events(self):
        self.__ui.entry_fps.bind("<Return>", self.__on_chenge_fps)
        TimerEx.after(1000, self.__init_scale_events)
        self.__ui.btn_reload_settings.bind('<1>',self.__on_click_reload_setting)

    def __init_scale_events(self):
        for scale in self.__setting_scales:
            scale.bind(self.__on_scale_changed)

    # *******************************
    # events function
    # *******************************
    def __on_click_reload_setting(self, event):
        self.__init_gui()
        self.__init_events()

    def __on_chenge_fps(self, event):
        fps = self.__ui.entry_fps.get()
        if fps.isdigit():
            if int(fps)>0:
                self.__settings.framerate = int(fps)
                self.__ui.frame_main.focus_set()

    def __on_change_image_size(self, size: str):
        self.close()
        self.__settings.resolution = tuple(map(int, size.split('x')))
        TimerEx.after(100,self.__reconnect_cam)

    def __on_change_device(self, device: str):
        num = int(device.replace('/dev/video', ''))
        if num == self.__settings.device_number:
            return
        self.close()
        self.__settings.device_number = num
        self.__init_gui()
        self.__init_events()
        TimerEx.after(100, self.__reconnect_cam)

    def __on_scale_changed(self):
        settings_bk = self.__settings.v4w2_ctls_menus
        settings_new = copy.deepcopy(settings_bk)

        for index, scale in enumerate(self.__setting_scales):
            key = list(settings_new.keys())[index]
            new_val = scale.get()
            if settings_bk[key]['value'] != new_val:
                self.__settings.apply_setting(
                    self.cam,
                    key,
                    new_val,
                    scale_finder=self.__find_scale_by_name
                )
                settings_new[key]['value'] = new_val
                break
        
        self.__settings.v4w2_ctls_menus = settings_new

    def __find_scale_by_name(self, name: str)->ScaleEx:
        for scale in self.__setting_scales:
            if scale.get_label() == name:
                return scale
        return None
    
    # *******************************
    # private function
    # *******************************
    def __reconnect_cam(self):
        callback = self.get_callback()
        super().__init__(self.__settings,callback)

    def __update_formats(self):
        formats = self.__settings.mjpeg_formats
        self.__ui.opt_image_size["menu"].delete(0, "end")
        for format in formats:
            self.__ui.opt_image_size["menu"].add_command(
                label=format,
                command=tk._setit(self.__ui.val_image_size, format, self.__on_change_image_size)
            )
        self.__ui.val_image_size.set(f'{self.__settings.resolution[0]}x{self.__settings.resolution[1]}')

    def __update_devices(self):
        devices = self.__settings.camera_devices
        self.__ui.opt_devices["menu"].delete(0, "end")
        for device in devices:
            self.__ui.opt_devices["menu"].add_command(
                label=device,
                command=tk._setit(self.__ui.val_devices, device, self.__on_change_device)
            )
        self.__ui.val_devices.set(f'/dev/video{self.__settings.device_number}')

    def __update_ctls_menus(self):
        for scale in self.__setting_scales:
            scale.destroy()
        self.__setting_scales.clear()
        
        settings = self.__settings.v4w2_ctls_menus
        for index, item in enumerate(settings):
            self.__setting_scales.append(ScaleEx(self.__ui.frame_main))
            if settings[item].get('min') is not None:
                self.__setting_scales[index].configure(
                    label=item,
                    from_=settings[item]['min'],
                    to=settings[item]['max'],
                    default=settings[item]['default'],
                    resolution=settings[item]['step']
                )
            else:
                self.__setting_scales[index].configure(
                    label=item,
                    from_=0,
                    to=1,
                    default=settings[item]['default']
                )
            self.__setting_scales[index].set(settings[item]['value'])

    # *******************************
    # public function
    # *******************************
    def show_widgets(self, visible: bool = True):
        if visible:
            self.__ui.mainwindow.pack(expand=True, fill="both", side="top")
        else:
            self.__ui.mainwindow.pack_forget()