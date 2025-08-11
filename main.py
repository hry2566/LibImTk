
from LibImTk import ImshowCustom,Camera,CameraSettings

def test(event, x, y):
    print(event, x, y)

def test2(event):
    print(event)


if __name__ == "__main__":
    app = ImshowCustom()
    settings = CameraSettings()
    settings.device_number = 1
    # settings.resolution = (3840, 2160)
    settings.resolution = (1920, 1080)
    settings.framerate = 10
    cam = Camera(settings)

    app.bind('<mouse_action>', test)
    app.bind('<keyboard_action>', test2) 

    elapsed_time = 0
    while True:
        img = cam.read() 
        app.imshow(cam.fps, img)
        key = app.waitKey(1)
        if key == 113:
            break



