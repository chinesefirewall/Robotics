#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import json
import signal
import sys
import time


def initialize_serial(com_port, baudrate=115200):
    """
    This function creates serial object and checks if the data is sent by request
    """
    try:
        ser = serial.Serial(com_port, baudrate=baudrate, timeout=2)
        return True, ser

    except (serial.SerialException or ValueError) as e:
        print("Failed to establish a serial connection: " + str(e))
        return False, None


def get_data_from_arduino(ser):
    """
    Retrieve data from ultrasonic sensor and line following module connected to Arduino
    """
    data = {}
    try:
        # Request data
        ser.write("R".encode())

        # Wait for a response to reach us from Arduino for two seconds,
        # if a response arrives convert it to a dictionary
        data = json.loads(ser.readline().decode().strip())

    except json.JSONDecodeError as e:
        data = {}
        print("Problem with decoding JSON data: " + str(e))

    except serial.serialutil.SerialException as e:
        print("Problem with writing to or reading from serial" + str(e))
        data = {}

    except OSError as e:
        data = {}
        print("Unexpected error:", str(e))

    finally:
        return data


def close(message=""):
    """
    read_sensors specific cleanup function
    """
    global running, ser
    running = False
    if ser.is_open:
        ser.close()
    print(message)
    sys.exit(0)


def signal_handler(sig, frame):
    """
    This function will be called when CTRL+C is pressed
    """
    close('\nYou pressed Ctrl+C! Closing the program nicely :)')


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    running, ser = initialize_serial('/dev/ttyUSB0')
    arduino_data = get_data_from_arduino(ser)

    while running:

        arduino_data = get_data_from_arduino(ser)

        if arduino_data:
            # Extract the sensor values
            ls1 = arduino_data['ls1']
            ls2 = arduino_data['ls2']
            ls3 = arduino_data['ls3']
            ls4 = arduino_data['ls4']
            ls5 = arduino_data['ls5']
            us = arduino_data['us']

            # Print received to the console
            print("LS1: ", ls1, "LS2: ", ls2, "LS3: ", ls3, "LS4: ", ls4, "LS5: ", ls5, "US: ", us)

        if not ser.is_open:
            close("Serial is closed!")

        # Throttle the loop to about 10 times per second
        time.sleep(.1)
