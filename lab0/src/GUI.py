import math
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time

if __name__ == "__main__":
    ser = Serial('/dev/tty.usbmodem204F377739472', timeout=10)
    ser.write(b'\x02')
    ser.write(b'\x04')
    print(ser.readlines())

