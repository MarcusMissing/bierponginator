from time import sleep
import itertools
import RPi.GPIO as GPIO
import numpy as np
import KI.config as config

MOTOR_Z = {"dir_pins": [20],
           "motor_pins": [21]}

MOTOR_X = {"dir_pins": [26, 12],
           "motor_pins": [19, 16]}

CW = 0
CCW = 1


def test_motor(motor,
               direction,
               nm_steps,
               sps,
               use_ramp=True,
               return_to_start=True):
    GPIO.setmode(GPIO.BCM)
    pins = list(itertools.chain.from_iterable([motor[key] for key in motor.keys()]))
    GPIO.setup(pins, GPIO.OUT)
    print("initialized pins: {}".format(pins))

    GPIO.output(motor["dir_pins"], direction)

    if use_ramp:
        delays = []

        for x in range(1, nm_steps):
            delay = (nm_steps - x) / sps
            delays.append(delay)
            GPIO.output(motor["motor_pins"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor["motor_pins"], GPIO.LOW)
            sleep(delay)
        print("Used ramp values: {}".format(delays))

    else:
        for x in range(1, nm_steps):
            delay = 1 / sps
            GPIO.output(motor["motor_pins"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor["motor_pins"], GPIO.LOW)
            sleep(delay)

    if return_to_start:
        test_motor(motor,
                   int(np.logical_not(direction)),
                   nm_steps,
                   sps,
                   use_ramp,
                   return_to_start=False)
    GPIO.cleanup()


test_motor(MOTOR_X, CW, 60, 80000)
