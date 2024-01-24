from matplotlib import pyplot

time = [range(1)]
height = [range(1)]

with open("data.csv", 'r') as file:
    time[0], height[0] = file.readline().rstrip().split(", ", 1)
    for line in file:
        new_data = line.rstrip().split(",", 1)
        try:
            float(new_data[0])
            float(new_data[1])
        except (ValueError, IndexError):
            print("exception")
        else:
            time.append(float(new_data[0]))
            height.append(float(new_data[1]))

pyplot.plot(time[1:], height[1:])
pyplot.xlabel(time[0])
pyplot.ylabel(height[0])
pyplot.show()