import matplotlib.pyplot as plt
import numpy as np

plt.ion()
for i in range(3):
    y = np.random.random([10,1])
    print(y)
    plt.plot(y)
    plt.draw()
    plt.pause(1)
    plt.clf()