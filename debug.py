import serial
import struct
from time import sleep

BAUD_RATE = 9600
OUT_MODE = 8
IN_MODE = 4
ANALOG_MODE = 2
DIGITAL_MODE = 1

class Command(object):
    def __init__(self, type_id, val1, val2=0):
        self.type_id = type_id << 4
        self.val1 = val1
        self.val2 = val2

    def pack(self):
        return struct.pack('>BBH', self.type_id, self.val1, self.val2)

class WriteDigital(Command):
    def __init__(self, pin_num, value):
        super(__class__, self).__init__(OUT_MODE | DIGITAL_MODE, pin_num, value)
        self.pin_num = pin_num
        self.value = value

class WriteAnalog(Command):
    def __init__(self, pin_num, value):
        super(__class__, self).__init__(OUT_MODE | ANALOG_MODE, pin_num, value)
        self.pin_num = pin_num
        self.value = value

class ReadDigital(Command):
    def __init__(self, pin_num):
        super(__class__, self).__init__(IN_MODE | DIGITAL_MODE, pin_num)
        self.pin_num = pin_num

class ReadAnalog(Command):
    def __init__(self, pin_num):
        super(__class__, self).__init__(IN_MODE | ANALOG_MODE, pin_num)
        self.pin_num = pin_num

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
        assert value in range(0, 1024)
        cmd = WriteAnalog(pin, value)
        return self.run_command(cmd)

    def digital_read(self, pin):
        cmd = ReadDigital(pin)
        output = self.run_command(cmd)
        lines = output.decode('ascii').split('\r\n')
        result = [x.split(': ')[1] for x in lines if 'read: ' in x][0]
        return int(result)

    def analog_read(self, pin):
        cmd = ReadAnalog(pin)
        output = self.run_command(cmd)
        lines = output.decode('ascii').split('\r\n')
        result = [x.split(': ')[1] for x in lines if 'read: ' in x][0]
        return int(result)
