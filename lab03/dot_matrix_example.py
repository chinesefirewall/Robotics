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
    # YOUR CODE GOES HERE:
    pass     # Remove this line when implementing


# Displays image 50 times
for i in range(50):

    # sets column number 3 high
    GPIO.output(col_pins[2], GPIO.HIGH)
    # sets row number 4 low, this should light up the middle LED
    GPIO.output(row_pins[3], GPIO.LOW)

    # wait
    time.sleep(wait_time)

    # set the pins back to previous states
    GPIO.output(col_pins[2], GPIO.LOW)
    GPIO.output(row_pins[3], GPIO.HIGH)

    # sets columns number 2, 4 high
    GPIO.output(col_pins[1], GPIO.HIGH)
    GPIO.output(col_pins[3], GPIO.HIGH)

    # sets row number 5 low
    GPIO.output(row_pins[4], GPIO.LOW)

    # wait
    time.sleep(wait_time)

    # set the pins back to previous states
    GPIO.output(col_pins[1], GPIO.LOW)
    GPIO.output(col_pins[3], GPIO.LOW)
    GPIO.output(row_pins[4], GPIO.HIGH)

# reset GPIO
GPIO.cleanup()
