"""
This file contains classes that are used by localization_gui.py and localization_logic.py.
You can change the code at your own risk!
"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import sys
import cv2
import numpy as np
from functools import partial
from threading import Timer

class Visualisation:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()

        # Create a window for plotting
        self.win.setWindowTitle('Plotter')
        self.win.resize(1024, 320)
        plot = self.win.addPlot()
        plot.setLabel('top', "Distance (mm)")
        plot.setXRange(0, 2000)
        plot.hideAxis('left')
        plot.hideAxis('top')
        plot.setAspectLocked()
        plot.addLegend(offset=(800, 20), labelTextColor=[0, 0, 0, 0], verSpacing=-10, labelTextSize='6pt')

        # Initialize curves for each sensor
        self.curve_us = plot.plot([], [], pen=pg.mkPen(width=3, color='r'), brush=pg.mkBrush(radius=10, color='r'),
                                  symbol='o',
                                  symbolBrush='r', symbolSize=10, name='Ultrasonic')
        self.curve_enc = plot.plot([], [], pen=pg.mkPen(width=3, color='g'), symbol='o', symbolBrush='g',
                                   symbolSize=10,
                                   name='Encoders')
        self.curve_cam = plot.plot([], [], pen=pg.mkPen(width=3, color='b'), symbol='o', symbolBrush='b',
                                   symbolSize=10,
                                   name='Camera')

        # Load a background image of a track
        img_arr = np.asarray(cv2.cvtColor(cv2.imread('map.png'), cv2.COLOR_BGR2RGB))
        img_item = pg.ImageItem(np.rot90(img_arr, -1))
        img_item.scale(1.37, 1.37)
        img_item.setZValue(-100)
        plot.addItem(img_item)

    def draw(self, current_us, current_enc, current_cam):
        # Update the graphs only when the values are valid
        if current_us >= 0:
            self._draw_us(current_us)

        if current_enc >= 0:
            self._draw_enc(current_enc)

        if current_cam >= 0:
            self._draw_cam(current_cam)

    # Draws a position from the ultrasonic sensor to the map
    def _draw_us(self, pos):
        x, y = self.curve_us.getData()
        x = np.append(x, pos)
        y = np.append(y, 150)
        self.curve_us.setData(x, y)

    # Draws a position from encoders to the map
    def _draw_enc(self, pos):
        x, y = self.curve_enc.getData()
        x = np.append(x, pos)
        y = np.append(y, 120)
        self.curve_enc.setData(x, y)

    # Draws a position from a camera to the map
    def _draw_cam(self, pos):
        x, y = self.curve_cam.getData()
        x = np.append(x, pos)
        y = np.append(y, 90)
        self.curve_cam.setData(x, y)

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
