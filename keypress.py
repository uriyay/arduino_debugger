from subprocess import Popen, PIPE

control_f4_sequence = b'''keydown Control_L
key F4
keyup Control_L
'''

shift_a_sequence = b'''keydown Shift_L
key A
keyup Shift_L
'''

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)
