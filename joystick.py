from time import sleep
import keypress

class Joystick(object):
    def __init__(self, debugger, vx, vy, sw):
        self.vx = vx
        self.vy = vy
        self.sw = sw
        self.d = debugger

    def get_xy(self):
        x = self.d.analog_read(self.vx)
        y = self.d.analog_read(self.vy)
        return x,y

    def monitor(self, callback):
        while True:
            x,y = self.get_xy()
            callback(x,y)
            sleep(0.01)

    def callback(self, x, y):
        # print((x,y))
        if y > 625:
            print('up')
            keypress.keypress(b'keydown Up\nkeyup Up\n')
        elif y < 375:
            print('down')
            keypress.keypress(b'keydown Down\nkeyup Down\n')
        if x > 325:
            print('left')
            keypress.keypress(b'keydown Left\nkeyup Left\n')
        elif x < 75:
            print('right')
            keypress.keypress(b'keydown Right\nkeyup Right\n')
