import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup([i for i in range(20)], GPIO.LOW)
GPIO.cleanup()
