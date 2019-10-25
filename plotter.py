import matplotlib.pyplot as plt
import pyart
from pathlib import Path

directory = Path(__file__).resolve().parent

file1 = str(directory/"KVBX20191002_081520_V06")
file2 = str(directory/"KVBX20191002_082505_V06")


def render_file(fname):
    radar = pyart.io.read_nexrad_archive(fname)
    xsect = pyart.util.cross_section_ppi(radar, [273,278])
    display = pyart.graph.RadarDisplay(xsect)
    return display


def plotter(display,fig,gs,idx):
    keys = list(display.fields.keys())
    subs = []
    for i in range(len(keys)):
        subs.append(fig.add_subplot(gs[i,idx]))
    for i in range(len(keys)):
        display.plot(keys[i],0,ax=subs[i])
        display.set_limits(ylim=[0,9],xlim=[0,30],ax=subs[i])

if __name__ == "__main__":
    display1 = render_file(file1)
    display2 = render_file(file2)
    fig = plt.figure()
    gs = fig.add_gridspec(6,2)
    plotter(display1,fig,gs,0)
    plotter(display2,fig,gs,1)
    plt.show()