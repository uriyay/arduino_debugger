#tuples of (gfedcba, abcdefg)
NUMBER = {
        0: (0x3f, 0x7e),
        1: (0x06, 0x30),
        2: (0x5b, 0x6d),
        3: (0x4f, 0x79),
        4: (0x66, 0x33),
        5: (0x6d, 0x5b),
        6: (0x7d, 0x5f),
        7: (0x07, 0x70),
        8: (0x7f, 0x7f),
        9: (0x6f, 0x7b),
        10: (0x77, 0x77),
        11: (0x7c, 0x1f),
        12: (0x39, 0x4e),
        13: (0x5e, 0x3d),
        14: (0x79, 0x4f),
        15: (0x71, 0x47),
        }

class SegmentDisplay(object):
    def __init__(self, debugger, *ports):
        '''
        the order of the ports needs to be:
        dot, and right way
        then from left to right - the other side

        The order on the circut looks like:
        dot, c, GND, d, e
        b, a, GND, f, g
        '''
        self.ports = ports
        self.d = debugger

    def _write(self, *values):
        for value,port in zip(values, self.ports):
            self.d.digital_write(port, value)

    def to_binary(self, number, width):
        result = ''
        for i in range(width):
            result = str(number & 1) + result
            number >>= 1
        return result

    def write(self, number):
        if number not in NUMBER:
            raise Exception('Invalid number %d to display' % (number))
        #just the same represantion forward and backward
        gfedcba, abcdefg = NUMBER[number]
        g,f,e,d,c,b,a = [int(x) for x in self.to_binary(gfedcba, 7)]
        dot = 0 #turn off always
        self._write(dot,c,d,e,
                #the other side of the segment display:
                b,a,f,g)

    def clear(self):
        self._write(0,0,0,0,0,0,0,0)
