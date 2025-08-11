from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from LibImTk import ImshowCustom

from time import sleep


class EventManager:
    EVENT_MOUSEMOVE = 0
    EVENT_LBUTTONDOWN = 1
    EVENT_LBUTTONUP = 2
    EVENT_RBUTTONDOWN = 3
    EVENT_RBUTTONUP = 4
    EVENT_WHEELDOWN = 5
    EVENT_WHEELUP = 6
    EVENT_WHEEL_CLICKUP = 7
    EVENT_WHEEL_CLICKDOWN = 8

    def __init__(self, imshow_custom_instance: ImshowCustom):
        self.__imshow_custom = imshow_custom_instance
        self.__start_x = 0
        self.__start_y = 0

    def _handle_mouse_event(self, event_code, x, y):
        if self.__imshow_custom._func_onmouse is None:
            return
        x = int(x / self.__imshow_custom._image_scale - self.__imshow_custom._imgpos_x / self.__imshow_custom._image_scale)
        y = int(y / self.__imshow_custom._image_scale - self.__imshow_custom._imgpos_y / self.__imshow_custom._image_scale)
        self.__imshow_custom._func_onmouse(event_code, x, y)

    def _handle_key_event(self, event):
        if self.__imshow_custom._func_onkeyboard is None:
            return
        self.__imshow_custom._func_onkeyboard(event)

    def _on_mouse_left_up(self, event):
        self._handle_mouse_event(self.EVENT_LBUTTONUP, event.x, event.y)

    def _on_mouse_right_up(self, event):
        self._handle_mouse_event(self.EVENT_RBUTTONUP, event.x, event.y)

    def _on_mouse_left_down(self, event):
        self._handle_mouse_event(self.EVENT_LBUTTONDOWN, event.x, event.y)

    def _on_mouse_right_down(self, event):
        if self.__imshow_custom._ctrl_key:
            self.__imshow_custom._view_scale = 1.0
            self.__imshow_custom._imgpos_x = 0
            self.__imshow_custom._imgpos_y = 0
            self.__imshow_custom._calc_scale()
            self.__imshow_custom._draw(None)
        else:
            self._handle_mouse_event(self.EVENT_RBUTTONDOWN, event.x, event.y)

    def _on_mouse_move(self, event):
        self.__imshow_custom._mouse_x = event.x
        self.__imshow_custom._mouse_y = event.y
        self.__imshow_custom._set_status_value()
        self._handle_mouse_event(self.EVENT_MOUSEMOVE, event.x, event.y)

    def _click_close(self):
        pass

    def _on_key_release(self, event):
        self._handle_key_event(event)
        if event.keysym == 'Control_L':
            self.__imshow_custom._ctrl_key = False
        else:
            self.__imshow_custom._key_flag = False
            self.__imshow_custom._key = 0
        sleep(0.01)

    def _on_key(self, event):
        self._handle_key_event(event)
        if self.__imshow_custom._key_flag:
            return
        if event.keysym == 'Control_L':
            self.__imshow_custom._ctrl_key = True
        else:
            try:
                self.__imshow_custom._key_flag = True
                self.__imshow_custom._key = ord(event.keysym)
            except Exception:
                pass
        sleep(0.01)

    def _mouse_wheel_down(self, event):
        if self.__imshow_custom._ctrl_key:
            self.__start_x = event.x
            self.__start_y = event.y
        else:
            self._handle_mouse_event(self.EVENT_WHEEL_CLICKDOWN, event.x, event.y)

    def _mouse_wheel_up(self, event):
        if self.__imshow_custom._ctrl_key:
            self.__imshow_custom._imgpos_x -= self.__start_x - event.x
            self.__imshow_custom._imgpos_y -= self.__start_y - event.y
            self.__imshow_custom._draw(None)
        else:
            self._handle_mouse_event(self.EVENT_WHEEL_CLICKUP, event.x, event.y)

    def _mouse_wheel(self, event):
        wheel = True
        if self.__imshow_custom._os_type == 'Windows':
            wheel = event.delta > 0
        elif self.__imshow_custom._os_type == 'Linux':
            wheel = event.num == 4

        if self.__imshow_custom._ctrl_key:
            # 拡縮前のマウスカーソル位置での元画像上の座標を計算
            # img_x, img_y は元画像におけるピクセル座標
            img_x = (event.x - self.__imshow_custom._imgpos_x) / self.__imshow_custom._image_scale
            img_y = (event.y - self.__imshow_custom._imgpos_y) / self.__imshow_custom._image_scale
            
            # スケール変更
            # prev_scale = self.__imshow_custom._view_scale
            self.__imshow_custom._view_scale *= 1.1 if wheel else 0.9
            if self.__imshow_custom._view_scale < 0.1:
                self.__imshow_custom._view_scale = 0.1
            
            self.__imshow_custom._calc_scale() # image_scale を更新
            new_scale = self.__imshow_custom._image_scale

            # 新しいスケールでの画像上の点と、マウスカーソル位置が一致するように imgpos を調整
            self.__imshow_custom._imgpos_x = event.x - img_x * new_scale
            self.__imshow_custom._imgpos_y = event.y - img_y * new_scale
            
            self.__imshow_custom._draw(None)
        else:
            event_code = self.EVENT_WHEELUP if wheel else self.EVENT_WHEELDOWN
            self._handle_mouse_event(event_code, 0, 0)
        self.__imshow_custom._set_status_value()

    def _on_resize(self, event):
        self.__imshow_custom._calc_scale()
        self.__imshow_custom._draw(None)