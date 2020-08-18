from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 0     # Clockwise Rotation
CCW = 1    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = SPR
delay_CW = .00001
delay_CCW = .0005

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay_CW)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay_CW)
    print(x)

sleep(.5)
GPIO.output(DIR, CCW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay_CCW)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay_CCW)

GPIO.cleanup()