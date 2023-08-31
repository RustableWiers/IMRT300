# Example code for IMRT1000 robot project


# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 250
TURNING_SPEED = 100
STOP_DISTANCE = 35

def check_surrounding():
    speed = 150

    left = motor_serial.get_dist_1()
    right = motor_serial.get_dist_2()
    front = motor_serial.get_dist_3()
    rear = motor_serial.get_dist_4()
    
    drive_backwards(0.5)

    while front < 60:
        left = motor_serial.get_dist_1()
        right = motor_serial.get_dist_2()
        front = motor_serial.get_dist_3()
        rear = motor_serial.get_dist_4()

        motor_serial.send_command(speed, -speed)

        print("Left:", left, "   Right:", right, "   Front:", front, "   Rear:", rear)
        time.sleep(0.10)
    

def turn_left(duration):
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED, DRIVING_SPEED)
        time.sleep(0.10)

def turn_right(duration):
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(DRIVING_SPEED, TURNING_SPEED)
        time.sleep(0.10)

def turn_hard_right(duration):
    speed = left / 0.8
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(DRIVING_SPEED, -80)
        time.sleep(0.10)
def turn_hard_left(duration):
    speed = right / 0.8
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(0, DRIVING_SPEED)
        time.sleep(0.10)

def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)

def drive_backwards(duration):
    speed = DRIVING_SPEED / 2
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(-80, -120)
        if rear < 7:
            drive_robot(FORWARDS, 0.1)
        time.sleep(0.10)
def seier(duration):
    speed = random.randint(100, 400)
    speed2 = random.randint(100, 400)
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, -speed2)
        time.sleep(0.1)

    speed = random.randint(100, 400)
    speed2 = random.randint(100, 400)
    iterations2 = int(duration * 10)

    for i in range(iterations2):
        motor_serial.send_command(-speed, -speed)
        time.sleep(0.1)


execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds

motor_serial = imrt_robot_serial.IMRTRobotSerial()

try:
    motor_serial.connect("/dev/ttyUSB0")
except: 
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

motor_serial.run()

print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now:

    # Get and print readings from distance sensors
    left = motor_serial.get_dist_1()
    right = motor_serial.get_dist_2()
    front = motor_serial.get_dist_3()
    rear = motor_serial.get_dist_4()

    print("Left:", left, "   Right:", right, "   Front:", front, "   Rear:", rear)
    if left < 5 or front < 5:
        drive_backwards(0.1)
    elif left < 30 and front < 30 and right < 30:
        check_surrounding()
    elif left < 20 or front < 15:
        turn_hard_right(0.1)
    elif left > 20 and left < 25:
        turn_right(0.1)
    elif left > 25 and left < 50:
        drive_robot(FORWARDS, 0.1)
    elif left > 50 or right < 15:
        turn_left(0.1)
