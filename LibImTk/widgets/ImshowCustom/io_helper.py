from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from LibImTk import ImshowCustom

import os
import cv2
import numpy as np

class IOHelper:
    def __init__(self, imshow_custom_instance:ImshowCustom):
        pass

    def imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            np_file = np.fromfile(filename, dtype)
            img = cv2.imdecode(np_file, flags)
            return img
        except Exception as error:
            print(error)
            return None

    def imwrite(self, filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)

            if result:
                with open(filename, mode='w+b') as file:
                    n.tofile(file)
                return True
            return False
        except Exception as error:
            print(error)
            return False