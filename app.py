import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from metpy.io import Level2File

directory = Path(__file__).resolve().parent

'''
one item of the sweep array has:
    one azimuth/elevation index
    data items, in order of nearest to furthest
    gate info:
        |   |   |   |
        |   |   |   |
        |   |   |   |
        |   |   |
'''

def load_file(filename):
    f = Level2File(str(directory / filename))
    return f

def range(x, axis=0):
    return np.max(x, axis=axis) - np.min(x, axis=axis)

def processor(f):
    sweep = 0
    az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])
    el = np.array([ray[0].el_angle for ray in f.sweeps[sweep]])
    print(len(f.sweeps[sweep]))
    swoop = f.sweeps[sweep][0]
    swoop2 = f.sweeps[sweep][1]
    for swaep in f.sweeps[sweep]:
        #0-3 is constants and metadata
        #4 is actual datasets

        reflectivity = swaep[4][b"REF"]
        #print(reflectivity)
        ref = reflectivity[0]
        #reflectivity is a tuple: (more metadata, dataset)
        '''print(f"ref number of gates: {ref.num_gates}")
        print(f"ref first gate: {ref.first_gate}")
        print(f"ref gate width: {ref.gate_width}")'''
        #azimuth: horizontal angle
        #elevation: vertical angle
        azimuth = swaep[0].az_angle
        elevation = swaep[0].el_angle
        rng = 0
        #az_el(azimuth,elevation,rng)
        #line_plot_gates(reflectivity[1])
        #polar_plot_gates(reflectivity[1])
        d = (np.arange(ref.num_gates + 1) - 0.5) * ref.gate_width + ref.first_gate
        for item in d:
            az_el(azimuth,elevation,item)
        #line_plot_gates(reflectivity[1],d)
    (az,el)
    plt.show()

def az_el(az,el,rng):
    print(f"azimuth (horizontal): {az}, elevation (vertical): {el}, range (distance): {rng}km")


def plot_az_el(az,el):
    plt.plot(az)
    plt.plot(el)


def line_plot_gates(a,b=None):
    plt.plot(a)
    try:
        data = np.ma.array(b)
        data[np.isnan(data)] = np.ma.masked
        plt.plot(b)
    except:
        pass
    plt.show()

def polar_plot_gates(data):
    
    for rad,idx in zip(data,rads):
        plt.polar(rad,idx)
    plt.show()

if __name__ == "__main__":
    f = load_file("KVBX20191002_081520_V06")
    processor(f)