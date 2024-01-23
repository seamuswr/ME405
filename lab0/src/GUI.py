import math
import tkinter
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time

time_data = []
height_data = []


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Make an example plot to show a simple(ish) way to embed a plot into a GUI.
    The data is just a nonsense simulation of a diving board from which a
    typically energetic otter has just jumped.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """
    # Here we create some fake data. It is put into an X-axis list (times) and
    # a Y-axis list (boing). Real test data will be read through the USB-serial
    # port and processed to make two lists like these
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

    voltage_theory = [3.3*(1 - math.exp((-1)*t/330)) for t in time_data]

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(time_data, height_data)
    plot_axes.plot(time_data, voltage_theory)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot.
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


if __name__ == "__main__":
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Step Response")

    #pyplot.plot(time_data[1:], height_data[1:])
    #pyplot.xlabel(time_data[0])
    #pyplot.ylabel(height_data[0])
    #pyplot.show()

"""! TO DO:
1. Modify homework 0 to take in serial data and end at 'End'
2. Incorporate GUI from example code
3. Add second curve to plot
4. Clean up github/file organization
5. Write README
"""
