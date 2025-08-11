from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from LibImTk import ImshowCustom

import cv2
from PIL import Image, ImageTk

class Renderer:
    def __init__(self, imshow_custom_instance:ImshowCustom):
        self.__imshow_custom = imshow_custom_instance

    def _draw(self, *args):
        if self.__imshow_custom._origin_img is None:
            self.__imshow_custom.mainwindow.update()
            return

        canvas_width = self.__imshow_custom.img_view.winfo_width()
        canvas_height = self.__imshow_custom.img_view.winfo_height()

        # 現在の表示スケールを考慮した画像全体の仮想サイズ
        # scaled_img_width = int(self.__imshow_custom._origin_img.shape[1] * self.__imshow_custom._image_scale)
        # scaled_img_height = int(self.__imshow_custom._origin_img.shape[0] * self.__imshow_custom._image_scale)

        # キャンバスに表示される画像の左上座標（仮想座標系）
        # この仮想座標は、画像全体をスケーリングしたときの座標
        view_x_start = -self.__imshow_custom._imgpos_x
        view_y_start = -self.__imshow_custom._imgpos_y

        # 元画像からの切り取り範囲を計算 (ピクセル単位)
        # キャンバスの左上に対応する元画像のピクセル位置
        img_x1 = int(view_x_start / self.__imshow_custom._image_scale)
        img_y1 = int(view_y_start / self.__imshow_custom._image_scale)

        # キャンバスの右下に対応する元画像のピクセル位置
        img_x2 = int((view_x_start + canvas_width) / self.__imshow_custom._image_scale)
        img_y2 = int((view_y_start + canvas_height) / self.__imshow_custom._image_scale)

        # 切り取り範囲を画像の境界内に収める
        img_x1 = max(0, img_x1)
        img_y1 = max(0, img_y1)
        img_x2 = min(self.__imshow_custom._origin_img.shape[1], img_x2)
        img_y2 = min(self.__imshow_custom._origin_img.shape[0], img_y2)

        # 切り取り範囲が不正な場合（例：画像が完全に画面外にある）
        if img_x1 >= img_x2 or img_y1 >= img_y2:
            self.__imshow_custom.img_view.delete("all")
            self.__imshow_custom.img_view.update()
            self.__imshow_custom._busy_flag = False
            return

        # 画像を切り取る
        cropped_img = self.__imshow_custom._origin_img[img_y1:img_y2, img_x1:img_x2]

        # 切り取った画像をキャンバス上で表示する最終的なサイズ
        # 切り取った画像の幅/高さに、現在のimage_scaleを適用
        display_width = int(cropped_img.shape[1] * self.__imshow_custom._image_scale)
        display_height = int(cropped_img.shape[0] * self.__imshow_custom._image_scale)
        
        # リサイズ後のサイズが0にならないように保護
        if display_width == 0: display_width = 1
        if display_height == 0: display_height = 1

        img_to_display = cv2.resize(cropped_img, (display_width, display_height), interpolation=cv2.INTER_LINEAR)

        cv_image = cv2.cvtColor(img_to_display, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        # PhotoImageを更新または新規作成
        if self.__imshow_custom._canvas_img and \
           self.__imshow_custom._shape_size == img_to_display.shape:
            self.__imshow_custom._canvas_img.paste(pil_image)
        else:
            self.__imshow_custom._canvas_img = ImageTk.PhotoImage(image=pil_image)
            self.__imshow_custom._shape_size = img_to_display.shape

        # 描画位置の調整: 切り取った画像がキャンバス上でどこから始まるべきか
        # 元のimgpos_x/yは画像全体の左上を基準としているため、切り取られた部分の左上を基準にする
        render_x = self.__imshow_custom._imgpos_x + (img_x1 * self.__imshow_custom._image_scale)
        render_y = self.__imshow_custom._imgpos_y + (img_y1 * self.__imshow_custom._image_scale)
        
        self.__imshow_custom.img_view.delete("all")
        self.__imshow_custom.img_view.create_image(render_x, render_y, image=self.__imshow_custom._canvas_img, anchor='nw')
        self.__imshow_custom.img_view.update()
        self.__imshow_custom._busy_flag = False