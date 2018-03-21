import serial
import struct
from time import sleep

s =  serial.Serial

BAUD_RATE = 9600
OUT_MODE = 8
IN_MODE = 4
ANALOG_MODE = 2
DIGITAL_MODE = 1

class Command(object):
    def build(self):
        raise NotImplementedError()

    def pack(self):
        return struct.pack('>I', self.build())

class WriteDigital(Command):
    def __init__(self, pin_num, value):
        self.pin_num = pin_num
        self.value = value

    def build(self):
        res = OUT_MODE | DIGITAL_MODE
        res <<= 28
        res |= (self.pin_num << 8)
        res |= (self.value)
        return res

class WriteAnalog(Command):
    def __init__(self, pin_num, value):
        self.pin_num = pin_num
        self.value = value

    def build(self):
        res = OUT_MODE | ANALOG_MODE
        res <<= 28
        res |= (self.pin_num << 8)
        res |= (self.value)
        return res

class ReadDigital(Command):
    def __init__(self, pin_num):
        self.pin_num = pin_num

    def build(self):
        res = IN_MODE | DIGITAL_MODE
        res <<= 28
        res |= (self.pin_num << 8)
        return res

class ReadAnalog(Command):
    def __init__(self, pin_num):
        self.pin_num = pin_num

    def build(self):
        res = IN_MODE | ANALOG_MODE
        res <<= 28
        res |= (self.pin_num << 8)
        return res

class Debugger(object):
    def __init__(self, tty="/dev/ttyACM0"):
        self.serial = serial.Serial(tty, BAUD_RATE)

    def __del__(self):
        self.serial.close()

    def run_command(self, command):
        self.serial.write(command.pack())
        sleep(0.05)
        return self.serial.read_all()

    def digital_write(self, pin, value):
        assert value in (1,0)
        cmd = WriteDigital(pin, value)
        return self.run_command(cmd)

    def analog_write(self, pin, value):
        assert value in range(0, 256)
        cmd = WriteAnalog(pin, value)
        return self.run_command(cmd)

    def digital_read(self, pin):
        cmd = ReadDigital(pin)
        output = self.run_command(cmd)
        return output

    def analog_read(self, pin):
        cmd = ReadAnalog(pin)
        output = self.run_command(cmd)
        return output
