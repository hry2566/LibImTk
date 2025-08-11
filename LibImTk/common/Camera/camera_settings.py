import re
import subprocess
import cv2
from LibImTk.common.timer_ex import TimerEx

class CameraSettings:
    V4W2_PATH = f'./LibImTk/common/Camera/lib/v4w2-ctl.exe'

    def __init__(self, path_settings: str = None):
        self.device_number: int = 0
        self.resolution: tuple = (640, 480)
        self.framerate: int = 10
        self.__camera_devices: dict = None
        self.__v4w2_ctrls_menus: dict = None
        self.__mjpeg_formats: dict = None

        if path_settings is not None:
            self.load_file(path_settings)

        if self.camera_devices.get(f'/dev/video{self.device_number}') is None:
            self.device_number = 0

    @property
    def v4w2_ctls_menus(self) -> dict:
        self.__v4w2_ctrls_menus = self.__get_v4w2_ctrs_menus()
        return self.__v4w2_ctrls_menus

    @v4w2_ctls_menus.setter
    def v4w2_ctls_menus(self, value: dict):
        self.__v4w2_ctrls_menus = value

    @property
    def camera_devices(self) -> dict:
        self.__camera_devices = self.__get_camera_devices()
        return self.__camera_devices

    @property
    def mjpeg_formats(self) -> dict:
        self.__mjpeg_formats = self.__get_v4w2_formats_ext()
        return self.__mjpeg_formats

    def __get_v4w2_ctrs_menus(self, args: list = ['-L']) -> dict:
        try:
            # print([self.V4W2_PATH, '-d', f'/dev/video{self.device_number}'] + args)
            result = subprocess.run(
                [self.V4W2_PATH, '-d', f'/dev/video{self.device_number}'] + args,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            output_lines = result.stdout.splitlines()
            params_dict = {}
            int_bool_pattern = re.compile(
                r'\s*([a-zA-Z0-9_-]+)\s+\((int|bool|menu)\)\s*:\s*(?:min=([-\d]+)\s+max=([-\d]+)\s+step=([-\d]+)\s+)?default=([-\w]+)\s+value=([-\w]+)'
            )
            menu_item_pattern = re.compile(r'^\s+(\d+):\s+(.+)')
            current_param_name = None
            for line in output_lines:
                match = int_bool_pattern.search(line)
                if match:
                    param_name = match.group(1).strip()
                    param_type = match.group(2)
                    param_details = {
                        'type': param_type,
                        'default': self.__convert_value(match.group(6), param_type),
                        'value': self.__convert_value(match.group(7), param_type)
                    }
                    if param_type in ('int', 'menu'):
                        param_details['min'] = int(match.group(3)) if match.group(3) else None
                        param_details['max'] = int(match.group(4)) if match.group(4) else None
                        param_details['step'] = int(match.group(5)) if match.group(5) else None
                    if param_type == 'menu':
                        param_details['menu'] = {}
                        current_param_name = param_name
                    else:
                        current_param_name = None
                    params_dict[param_name] = param_details
                elif current_param_name and line.strip():
                    menu_match = menu_item_pattern.search(line)
                    if menu_match:
                        menu_id = int(menu_match.group(1))
                        menu_label = menu_match.group(2).strip()
                        params_dict[current_param_name]['menu'][menu_id] = menu_label

            return params_dict
        except FileNotFoundError:
            print(f"Error: The executable file was not found at {self.V4W2_PATH}")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with return code {e.returncode}")
            print(f"Stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def __get_v4w2_formats_ext(self) -> dict:
        """
        v4l2-ctl --list-formats-ext の出力から、MJPEGフォーマットの解像度とフレームレートを取得します。
        出力例: {'1920x1080': '30.000 fps', '1280x1024': '30.000 fps', ...}
        """
        try:
            # print([self.V4W2_PATH, '-d', f'/dev/video{self.device_number}', '--list-formats-ext'])
            result = subprocess.run(
                [self.V4W2_PATH, '-d', f'/dev/video{self.device_number}', '--list-formats-ext'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )

            output_lines = result.stdout.splitlines()
            mjpeg_formats = {}
            in_mjpeg_section = False

            for line in output_lines:
                # MJPG セクションの開始検出
                if "[0]: 'MJPG'" in line:
                    in_mjpeg_section = True
                    continue

                # 次のフォーマットセクションに入ったら終了
                if in_mjpeg_section and line.strip().startswith("[") and "'MJPG'" not in line:
                    break

                if in_mjpeg_section:
                    size_match = re.search(r'Size:\s+Discrete\s+(\d+x\d+)', line)
                    if size_match:
                        current_size = size_match.group(1)
                        continue  # 次の行に Interval があるので待つ

                    interval_match = re.search(r'Interval:\s+Discrete\s+[\d.]+s\s+\(([\d.]+)\s+fps\)', line)
                    if interval_match and current_size:
                        fps = interval_match.group(1)
                        mjpeg_formats[current_size] = f"{fps} fps"

            return mjpeg_formats

        except FileNotFoundError:
            print(f"Error: The executable file was not found at {self.V4W2_PATH}")
            return {}
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with return code {e.returncode}")
            print(f"Stderr: {e.stderr}")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}


    def __convert_value(self, value_str: str, value_type: str):
        if value_str is None:
            return None
        value_str = value_str.strip()
        if value_type == 'int':
            return int(value_str)
        elif value_type == 'bool':
            return value_str.lower() in ('1', 'true')
        elif value_type == 'menu':
            return int(value_str) if value_str.isdigit() else value_str
        return value_str

    def __get_camera_devices(self, args=['--list-devices']):
        try:
            result = subprocess.run(
                [self.V4W2_PATH] + args,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            output_lines = result.stdout.splitlines()
            devices = {}
            current_device_name = None
            device_name_pattern = re.compile(r'(.+):')
            device_path_pattern = re.compile(r'^\s*(/dev/video\d+)')
            for line in output_lines:
                name_match = device_name_pattern.search(line)
                if name_match:
                    current_device_name = name_match.group(1).strip()
                    continue
                path_match = device_path_pattern.search(line)
                if path_match and current_device_name:
                    device_path = path_match.group(1).strip()
                    devices[device_path] = current_device_name
                    current_device_name = None
            return devices
        except FileNotFoundError:
            print(f"Error: The executable file was not found at {self.V4W2_PATH}")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with return code {e.returncode}")
            print(f"Stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    def __set_v4w2_ctl(self, params: dict):
        """
        v4w2-ctlを使用してカメラの設定を適用します。
        
        Args:
            params (dict): {パラメータ名: 値} の形式の辞書。
                            例: {'whitebalance_automatic': 1, 'brightness': 128}
        """
        try:
            args = ['-d', f'/dev/video{self.device_number}']
            for key, value in params.items():
                args.extend(['-c', f'{key}={value}'])
            
            result = subprocess.run(
                [self.V4W2_PATH] + args,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )       
        except FileNotFoundError:
            print(f"Error: The executable file was not found at {self.V4W2_PATH}")
        except subprocess.CalledProcessError as e:
            print(f"Error: Command failed with return code {e.returncode}")
            print(f"Stderr: {e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def load_file(self, filename):
        pass

    def save_file(self, filename):
        pass

    def apply_setting(self, cam: cv2.VideoCapture, item_name: str, value: int, scale_finder:callable=None):
        if item_name == 'brightness':
            cam.set(cv2.CAP_PROP_BRIGHTNESS, value)
        elif item_name == 'contrast':
            cam.set(cv2.CAP_PROP_CONTRAST, value)
        elif item_name == 'hue':
            cam.set(cv2.CAP_PROP_HUE, value)
        elif item_name == 'saturation':
            cam.set(cv2.CAP_PROP_SATURATION, value)
        elif item_name == 'sharpness':
            cam.set(cv2.CAP_PROP_SHARPNESS, value)
        elif item_name == 'gamma':
            cam.set(cv2.CAP_PROP_GAMMA, value)
        elif item_name == 'whitebalance_automatic':
            self.__set_v4w2_ctl({'whitebalance_automatic': 1}) 
            if value == 0 and scale_finder:
                whitebalance = scale_finder('whitebalance').get()
                cam.set(cv2.CAP_PROP_TEMPERATURE, whitebalance)
                TimerEx().after(100, lambda : cam.set(cv2.CAP_PROP_TEMPERATURE, whitebalance))
        elif item_name == 'whitebalance':
            cam.set(cv2.CAP_PROP_TEMPERATURE, value)
            if scale_finder:
                scale_finder('whitebalance_automatic').set(0, False)
        elif item_name == 'backlight-compensation':
            cam.set(cv2.CAP_PROP_BACKLIGHT, value)
        elif item_name == 'gain':
            cam.set(cv2.CAP_PROP_GAIN, value)
        elif item_name == 'exposure_automatic':
            cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, value)
            if value == 0 and scale_finder:
                exposure = scale_finder('exposure').get()
                cam.set(cv2.CAP_PROP_EXPOSURE, exposure)
                TimerEx().after(100, lambda : cam.set(cv2.CAP_PROP_EXPOSURE, exposure))
        elif item_name == 'exposure':
            cam.set(cv2.CAP_PROP_EXPOSURE, value)
            if scale_finder:
                scale_finder('exposure_automatic').set(0, False)
        elif item_name == 'focus_automatic':
            cam.set(cv2.CAP_PROP_AUTOFOCUS, value)
            if value == 0 and scale_finder:
                focus = scale_finder('focus').get()
                cam.set(cv2.CAP_PROP_FOCUS, focus)
                TimerEx().after(100, lambda : cam.set(cv2.CAP_PROP_FOCUS, focus))
        elif item_name == 'focus':
            cam.set(cv2.CAP_PROP_FOCUS, value)
            if scale_finder:
                scale_finder('focus_automatic').set(0, False)
        elif item_name == 'pan':
            cam.set(cv2.CAP_PROP_PAN, value)
        elif item_name == 'tilt':
            cam.set(cv2.CAP_PROP_TILT, value)
        elif item_name == 'zoom':
            cam.set(cv2.CAP_PROP_ZOOM, value)

    def apply_resolution(self, cam: cv2.VideoCapture):
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        print('apply_resolution')