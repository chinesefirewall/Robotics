
import easygopigo3 as go


def move_forward_seconds(t):
    myRobot.forward()
    time.sleep(t)
    myRobot.stop()

def move_backward_seconds(t):
    myRobot.backward()
    time.sleep(t)
    myRobot.stop()


# Import time
import time

#Create an instance of the robot with a constructor from the easygopigo3 module that was imported as "go".
myRobot = go.EasyGoPiGo3()

# Set speed for the GoPiGo robot in degrees per second
myRobot.set_speed(450)
# Go forward
#move_forward_seconds(2)
# Block here for 1 second
myRobot.blinker_on(0)
myRobot.blinker_on(1)


myRobot.drive_cm(60, blocking=True)
 

time.sleep(0.6)
# Start turning right

myRobot.blinker_off(0)
myRobot.blinker_off(1)

# Keep turning right for 0.5 seconds

myRobot.right()
#myRobot.turn_degrees(120, blocking=True)
myRobot.blinker_on(1)

time.sleep(1.109)
myRobot.blinker_off(1)


# Go forward
myRobot.drive_cm(40, blocking=True)
# Block here for 1 second
time.sleep(0.6)


myRobot.left()
myRobot.blinker_on(0)
# Keep turning right for 0.5 seconds
time.sleep(0.2)

myRobot.orbit(-150, radius_cm=20, blocking=True)

time.sleep(0.2)
myRobot.blinker_off(0)

# Stop the robot
myRobot.stop()

    