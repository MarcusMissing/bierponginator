from time import sleep

import RPi.GPIO as GPIO

import KI.config as config


def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.DIR_1, GPIO.OUT)
    GPIO.setup(config.STEP_1, GPIO.OUT)
    GPIO.setup(config.DIR_2, GPIO.OUT)
    GPIO.setup(config.STEP_2, GPIO.OUT)


def motor_test(DIR_pin, DIR, STEP_pin, steps, delay):
    GPIO.output(DIR_pin, DIR)
    for x in range(steps):
        GPIO.output(STEP_pin, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_pin, GPIO.LOW)
        sleep(delay)


init_GPIO()

motor_test(config.DIR_1, config.CW, config.STEP_1, steps=50, delay=.005)
motor_test(config.DIR_1, config.CCW, config.STEP_1, steps=50, delay=.005)

motor_test(config.DIR_2, config.CW, config.STEP_2, steps=50, delay=.001)
motor_test(config.DIR_2, config.CCW, config.STEP_2, steps=50, delay=.002)

GPIO.cleanup()
