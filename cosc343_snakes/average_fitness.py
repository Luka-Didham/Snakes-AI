import matplotlib.pyplot as plot
import numpy as np

x = []
y = []
count = 0
for line in open('avg_fitness.txt', 'r'):
    count += 1
    y.append(float(line))
    x.append(count)

plot.title("Fitness per Training Game (Random, nPercepts=9 3x3)")
plot.xlabel('Training Game')
plot.ylabel("Average Fitness")

#Individual points
plot.plot(x, y, marker='o', c='b')
x_value = [x[0], x[len(x)-1]]
y_value = [y[0], y[len(y)-1]]
#plot.plot(x_value, y_value, linestyle="--", c='r')



plot.show()
