from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from LibImTk import ImshowCustom

class UIWidget:
    def __init__(self, imshow_custom_instance:ImshowCustom):
        self.__imshow_custom = imshow_custom_instance

    def _set_status_value(self):
        scale = format(self.__imshow_custom._view_scale, '.2f')
        curPos = self.get_cursor_pos()
        info_txt = '(Scaling:ctrl+wheel, Move:ctrl+wheel_D&D, Reset:ctrl+right_click)'
        self.__imshow_custom.statusbar["text"] = f'scale: {scale} curPos: {curPos} {info_txt}'

    def _get_canvas_size(self):
        self.__imshow_custom.mainwindow.update()
        canvas_width = int(
            self.__imshow_custom.img_view.winfo_width() * self.__imshow_custom._view_scale)
        canvas_height = int(
            self.__imshow_custom.img_view.winfo_height() * self.__imshow_custom._view_scale)
        return canvas_width, canvas_height

    def get_cursor_pos(self):
        scale_inv = 1.0 / self.__imshow_custom._image_scale
        posx = (self.__imshow_custom._mouse_x - self.__imshow_custom._imgpos_x) * scale_inv
        posy = (self.__imshow_custom._mouse_y - self.__imshow_custom._imgpos_y) * scale_inv
        return int(posx), int(posy)