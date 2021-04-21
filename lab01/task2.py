
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
myRobot.set_speed(500)
# Go forward
move_forward_seconds(1)
# Block here for 1 second
time.sleep(0.6)
# Start turning right

myRobot.right()
# Keep turning right for 0.5 seconds

time.sleep(0.6)

######################
move_forward_seconds(1)
# Block here for 1 second
time.sleep(0.6)
# Start turning right
myRobot.right()
# Keep turning right for 0.5 seconds
time.sleep(0.6)
################
move_forward_seconds(1)
# Block here for 1 second
time.sleep(0.6)
# Start turning right
myRobot.right()
# Keep turning right for 0.5 seconds
time.sleep(0.6)


####################

move_forward_seconds(1)
# Block here for 1 second
time.sleep(0.6)
# Start turning right
myRobot.right()
# Keep turning right for 0.5 seconds
time.sleep(0.6)

# Stop the robot
myRobot.stop()

    
