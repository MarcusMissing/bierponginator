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

CW = 0
CCW = 1


def init_pins(pins, motor, direction):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins, GPIO.OUT)
    GPIO.output(motor["dir_pins"], direction)
    print("initialized pins: {}".format(pins))


def drive_motor(motor,
                ramp_func,
                nm_steps,
                sps):
    assert ramp_func in ["exp", "tanh", "const"], "ramp functions available:exp,tanh,const"
    delays = []
    if ramp_func == "exp":
        for x in range(1, nm_steps):
            delay = 1 / (sps * np.exp(1 / (nm_steps - x) - 1))
            delays.append(delay)
            GPIO.output(motor["motor_pins"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor["motor_pins"], GPIO.LOW)
            sleep(delay)

    if ramp_func == "tanh":
        for x in range(1, nm_steps):
            delay = (1 / sps) * 1 / (np.tanh(x * (1 / nm_steps)) + 0.2)
            delays.append(delay)
            GPIO.output(motor["motor_pins"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor["motor_pins"], GPIO.LOW)
            sleep(delay)
    if ramp_func == "const":
        for x in range(1, nm_steps):
            delay = 1 / sps
            GPIO.output(motor["motor_pins"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor["motor_pins"], GPIO.LOW)
            sleep(delay)

    for j in range(1, 12):
        delay *= j * 2
        delays.append(delay)
        GPIO.output(motor["motor_pins"], GPIO.HIGH)
        sleep(delay)
        GPIO.output(motor["motor_pins"], GPIO.LOW)
        sleep(delay)

    return delays


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
    print(microstepping_resolution)
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
               return_to_start=True,
               ramp_func="const",
               microstepping_resolution=1):

    print(motor,
          direction,
          nm_steps,
          sps,
          return_to_start,
          ramp_func,
          microstepping_resolution)

    if microstepping_resolution != 1:
        print("Using Microstepping")
        microstepping(microstepping_resolution, motor, nm_steps)

    pins = list(itertools.chain.from_iterable([motor[key] for key in motor.keys()]))
    init_pins(pins,
              motor,
              direction)

    delays = drive_motor(motor, ramp_func, nm_steps, sps)
    print("k")
    print("Used ramp values: {}".format(delays))

    if return_to_start:
        print('returning')
        sleep(0.2)
        test_motor(motor,
                   int(np.logical_not(direction)),
                   nm_steps,
                   sps,
                   return_to_start=False,
                   ramp_func="const",
                   microstepping_resolution=1)


test_motor(MOTOR_X,
           CW,
           50,
           300,
           return_to_start=True,
           ramp_func="const",
           microstepping_resolution=1)

GPIO.cleanup()
