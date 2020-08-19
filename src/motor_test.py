from time import sleep
import RPi.GPIO as GPIO

DIR_1 = 20
STEP_1 = 21
DIR_2 = 26
STEP_2 = 19
CW = 0
CCW = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)
GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)


def motor_test(DIR_pin, DIR, STEP_pin, steps, delay):
    GPIO.output(DIR_pin, DIR)
    for x in range(steps):
        GPIO.output(STEP_pin, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_pin, GPIO.LOW)
        sleep(delay)


motor_test(DIR_1, CW, STEP_1, steps=50, delay=.005)
motor_test(DIR_1, CCW, STEP_1, steps=50, delay=.005)

motor_test(DIR_2, CW, STEP_2, steps=50, delay=.001)
motor_test(DIR_2, CCW, STEP_2, steps=50, delay=.002)

GPIO.cleanup()
