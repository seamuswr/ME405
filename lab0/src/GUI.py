import math
import tkinter
from serial import Serial
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# This function define both plots (Theorectical and Experimental). We also used the readline() method as well as utilizing strip and split similar to the HW1.
def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    # Real test data will be read through the USB-serial
    # port and processed to make two lists like these
    time_data = []
    height_data = []
    ser = Serial('/dev/tty.usbmodem204F377739472', timeout=10)
    # Seamus's serial /dev/tty.usbmodem204F377739472
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
# Calculation of Voltage
    voltage_theory = [3.3*(1 - math.exp((-1)*t/330)) for t in time_data]

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(time_data, height_data, linestyle='dotted')
    plot_axes.plot(time_data, voltage_theory)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()

# This function is for the GUI program.
def tk_matplot(plot_function, xlabel, ylabel, title):
    
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

# main
if __name__ == "__main__":
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Step Response")


"""! TO DO:
1. Modify homework 0 to take in serial data and end at 'End'
2. Incorporate GUI from example code
3. Add second curve to plot
4. Clean up github/file organization
5. Write README
"""
