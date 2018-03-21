from webcolors import name_to_rgb, IntegerRGB
from time import sleep

class LedRGB(object):
    def __init__(self, dbg, red_pin, green_pin, blue_pin):
        self.dbg = dbg
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

    def write_rgb(self, rgb):
        self.dbg.analog_write(self.red_pin, rgb.red)
        self.dbg.analog_write(self.green_pin, rgb.green)
        self.dbg.analog_write(self.blue_pin, rgb.blue)

    def set_color(self, colorname, duration=0.5):
        rgb = name_to_rgb(colorname)
        self.write_rgb(rgb)
        if duration != 0:
            sleep(duration)
            self.clear()

    def clear(self):
        rgb = IntegerRGB(0, 0, 0)
        self.write_rgb(rgb)
