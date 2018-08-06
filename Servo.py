import RPi.GPIO as GPIO
import pigpio as gpio
import os

class Servo_Type:
    def __init__(self, frequency, zero, maxleft, maxright):
        self.frequency = frequency
        self.zero = zero
        self.maxccw = maxleft
        self.maxcw = maxright

PARALLAX_CONTINUOUS = Servo_Type(50, 150, 170, 130)

class Servo:
    def __init__(self, servo_type = PARALLAX_CONTINUOUS):
        self.frequency = servo_type.frequency #this should be in Hertz
        self.zero = servo_type.zero #Pulse width in ms for center
        self.maxcw = servo_type.maxcw #Pulse width in ms
        self.maxccw = servo_type.maxccw #Pulse width in ms
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        self.io = GPIO.PWM(12, self.frequency)
        self.direction = "none"
        self.speed = 0 #this value should be 0 to 100
        self.pigpio = False
	self.armed = False
        
        
    def __init__(self, servo_type = PARALLAX_CONTINUOUS, usepigpio = True):
        if os.system("top -b -n 1 | grep pigpiod"):
            os.system("sudo pigpiod")
        self.frequency = servo_type.frequency #this should be in Hertz
        self.zero = servo_type.zero #Pulse width in ms for center
        self.maxcw = servo_type.maxcw #Pulse width in ms
        self.maxccw = servo_type.maxccw #Pulse width in ms
        self.io = gpio.pi()
        self.direction = "none"
        self.speed = 0 #this value should be 0 to 100
        self.pigpio = True
	sefl.armed = False
        
        
    def set_direction_clockwise(self):
        self.direction = "cw"
	self.go()
    def right(self):
        self.set_direction_clockwise()
    def cw(self):
        self.set_direction_clockwise()
        
    def set_direction_counterclockwise(self):
        self.direction = "ccw"
	self.go()
    def left(self):
        self.set_direction_counterclockwise()
    def ccw(self):
        self.set_direction_counterclockwise()
        
    def set_speed(self, speed):
	if speed > 100:
	    speed = 100
	if speed < 0:
	    speed = 0
        self.speed = speed
        
    def go(self):
        self.__set_dc__()
        if self.pigpio and self.armed:
            self.io.hardware_PWM(18, self.frequency, self.dc)
        else:
            self.io.start(self.dc)
        
    def stop(self):
        self.io.stop()
    
    def __set_dc__(self):
        dir = self.zero
        if self.direction == "cw":
            dir = self.maxcw
        elif self.direction == "ccw":
            dir = self.maxccw
        
        period = 1000/self.frequency
        gpiointerfacemultiplier = 1
        if self.pigpio:
            gpiointerfacemultiplier = 10000
        self.dc = ((((self.speed/100)*(dir - self.zero))+self.zero) / period) * gpiointerfacemultiplier
