import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from metpy.io import Level2File
from conversion import radar_to_latlon
import csv,types
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


def az_el(az,el,rng):
    siteObj = {"lat": 34.838314, "lon": -120.397780, "alt": 376 }
    out = radar_to_latlon(az,el,rng*1000,siteObj["lat"],siteObj["lon"],siteObj["alt"])
    #print(f"azimuth (horizontal): {az}, elevation (vertical): {el}, range (distance): {rng}km")
    #print(f"{out['lat']},{out['lon']}")
    return out


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
    return out,ranged

def iter_azimuth(f,product,el,gate=0):
    data = None
    sweep = 0
    for i in range(len(f.sweeps)):
        if f.sweeps[i][0][0].el_angle == el:
            sweep = i
            break
    for ray in f.sweeps[sweep]:
        out = ray[4][product]
        outmeta = out[0]
        ranged = (np.arange(outmeta.num_gates + 1) - 0.5) * outmeta.gate_width + outmeta.first_gate
        yield ray[0].az_angle,ranged


def process_for_csv(az,el,rng):
    if isinstance(az,types.GeneratorType):
        for a in az:
                azimuth = a[0]
                ranged = a[1]
                for item in ranged:
                    yield az_el(azimuth,el,item)
    else:
        for item in rng:
            yield az_el(az,el,item)

def gen_csv(az,el,rng=None):
    with open("test.csv","w+") as f:
        writer = csv.DictWriter(f,fieldnames=["lat","lon"])
        writer.writeheader()
        for item in process_for_csv(az,el,rng):
            #print(item)
            writer.writerow(item)


if __name__ == "__main__":
    f = load_file("KVBX20191002_081520_V06")
    #processor(f)
    #azimuth = 139.25994873046875
    elevation = 0.3790283203125
    #test,ranged = get_data(f,b"REF",azimuth,elevation)
    alz = iter_azimuth(f,b"REF",elevation)
    """
    test2,ranged2 = get_data(f,b"PHI",azimuth,elevation)
    test3,ranged3 = get_data(f,b"ZDR",azimuth,elevation)
    test4,ranged4 = get_data(f,b"RHO",azimuth,elevation)
    print(test)
    print(test2)
    print(test3)
    print(test4)
    """
    #gen_csv(azimuth,elevation,ranged) for non-list azimuths
    gen_csv(alz,elevation) # for list azimuths
