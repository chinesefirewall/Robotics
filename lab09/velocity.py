#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

####################################################
# Task 1: Calculate velocity for different sensors #
####################################################
def calculate_velocity(position1, time1, position2, time2):
    # position1 is the position of the robot at time1
    # position2 is the position of the robot at time2
    # Fill in the function and return the correct value

    dist = position2 - position1
    time_covered = time2 - time1
    velocity = dist/time_covered
    print('velocity  ----->', velocity)
    return velocity


class Velocity:
    def __init__(self, initial_velocities):
        self.velocities = initial_velocities
        self.last_times = {}
        self.last_positions = {}

    def update_velocity_for_sensor(self, new_position, sensor):
        new_measurement_time = time.time()

        if sensor in self.last_times:
            sensor_velocity = calculate_velocity(self.last_positions[sensor], self.last_times[sensor],
                                                 new_position, new_measurement_time)
            self.velocities[sensor] = sensor_velocity

        self.last_times[sensor] = new_measurement_time
        self.last_positions[sensor] = new_position

        return
