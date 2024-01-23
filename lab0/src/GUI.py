import math
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time

time_data = [range(1)]
height_data = [range(1)]

if __name__ == "__main__":
    ser = Serial('/dev/tty.usbmodem204F377739472', timeout=10)
    ser.write(b'\x02')
    ser.write(b'\x04')
    line = ser.readline().decode('utf-8').rstrip().split(",", 1)
    while line[0] != "END":
        try:
            float(line[0])
            float(line[1])
        except (ValueError, IndexError):
            print("exception")
        else:
            time_data.append(float(line[0]))
            height_data.append(float(line[1]))
        finally:
            line = ser.readline().decode('utf-8').rstrip().split(",", 1)

    pyplot.plot(time_data[1:], height_data[1:])
    #pyplot.xlabel(time_data[0])
    #pyplot.ylabel(height_data[0])
    pyplot.show()

"""! TO DO:
1. Modify homework 0 to take in serial data and end at 'End'
2. Incorporate GUI from example code
3. Add second curve to plot
4. Clean up github/file organization
5. Write README
"""
