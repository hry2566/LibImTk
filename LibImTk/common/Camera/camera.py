import threading
import time
from typing import Literal
import cv2

from LibImTk import CameraSettings

class Camera:
    # **********************************************************
    # init function
    # **********************************************************

    def __init__(self, settings:CameraSettings,callback:callable=None):
        self.__thread_open_cam: threading.Thread = None
        self.__thread_read_buffer: threading.Thread = None
        self.__thread_get_frame: threading.Thread = None
        self.__stop_open_cam_event = threading.Event()
        self.__stop_read_buffer_event = threading.Event()
        self.__stop_get_frame_event = threading.Event()
        self.__open_cam_callback: callable = None
        self.__read_frame_function: callable = None
        self.__is_cam_opened: bool = False
        self.__settings: CameraSettings = settings
        self.__cam: cv2.VideoCapture = None
        self.__start: float = time.time()
        self.__frame_count: int = 0
        self.__fps: int = 0
        self.__fps_display_time: float = time.time()

        if callback is not None:
            self.__open_cam_callback = callback[0]
            self.__read_frame_function = callback[1]

        self.__thread_open_cam = self.__start_thread(self.__open_cam)

    def __del__(self):
        self.close()

    # **********************************************************
    # property
    # **********************************************************
    @property
    def fps(self):
        return self.__fps
    
    @property
    def cam(self):
        return self.__cam

    # **********************************************************
    # thread function
    # **********************************************************
    def __open_cam(self):
        while not self.__stop_open_cam_event.is_set():
            self.__cam = cv2.VideoCapture(self.__settings.device_number)
            if self.__stop_open_cam_event.wait(1):
                break
            if self.__cam.isOpened():
                self.__settings.apply_resolution(self.__cam) 
                self.__is_cam_opened = True
                if self.__open_cam_callback is not None:
                    self.__handler(self.__open_cam_callback)
                self.__thread_read_buffer = self.__start_thread(self.__start_read_buffer)
                break
            else:
                print("Camera not opened")
                self.__cam.release()
                self.__cam = None
                if self.__stop_open_cam_event.wait(0.1):
                    break

    def __start_read_buffer(self):
        # print('start_read_buffer')
        while not self.__stop_read_buffer_event.is_set():
            if self.__cam:
                self.__cam.grab()
            if self.__stop_read_buffer_event.wait(0.001):
                break

    def __start_get_frame(self):
        # print('start_get_frame')
        while not self.__stop_get_frame_event.is_set():
            img = self.read()
            if img is not None and self.__read_frame_function is not None:
                self.__handler(self.__read_frame_function, img)
            else:
                if self.__stop_get_frame_event.wait(0.005):
                    break

    # **********************************************************
    # private function
    # **********************************************************

    def __handler(self, func: callable, *args: tuple):
        try:
            func(*args)
        except Exception as e:
            print(f"Error in callback: {e}")

    def __start_thread(self, func: callable):
        th = threading.Thread(target=func, daemon=True)
        th.start()
        return th
    
    def __close(self):
        self.__stop_open_cam_event.set()
        # self.__read_frame_function=None
        self.__stop_read_buffer_event.set()
        if self.__thread_read_buffer is not None:
            self.__thread_read_buffer.join()

        self.__stop_get_frame_event.set()
        if self.__thread_get_frame is not None:
            self.__thread_get_frame.join()
            self.__thread_get_frame = None

        self.__stop_open_cam_event.set()
        if self.__thread_open_cam is not None:
            self.__thread_open_cam.join()

        if self.__cam is not None:
            self.__cam.release()
            self.__cam = None
            self.__is_cam_opened=False
        print('cam closed')


    # **********************************************************
    # public function
    # **********************************************************
    def bind(self, mode: Literal["open_cam", "read_frame"], func: callable):
        if mode == "open_cam":
            self.__open_cam_callback = func
        if mode == "read_frame":
            self.__read_frame_function = func

    def close(self):
        try:
            self.__start_thread(self.__close)
        except:
            pass

    def read(self) -> cv2.Mat:
        if self.__cam is None:
            return None

        if time.time() - self.__fps_display_time >= 1.0:
            self.__fps = self.__frame_count
            self.__frame_count = 0
            self.__fps_display_time = time.time()
        self.__frame_count += 1

        target_duration = 1 / self.__settings.framerate
        while True:
            elapsed = time.time() - self.__start
            if elapsed >= target_duration:
                break
            if self.__stop_get_frame_event.wait(0.001):
                return None
        self.__start = time.time()

        while self.__cam:
            ret, image = self.__cam.retrieve()
            if ret:
                return image
            if self.__stop_get_frame_event.wait(0.01):
                return None
        return None

    def wait_open_cam(self):
        while not self.__is_cam_opened:
            time.sleep(0.1)

    def start_get_frame(self):
        self.__stop_get_frame_event.clear()
        self.__thread_get_frame = self.__start_thread(self.__start_get_frame)

    def stop_get_frame(self):
        self.__stop_get_frame_event.set()
        if self.__thread_get_frame is not None:
            self.__thread_get_frame.join()
        self.__thread_get_frame = None

    def get_callback(self):
        return [self.__open_cam_callback,self.__read_frame_function]



