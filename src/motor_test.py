from time import sleep

import RPi.GPIO as GPIO
from numpy.testing._private.parameterized import param

import KI.config as config

MOTOR_Z_DIR_PIN = 20
Motor_Z = 21
MOTOR_X_DIR_PIN = 26
Motor_X = 19
CW = 0
CCW = 1


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_Z_DIR_PIN, GPIO.OUT)
    GPIO.setup(Motor_Z, GPIO.OUT)
    GPIO.setup(MOTOR_X_DIR_PIN, GPIO.OUT)
    GPIO.setup(Motor_X, GPIO.OUT)


def motor_test(DIR_pin, DIR, STEP_pin, steps, delay):
    GPIO.output(DIR_pin, DIR)
    for x in range(steps):
        GPIO.output(STEP_pin, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_pin, GPIO.LOW)
        sleep(delay)


def ramp_motor(direction_pin, direction, motor_pin, nm_steps, sps):
    print("Set Steps per Second to: {}".format(sps))
    GPIO.output(direction_pin, direction)
    for x in range(1, nm_steps):
        GPIO.output(motor_pin, GPIO.HIGH)
        delay = 1/(sps * (1 / (nm_steps - x)))
        sleep(delay)
        GPIO.output(motor_pin, GPIO.LOW)
        sleep(delay)


init_GPIO()

# motor_test(config.DIR_1, config.CW, config.STEP_1, steps=50, delay=.005)
# motor_test(config.DIR_1, config.CCW, config.STEP_1, steps=50, delay=.005)

# motor_test(config.DIR_2, config.CW, config.STEP_2, steps=50, delay=.001)
# motor_test(config.DIR_2, config.CCW, config.STEP_2, steps=50, delay=.002)

ramp_motor(MOTOR_X_DIR_PIN, CW, Motor_X, 60, 1000)

GPIO.cleanup()
