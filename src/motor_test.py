from time import sleep
import RPi.GPIO as GPIO

DIR_1 = 20
STEP_1 = 21
DIR_2 = 26
STEP_2 = 19
CW = 0
CCW = 1
SPR = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)
GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)
GPIO.output(DIR_1, CW)

step_count = SPR
delay_CW = .0005
delay_CCW = .0005

for x in range(step_count):
    GPIO.output(STEP_1, GPIO.HIGH)
    sleep(delay_CW)
    GPIO.output(STEP_1, GPIO.LOW)
    sleep(delay_CW)

sleep(.5)
GPIO.output(DIR_1, CCW)
for x in range(step_count):
    GPIO.output(STEP_1, GPIO.HIGH)
    sleep(delay_CCW)
    GPIO.output(STEP_1, GPIO.LOW)
    sleep(delay_CCW)

sleep(1)

GPIO.output(DIR_2, CW)
for x in range(step_count):
    GPIO.output(STEP_2, GPIO.HIGH)
    sleep(delay_CW)
    GPIO.output(STEP_2, GPIO.LOW)
    sleep(delay_CW)

sleep(.5)
GPIO.output(DIR_2, CCW)
for x in range(step_count):
    GPIO.output(STEP_2, GPIO.HIGH)
    sleep(delay_CCW)
    GPIO.output(STEP_2, GPIO.LOW)
    sleep(delay_CCW)

GPIO.cleanup()
