#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# reference pins by GPIO numbers
GPIO.setmode(GPIO.BCM)
# disable warnings
GPIO.setwarnings(False)

# define row and column pin numbers
row_pins = [21, 20, 16, 19, 13, 6, 5]
col_pins = [2, 3, 4, 14, 15]

# set all the pins as outputs and set column pins high, row pins low
GPIO.setup(col_pins, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(row_pins, GPIO.OUT, initial=GPIO.HIGH)

# Sets the waiting time between rows. With larger wait times (0.1) you can see that rows are lit up at different times. With smaller times (0.01) the LEDs appear to be not blinking at all
wait_time = 0.05

def show_row(row_number, columns, delay):
    # Control a row of the dot matrix display
    GPIO.output(row_pins[row_number-1], GPIO.LOW)
    for i in range(len(columns)):
        GPIO.output(col_pins[columns[i]-1], GPIO.HIGH)
    time.sleep(delay)

    GPIO.output(row_pins[row_number-1], GPIO.HIGH)
    for i in range(len(columns)):
        GPIO.output(col_pins[columns[i]-1], GPIO.LOW)
         # Remove this line when implementing


d_time = 0.001
ranger = 1000
####################   3 dots task  ######################
for i in range(int(ranger)):
    show_row(6, [2, 3, 5], d_time)



####Displays image 50 times #########  Letter A ######################

for i in range(int(ranger)):

    # sets row number 1 low
    show_row(1, [2, 3, 4], d_time)
    show_row(2, [1, 5], d_time)
    show_row(3, [1, 5], d_time)
    show_row(4, [1, 2, 3, 4, 5], d_time)
    show_row(5, [1, 5], d_time)
    show_row(6, [1, 5], d_time)
    show_row(7, [1, 5], d_time)

# reset GPIO so u dont need to reset before switching the letters
##GPIO.cleanup()

#

# Displays image 50 times #########  Letter N ######################

for i in range(int(ranger)):

    # sets row number 1 low
    show_row(1, [1, 5], d_time)
    show_row(2, [1, 2, 5], d_time)
    show_row(3, [1, 3, 5], d_time)
    show_row(4, [1, 4, 5], d_time)
    show_row(5, [1, 5], d_time)
    show_row(6, [1, 5], d_time)
    show_row(7, [1, 5], d_time)

# reset GPIO
GPIO.cleanup()

