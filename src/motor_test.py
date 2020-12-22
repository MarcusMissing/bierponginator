from time import sleep
import itertools
import RPi.GPIO as GPIO
import numpy as np
import pigpio

MOTOR_Z = {"dir_pins": [20],
           "motor_pins": [21],
           }

MOTOR_X = {"dir_pins": [26, 12],
           "motor_pins": [19, 16]}

MICROSTEP_RES_PINS = (14, 15, 18)
RELAY_PIN = 6

ENDSTOP_PIN = 22

CW = 0
CCW = 1

global INITIALIZED


def rising_edge_callback():
    print('This is a edge event callback function!')
    print('This is run in a different thread to your main program')


def init_pins(pins, motor, direction):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins, GPIO.OUT)
    GPIO.output(motor["dir_pins"], direction)
    print("initialized pins: {}".format(pins))


def init_endstop_detect():
    GPIO.remove_event_detect(ENDSTOP_PIN)
    # GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENDSTOP_PIN, GPIO.IN)
    GPIO.add_event_detect(ENDSTOP_PIN, GPIO.RISING, bouncetime=800)
    print("Initialized endstop pin {}".format(ENDSTOP_PIN))


def high_low_switching(delay, delays, motor, high, low):
    delays.append(delay)
    GPIO.output(motor["motor_pins"], high)
    sleep(delay)
    GPIO.output(motor["motor_pins"], low)
    sleep(delay)
    return delays


def use_tanh(nm_steps, motor, sps, delays, high, low, direction):
    print("Using Tanh velocity with {} steps ".format(nm_steps))
    which_motor = len(motor["dir_pins"])
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    for x in range(1, nm_steps):
        if GPIO.event_detected(ENDSTOP_PIN) and which_motor < 2:
            direction = int(np.logical_not(direction))
            print("Switching direction from {} to {}".format(direction, direction))
            GPIO.output(motor["dir_pins"], direction)

        delay = (1 / sps) * 1 / (np.tanh(x * (1 / nm_steps)) + 0.2)
        delays.append(high_low_switching(delay, delays, motor, high, low))
    GPIO.output(RELAY_PIN, GPIO.LOW)
    return delays


def use_const(nm_steps, motor, sps, delays, high, low, direction):
    print("Using Constant velocity with {} steps".format(nm_steps))
    which_motor = len(motor["dir_pins"])
    GPIO.output(RELAY_PIN, GPIO.HIGH)

    for x in range(1, nm_steps):
        if GPIO.event_detected(ENDSTOP_PIN) and which_motor < 2:
            direction = int(np.logical_not(direction))
            print("Switching direction from {} to {}".format(direction, direction))
            GPIO.output(motor["dir_pins"], direction)

        delay = 1 / sps
        delays.append(high_low_switching(delay, delays, motor, high, low))
    GPIO.output(RELAY_PIN, GPIO.LOW)
    return delays


def use_ramp_down(motor, delay, delays, high, low):
    print("Ramping down with initial delay {} ".format(delay))
    for j in range(1, 5):
        delay = delay * j
        if delay > 0.02:
            delay = 0.02
        delays.append(high_low_switching(delay, delays, motor, high, low))
    return delays


def drive_motor(motor,
                motor_kennlinien,
                nm_steps,
                sps,
                direction):
    delays = []
    high = list(itertools.repeat(GPIO.HIGH, len(motor["motor_pins"])))
    low = list(itertools.repeat(GPIO.LOW, len(motor["motor_pins"])))

    if "const" in motor_kennlinien:
        delays = use_const(nm_steps, motor, sps, delays, high, low, direction)
    elif "tanh" in motor_kennlinien:
        delays = use_tanh(nm_steps, motor, sps, delays, high, low, direction)
    elif "ramp_down" in motor_kennlinien:
        delays = use_ramp_down(motor, delays[-1], delays, high, low)

    # print("Used {} values: {}".format(str(motor_kennlinien), delays))


def microstepping(microstepping_resolution,
                  motor,
                  nm_steps,
                  ):
    pi = pigpio.pi()

    res = {1: (0, 0, 0),
           2: (1, 0, 0),
           4: (0, 1, 0),
           8: (1, 1, 0),
           16: (0, 0, 1),
           32: (1, 0, 1)}

    pi.set_mode(motor["dir_pins"][0], pigpio.OUTPUT)
    pi.set_mode(motor["motor_pins"][0], pigpio.OUTPUT)
    for i in range(3):
        pi.write(MICROSTEP_RES_PINS[i], res[microstepping_resolution][i])

    # Set duty cycle and frequency
    pi.set_PWM_dutycycle(motor["motor_pins"][0], 128)  # PWM 1/2 On 1/2 Off
    pi.set_PWM_frequency(motor["motor_pins"][0], 500)  # 500 pulses per second

    pi.set_PWM_dutycycle(motor["motor_pins"], 0)  # PWM off
    pi.stop()


def test_motor(motor,
               direction,
               nm_steps,
               sps,
               initialize_pins=True,
               motor_kennlinien=None,
               microstepping_resolution=1):
    if motor_kennlinien is None:
        motor_kennlinien = ["const", "ramp_down"]

    if microstepping_resolution != 1:
        microstepping(microstepping_resolution, motor, nm_steps)

    pins = list(itertools.chain.from_iterable([motor[key] for key in motor.keys()])) + [RELAY_PIN]
    if initialize_pins:
        init_pins(pins,
                  motor,
                  direction)

        if len(motor["dir_pins"]) < 2:
            init_endstop_detect()
    drive_motor(motor, motor_kennlinien, nm_steps, sps, direction)


test_motor(motor=MOTOR_Z,
           direction=CCW,
           nm_steps=1000,
           sps=350,
           initialize_pins=True,
           motor_kennlinien=["const"],
           microstepping_resolution=1)

GPIO.cleanup()
sleep(2)
test_motor(motor=MOTOR_X,
           direction=CW,
           nm_steps=50,
           sps=700,
           initialize_pins=True,
           motor_kennlinien=None,
           microstepping_resolution=1)

GPIO.cleanup()
sleep(0.4)
test_motor(motor=MOTOR_X,
           direction=CCW,
           nm_steps=50,
           sps=200,
           initialize_pins=True,
           motor_kennlinien=None,
           microstepping_resolution=1)
GPIO.cleanup()
