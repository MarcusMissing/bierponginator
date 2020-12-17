from time import sleep

import RPi.GPIO as GPIO
from numpy.testing._private.parameterized import param

import KI.config as config

CW_PIN = 20
Motor_Z = 21
CCW_PIN = 26
Motor_X = 19
CW = 0
CCW = 1

pi = True


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CW_PIN, GPIO.OUT)
    GPIO.setup(Motor_Z, GPIO.OUT)
    GPIO.setup(CCW_PIN, GPIO.OUT)
    GPIO.setup(Motor_Z, GPIO.OUT)


def motor_test(DIR_pin, DIR, STEP_pin, steps, delay):
    GPIO.output(DIR_pin, DIR)
    for x in range(steps):
        GPIO.output(STEP_pin, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_pin, GPIO.LOW)
        sleep(delay)


def ramp_motor(direction_pin, direction, motor_pin, steps, sps):
    print("Set Steps per Second to: {}".format(sps))
    GPIO.output(direction_pin, direction)
    for x in range(1, steps):
        GPIO.output(motor_pin, GPIO.HIGH)
        delay = 1/(sps*(1/(steps-x)))
        sleep(delay)
        GPIO.output(motor_pin, GPIO.LOW)
        sleep(delay)


init_GPIO()

# motor_test(config.DIR_1, config.CW, config.STEP_1, steps=50, delay=.005)
# motor_test(config.DIR_1, config.CCW, config.STEP_1, steps=50, delay=.005)

# motor_test(config.DIR_2, config.CW, config.STEP_2, steps=50, delay=.001)
# motor_test(config.DIR_2, config.CCW, config.STEP_2, steps=50, delay=.002)

ramp_motor(CCW_PIN, CCW, Motor_X, 60, 1000)

GPIO.cleanup()
