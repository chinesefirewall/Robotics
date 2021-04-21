#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import sys
import cv2
import numpy as np
from functools import partial
from threading import Timer
import time
from scipy import stats
from sensor_fusion import Gaussian

class Visualisation:
    def __init__(self, show_velocities = False, show_kalman = False,
                 show_ultrasonic = True, show_encoders = True, show_camera = True,
                 show_moving_avg = False, show_complementary = False):
        self.app = QtGui.QApplication([])
        self.win_distance = pg.GraphicsWindow()
        self.start_time = time.time()

        # Initialize variables for velocity plotting, Kalman plotting,
        # the three sensors (ultrasonic, encoders, camera)
        # and two filters (moving average, complementary)
        self.show_velocities = show_velocities
        self.show_kalman = show_kalman
        self.show_ultrasonic = show_ultrasonic
        self.show_encoders = show_encoders
        self.show_camera = show_camera
        self.show_moving_avg = show_moving_avg
        self.show_complementary = show_complementary

        # Create a window for plotting distance and Kalman curves
        self.win_distance.setWindowTitle('Distance Plotter')
        if self.show_kalman:
            self.win_distance.resize(1024, 640)
        else:
            self.win_distance.resize(1024, 320)

        # Create a distance plot from Lab08
        distance_plot = self.win_distance.addPlot()
        distance_plot.setLabel('top', "Distance (mm)")
        distance_plot.setXRange(-10, 2000)
        distance_plot.hideAxis('left')
        distance_plot.hideAxis('top')
        distance_plot.setAspectLocked()
        distance_plot.addLegend(offset=(800, 20), labelTextColor=[0, 0, 0, 0], verSpacing=-10, labelTextSize='6pt', colCount=2)

        # Initialize curves for each sensor on the distance plot
        if self.show_ultrasonic:
            self.curve_us = distance_plot.plot([], [], pen=pg.mkPen(width=3, color='r'), brush=pg.mkBrush(radius=10, color='r'),
                                               symbol='o',
                                               symbolBrush='r', symbolSize=10, name='Ultrasonic')
        if self.show_encoders:
            self.curve_enc = distance_plot.plot([], [], pen=pg.mkPen(width=3, color='g'), symbol='o', symbolBrush='g',
                                                symbolSize=10,
                                                name='Encoders')
        if self.show_camera:
            self.curve_cam = distance_plot.plot([], [], pen=pg.mkPen(width=3, color='b'), symbol='o', symbolBrush='b',
                                                symbolSize=10,
                                                name='Camera')
        if self.show_moving_avg:
            self.curve_ma_us = distance_plot.plot([], [], pen=pg.mkPen(width=3, color=1), symbol='o', symbolBrush=1,
                                               symbolSize=10,
                                               name='US Moving Average')
        if self.show_complementary:
            self.curve_compl = distance_plot.plot([], [], pen=pg.mkPen(width=3, color=2), symbol='o', symbolBrush=2,
                                                  symbolSize=10,
                                                  name='Complementary')
        if self.show_kalman:
            self.curve_kalman = distance_plot.plot([], [], pen=pg.mkPen(width=3, color='w'), symbol='o', symbolBrush='w',
                                                   symbolSize=10,
                                                   name='Kalman')

        # Load a background image of a track
        img_arr = np.asarray(cv2.cvtColor(cv2.imread('map.png'), cv2.COLOR_BGR2RGB))
        img_item = pg.ImageItem(np.rot90(img_arr, -1))
        img_item.scale(1.37, 1.37)
        img_item.setZValue(-100)
        distance_plot.addItem(img_item)

        # Create a plot for visualizing velocities according to different sensors
        if self.show_velocities:
            # Create the plot background
            self.win_velocity = pg.GraphicsWindow()
            self.win_velocity.setWindowTitle('Velocity Plotter')
            self.win_velocity.resize(640, 320)
            velocity_plot = self.win_velocity.addPlot()
            velocity_plot.setLabel('left', "Velocity (mm/s)")
            velocity_plot.setLabel('bottom', "Time (s)")
            velocity_plot.addLegend()
            velocity_plot.setYRange(-200, 200)
            self.velocity_plot = velocity_plot

            # Initialize velocity curves for each sensor
            VEL_INIT_X = list(reversed([ -x*0.1 for x in range(100) ]))
            VEL_INIT_Y = [0]*100
            if self.show_ultrasonic:
                self.curve_us_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='r'), name='Ultrasonic')
            if self.show_encoders:
                self.curve_enc_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='g'), name='Encoders')
            if self.show_camera:
                self.curve_cam_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='b'), name='Camera')
            if self.show_moving_avg:
                self.curve_ma_us_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color=1), name='US Moving Average')
            if self.show_complementary:
                self.curve_compl_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color=2), name='Complementary')
            if self.show_kalman:
                self.curve_kalman_vel = velocity_plot.plot(VEL_INIT_X[:], VEL_INIT_Y[:], pen=pg.mkPen(width=1, color='w'), name='Kalman')

        # Create a plot for visualizing Kalman filter behaviour
        if self.show_kalman:
            # Create the plot background
            self.win_distance.nextRow()
            kalman_plot = self.win_distance.addPlot()
            kalman_plot.setXRange(-10, 2000)
            kalman_plot.setYRange(0, 0.02)
            kalman_plot.hideAxis('left')
            kalman_plot.addLegend()

            # Initialize all Gaussian curves
            gaussian_names_and_colours = [("Camera", 'b'), ("Encoders", 'g'), ("Filtered result", 'w')]
            self.gaussian_curves = {}
            for name, color in gaussian_names_and_colours:
                self.gaussian_curves[name] = kalman_plot.plot([], [], pen=pg.mkPen(width=1, color=color), name=name)

    def draw(self, current_us, current_enc, current_cam, current_moving_avg_us, current_complementary, current_kalman,
                   us_velocity, enc_velocity, cam_velocity, moving_avg_us_velocity, complementary_velocity, kalman_velocity,
                   cam_gaussian = Gaussian(0, 1e309), enc_gaussian = Gaussian(0, 1e309), kalman_result_gaussian = Gaussian(0, 1e309)):
        # Update the graphs only when the values are valid
        # Update velocity graphs only when displaying velocities is turned on
        # Update Gaussians only when visualizing Kalman filter is turned on
        if current_us >= 0 and self.show_ultrasonic:
            self._draw_us(current_us)
            if self.show_velocities:
                self._draw_us_velocity(us_velocity)

        if current_enc >= 0 and self.show_encoders:
            self._draw_enc(current_enc)
            if self.show_velocities:
                self._draw_enc_velocity(enc_velocity)

        if current_cam >= 0 and self.show_camera:
            self._draw_cam(current_cam)
            if self.show_velocities:
                self._draw_cam_velocity(cam_velocity)

        if current_moving_avg_us >= 0 and self.show_moving_avg:
            self._draw_moving_avg_us(current_moving_avg_us)
            if self.show_velocities:
                self._draw_moving_avg_us_velocity(moving_avg_us_velocity)

        if current_complementary >= 0 and self.show_complementary:
            self._draw_compl(current_complementary)
            if self.show_velocities:
                self._draw_compl_velocity(complementary_velocity)

        if self.show_kalman:
            if current_kalman >= 0:
                self._draw_kalman(current_kalman)

            self._draw_kalman_velocity(kalman_velocity)

            self._plot_gaussian(cam_gaussian, "Camera")
            self._plot_gaussian(enc_gaussian, "Encoders")
            self._plot_gaussian(kalman_result_gaussian, "Filtered result")

    # Draws a position from the ultrasonic sensor to the map.
    def _draw_us(self, pos):
        x, y = self.curve_us.getData()
        x = np.append(x, pos)
        y = np.append(y, 240)
        self.curve_us.setData(x, y)

    # Draws a position from encoders to the map.
    def _draw_enc(self, pos):
        x, y = self.curve_enc.getData()
        x = np.append(x, pos)
        y = np.append(y, 210)
        self.curve_enc.setData(x, y)

    # Draws a position from a camera to the map.
    def _draw_cam(self, pos):
        x, y = self.curve_cam.getData()
        x = np.append(x, pos)
        y = np.append(y, 180)
        self.curve_cam.setData(x, y)

    # Draws a moving average of the ultrasonic sensor position to the map.
    def _draw_moving_avg_us(self, pos):
        x, y = self.curve_ma_us.getData()
        x = np.append(x, pos)
        y = np.append(y, 150)
        self.curve_ma_us.setData(x, y)

    # Draws a complementary filtered result to the map.
    def _draw_compl(self, pos):
        x, y = self.curve_compl.getData()
        x = np.append(x, pos)
        y = np.append(y, 120)
        self.curve_compl.setData(x, y)

    # Draws a position from Kalman filter to the map.
    def _draw_kalman(self, pos):
        x, y = self.curve_kalman.getData()
        x = np.append(x, pos)
        y = np.append(y, 90)
        self.curve_kalman.setData(x, y)

    # Draws the velocity of the robot calculated from US measurements to the plot.
    def _draw_us_velocity(self, velocity):
        x, y = self.curve_us_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_us_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from encoder measurements to the plot.
    def _draw_enc_velocity(self, velocity):
        x, y = self.curve_enc_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_enc_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from camera measurements to the plot.
    def _draw_cam_velocity(self, velocity):
        x, y = self.curve_cam_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_cam_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from US moving average measurements to the plot.
    def _draw_moving_avg_us_velocity(self, velocity):
        x, y = self.curve_ma_us_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_ma_us_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from complementary filtered results to the plot.
    def _draw_compl_velocity(self, velocity):
        x, y = self.curve_compl_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_compl_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Draws the velocity of the robot calculated from camera measurements to the plot.
    def _draw_kalman_velocity(self, velocity):
        x, y = self.curve_kalman_vel.getData()
        newest_time = time.time() - self.start_time
        x = np.append(x, newest_time)
        y = np.append(y, velocity)
        self.curve_kalman_vel.setData(x, y)
        self.velocity_plot.setXRange(newest_time-10, newest_time)

    # Plots Gaussian with given mu, sigma and name
    def _plot_gaussian(self, gaussian, name):
        if gaussian:
            x = np.arange(-100,2000)
            y = stats.norm.pdf(x, gaussian.mu, gaussian.sigma)
            self.gaussian_curves[name].setData(x, y)

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            self.app.exec_()
        else:
            raise Exception("Visualisation application did not start!")

    def set_on_close_function(self, exit_func, func_params):
        self.app.aboutToQuit.connect(partial(exit_func, func_params))

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def initialize_visualisation(TASK, close_function):
    # Initializes the visualisation logic of plotting distances, velocities and Kalman filter
    if TASK == 1:
        visual = Visualisation(show_velocities = True)
    elif TASK == 2:
        visual = Visualisation(show_velocities = True, show_moving_avg = True, show_encoders = False, show_camera = False)
    elif TASK == 3:
        visual = Visualisation(show_velocities = True, show_complementary = True, show_camera = False)
    elif TASK == 4:
        visual = Visualisation(show_velocities = True, show_kalman = True, show_ultrasonic = False)
    elif TASK == "FILTERS":
        visual = Visualisation(show_velocities = True, show_moving_avg = True, show_complementary = True, show_kalman = True,
                               show_ultrasonic = False, show_encoders = False, show_camera = False)
    elif TASK == "ALL":
        visual = Visualisation(show_velocities = True, show_moving_avg = True, show_complementary = True, show_kalman = True)
    else:
        visual = Visualisation()

    visual.set_on_close_function(close_function, "Plotter window closed.")

    return visual
