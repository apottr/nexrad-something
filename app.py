import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from metpy.io import Level2File

directory = Path(__file__).resolve().parent

'''
one item of the sweep array has:
    one azimuth/elevation index
    data items, in order of nearest to furthest
    gate: 
        v = list(0,number of gates) + 1
            gives us a value for each item in the data array
        g = v * width of one gate
            converts data values to km by width (width of one gate = some number of km)
        range = g + first gate
            adjusts range values to be correctly distanced (starting from the true beginning, ending at 460.0km)

        ((list(0,number of gates) + 1) - 0.5) * width of one gate + first gate
        
'''

def load_file(filename):
    f = Level2File(str(directory / filename))
    return f

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

def conv_to_ll(rlat,rlon,rel,az,el,rng):
    r1 = 3959 + rel
    theta = rlon
    phi = 90 - rlat

    r2 = rng
    theta2 = az
    phi2 = 90 - el

    x1 = r1*np.sin(phi)*np.cos(theta)
    y1 = r1*np.sin(phi)*np.sin(theta)
    z1 = r1*np.cos(phi)

    x2 = r2*np.sin(phi2)*np.cos(theta2)
    y2 = r2*np.sin(phi2)*np.sin(theta2)
    z2 = r2*np.cos(phi2)

    x = x1+x2
    y = y1+y2
    z = z1+z2

    lat = 90 - np.arctan(np.sqrt(pow(x,2)+pow(y,2))/pow(z,2))
    lon = np.arctan(y/x)

    return {"lat": lat, "lon": lon}

def az_el(az,el,rng):
    out = conv_to_ll(34.838314,-120.397780,376,az,el,rng)
    print(f"azimuth (horizontal): {az}, elevation (vertical): {el}, range (distance): {rng}km")
    print(f"{out['lat']},{out['lon']}")


def get_data(f,product,az,el,gate=0):
    data = None
    sweep = 0
    print(f"product: {product}; az: {az}; el: {el}")
    for i in range(len(f.sweeps)):
        if f.sweeps[i][0][0].el_angle == el:
            sweep = i
            break
    for ray in f.sweeps[sweep]:
        if ray[0].az_angle == az:
            data = ray
            break
    print(data[4].keys())
    out = data[4][product]
    outmeta = out[0]
    ranged = (np.arange(outmeta.num_gates + 1) - 0.5) * outmeta.gate_width + outmeta.first_gate
    az_el(az,el,ranged[-1])
    return out



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
    #processor(f)
    azimuth = 139.25994873046875
    elevation = 0.3790283203125
    test = get_data(f,b"REF",azimuth,elevation)
    test2 = get_data(f,b"PHI",azimuth,elevation)
    test3 = get_data(f,b"ZDR",azimuth,elevation)
    test4 = get_data(f,b"RHO",azimuth,elevation)
    print(test)
    print(test2)
    print(test3)
    print(test4)
