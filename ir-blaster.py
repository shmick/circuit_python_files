from time import sleep
import pulseio
import board
import adafruit_irremote
from digitalio import DigitalInOut, Direction, Pull

"""
Adapted from: https://core-electronics.com.au/tutorials/Circuit_Playground_Express_TV_Remote.html

Uses the onboard IR transmitter on the Seeed Studio Wio Terminal 
"""

button_3 = DigitalInOut(board.BUTTON_3)
button_2 = DigitalInOut(board.BUTTON_2)
button_1 = DigitalInOut(board.BUTTON_1)
switch_p = DigitalInOut(board.SWITCH_PRESS)
switch_u = DigitalInOut(board.SWITCH_UP)
switch_d = DigitalInOut(board.SWITCH_DOWN)
switch_l = DigitalInOut(board.SWITCH_LEFT)
switch_r = DigitalInOut(board.SWITCH_RIGHT)

def nec_hex_to_int(string):
    """
    Take a 32bit NEC HEX code ie: 20DF10EF and split it into a 4 byte array [20, DF, 10, EF]
    Convert the HEX to Int [32, 223, 16, 239] and re-order them for use with the
    adafruit_irremote.GenericTransmit transmit function [223, 32, 239, 16]
    """
    n = 2
    out = [(string[i : i + n]) for i in range(0, len(string), n)]
    B1 = int(out[0], 16)
    B2 = int(out[1], 16)
    B3 = int(out[2], 16)
    B4 = int(out[3], 16)
    return [B2, B1, B4, B3]


# Create the relavent instances
PWM = pulseio.PWMOut(board.IR, frequency=38000, duty_cycle=2 ** 15)
# Defines the IR signal pwm for communication with 50% duty cycle
Pulse_Out = pulseio.PulseOut(PWM)
# Creates the output pulse instance
Signal_Encoder = adafruit_irremote.GenericTransmit(
    header=[9500, 4500], one=[550, 550], zero=[550, 1700], trail=0
)
# Defines NEC signals to be sent

Dev_LG = {
    "PWR_ON": "20DF23DC",
    "PWR_OFF": "20DFA35C",
    "PWR_TOG": "20DF10EF",
    "HDMI1": "20DF738C",
}

def transmit(dev, cmd):
    code = nec_hex_to_int(dev[cmd])
    Signal_Encoder.transmit(Pulse_Out, code)
    print(f"{cmd}: {code}")
    sleep(2)

while True:
    if not button_3.value:
        dev = Dev_LG
        cmd = "PWR_ON"
        transmit(dev, cmd)
    if not button_2.value:
        dev = Dev_LG
        cmd = "PWR_OFF"
        transmit(dev, cmd)
    if not button_1.value:
        dev = Dev_LG
        cmd = "HDMI1"
        transmit(dev, cmd)
    sleep(0.1)
