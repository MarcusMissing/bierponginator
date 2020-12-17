from time import sleep

import RPi.GPIO as GPIO
from numpy.testing._private.parameterized import param

import KI.config as config

MOTOR_Z = {"dir_pins": [20],
           "motor_pins": [21]}

MOTOR_X = {"dir_pins": [26, 12],
           "motor_pins": [19, 16]}

CW = 0
CCW = 1


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    for pin in [MOTOR_Z["dir_pins"], MOTOR_Z["motor_pins"], MOTOR_X["dir_pins"], MOTOR_X["motor_pins"]]:
        GPIO.setup(pin, GPIO.OUT)


def motor_test(DIR_pin, DIR, STEP_pin, steps, delay):
    GPIO.output(DIR_pin, DIR)
    for x in range(steps):
        GPIO.output(STEP_pin, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_pin, GPIO.LOW)
        sleep(delay)


def ramp_motor(motor, direction, nm_steps, sps):
    for direction_pin in motor["dir_pins"]:
        GPIO.output(direction_pin, direction)
    for x in range(1, nm_steps):
        delay = 1 / (sps * (1 / (nm_steps - x)))

        for motor_pin in motor["motor_pins"]:
            GPIO.output(motor_pin, GPIO.HIGH)

        sleep(delay)
        for motor_pin in motor["motor_pins"]:
            GPIO.output(motor_pin, GPIO.LOW)

        sleep(delay)


init_GPIO()

# motor_test(config.DIR_1, config.CW, config.STEP_1, steps=50, delay=.005)
# motor_test(config.DIR_1, config.CCW, config.STEP_1, steps=50, delay=.005)

# motor_test(config.DIR_2, config.CW, config.STEP_2, steps=50, delay=.001)
# motor_test(config.DIR_2, config.CCW, config.STEP_2, steps=50, delay=.002)

ramp_motor(MOTOR_X, CW, 60, 80000)
ramp_motor(MOTOR_X, CCW, 60, 80000)

GPIO.cleanup()
