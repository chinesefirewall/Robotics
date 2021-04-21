# Niyi Solomon Adebayo
# -*- coding: utf-8 -*-
import numpy as np
from velocity import Velocity

####################################
# Lab09: code to continuously edit #
####################################
TASK = 3 # Update this value in the beginning of each task!


# Pre-defined dictionaries
# Dictionary for holding positions
positions = {'current_marker': -1, 'current_us': -1, 'current_enc': -1, 'current_cam': -1,
             'current_moving_avg_us': -1, 'current_complementary': -1, 'current_kalman': -1}

# A Velocity class object for holding and updating velocities
velocities = Velocity({'us': 0, 'enc': 0, 'cam': 0,
                       'moving_avg_us': 0, 'complementary': 0, 'kalman': 0})


############################################
# Task 2: Implement moving average filter  #
############################################
my_list =[]
def moving_average(pos):
    global my_list
    # Fill in the function.
    limit = 10
    my_list.append(pos)
#     i = 0
    print('my_list ----------------> ', my_list)
    if len(my_list) > limit:
            
    #    my_list[limit:-1]
        values = my_list[-limit:]  # returns 5 last elements
        moving_average = sum(values)/int(limit)
#             i += 1
#         print('my_list ----------------> ', my_list)
    else:
        values = my_list
        print('MOVING AVERAGE  ELSEE VALUE:  ', np.mean(values))
        moving_average = sum(values) / int(limit)
        
    print(' moving_average----->', moving_average)
    return moving_average

############################################
# Task 3: Implement complementary filter   #
############################################

encoder_value_dict = {}
complemetary_est_value_dict = {}

def complementary(us_pos, enc_pos):
    
    '''
posN=α⋅usN+β⋅(posN−1+Δenc).

'''
    global complemetary_est_value_dict, encoder_value_dict
    # Fill in the function
    enc_position = 'value'
    complemetary_est_value = 'value'
    usN = us_pos
    
    if 'enc_position' in encoder_value_dict: # first time it check if in dict...else it appends
        delta_encoders = encoder_value_dict['enc_position'] - enc_pos ## takes diff between current value and past value
    else:
        delta_encoders = 0
        
    encoder_value_dict['enc_position'] = enc_pos
    
    
    if 'complemetary_est_value' in complemetary_est_value_dict:
        posN_minus_1 = complemetary_est_value_dict['complemetary_est_value']
    else:
        posN_minus_1 = 1800 # 1800mm
        
    posN = (0.05 * usN) + 0.95 * (posN_minus_1 + delta_encoders)  ## weighted average
    complemetary_est_value_dict['complemetary_est_value'] = posN
   
    return posN
'''if one of the sensor is returning a constant value for e.g the ultrasonic sensor is return a constant value...
for example when it is blocked i.e "(posN_minus_1 + delta_encoders) = a constant value".
then, we will have a situation where the weigted average does not work as espected bcoz the weights are supposed to be shared
according the formular, so it negate the prupose for complementary filter and it will
hence add only the weights will be to the estimate of param1 '(0.05 * usN)'
...then "posN" starts accumulating errors we're trying to solve by implementing complemetary filter
'''
# A class for performing operations with Gaussians
class Gaussian:
    def __init__(self, mu, sigma):
        # Initializes a Gaussian with given mu and sigma values
        self.mu = mu
        self.sigma = sigma

    #################################################
    # Task 4.2: Implement addition of two Gaussians #
    #################################################
    def __add__(self, other):
        # Fill in the function.
        return Gaussian(0, 0)

    #######################################################
    # Task 4.3: Implement multiplication of two Gaussians #
    #######################################################
    def __mul__(self, other):
        # Fill in the function
        return Gaussian(0, 0)


# A Kalman filter class
class Kalman:
    def __init__(self, initial_gaussian):
        # Initializes a Kalman filter with the initial state given as an input
        self.filtered_result = initial_gaussian

    ########################################
    # Task 4.2: Implement the predict step #
    ########################################
    def predict(self, measurement):
        # Fill in the function
        return

    #######################################
    # Task 4.3: Implement the update step #
    #######################################
    def update(self, measurement):
        # Fill in the function
        return


# Global variables for holding the encoder difference and camera Gaussians
# and the Kalman class object for use in other files
# DO NOT CHANGE THE NAMES OF THESE VARIABLES!
camera_gaussian = None
encoder_diff_gaussian = None
kalman_filter = Kalman(None)


####################################
# Lab09: code to continuously edit #
####################################
def on_ultrasonic_measurement(us_pos):
    # Write code here that will perform actions
    # whenever the robot calculates a new ultrasonic-based location estimate
    moving_average_variable_holder  = moving_average(us_pos) ###  ----------------------------<<<<<<<<<<<<  CODE ADDED BY NIYI
    velocities.update_velocity_for_sensor(moving_average_variable_holder, 'moving_avg_us')
    positions['current_moving_avg_us'] = moving_average_variable_holder

    # Update the velocity calculated based on ultrasonic measurements
    velocities.update_velocity_for_sensor(us_pos, 'us')

    return

def on_encoder_measurement(enc_pos):
    # Write code here that will perform actions
    # whenever the robot calculates a new encoders-based location estimate
    current_ultra_sonic_pos = positions['current_us']
    complementary_value = complementary(current_ultra_sonic_pos, enc_pos)
    velocities.update_velocity_for_sensor(complementary_value, 'complementary')
    
    positions[ 'current_complementary'] = complementary_value
    
    # Update the velocity calculated based on encoder measurements
    velocities.update_velocity_for_sensor(enc_pos, 'enc')

    return

def on_camera_measurement(cam_pos):
    # Write code here that will perform actions
    # whenever the robot calculates a new camera-based location estimate

    # Update the velocity calculated based on ultrasonic measurements
    velocities.update_velocity_for_sensor(cam_pos, 'cam')

    return
