import numpy as np
import matplotlib.pyplot as plt

def to_ndarray(data):
    return data.filled()

def plot(data):
    fig = plt.figure()
    ax = fig.add_axes()
    y_size = np.arange(data.shape[0]+1)
    x_size = np.arange(data[0,].shape[0])
    print(x_size,y_size)
    plt.pcolormesh(x_size,y_size,data,figure=fig)
    plt.show()


def from_masked(data):
    x = to_ndarray(data)
    plot(x)
    

