#! /usr/local/rpi_home/python3/bin/python3

from DFRobot_GP8403 import DFRobot_GP8403,OUTPUT_RANGE_10V
from bedrock_cgi import ServiceBase
import RPi.GPIO as GPIO
from time import sleep


UNUSED = 11
HEATER = 13
PUMP = 15

# we look for this text, but false input is True to the GPIO
FALSE = [False, "false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF"]
TRUE = [True, "true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"]


# the simple event "ok"
def event_ok(event):
    event.ok({"OK": "OK"})


# the hass event
def handle_hass(event):
    query = event.query
    # hass events will have a driver and data
    # so... driver = switch, data = target_state

    pass


# the mqtt event
def handle_mqtt(event):
    query = event.query
    # mqtt events will have a server address, username, and password
    # TODO, should the password be encrypted? The TLS connection will prevent it from being clear-
    #       text on the open network
    pass


# a prototype light event
def handle_light(event):
    dac = DFRobot_GP8403(0x5f)
    while dac.begin() != 0:
        sleep(1)
    dac.set_DAC_outrange(OUTPUT_RANGE_10V)
    dac.set_DAC_out_voltage(int(float(event.query["brightness"])) * 100, 0)
    dac.set_DAC_out_voltage(int(float(event.query["color"])) * 100, 1)
    event_ok(event)


def do_gpio(pin: int, state: bool):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(state)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)


ServiceBase.respond()
