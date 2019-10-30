import matplotlib.pyplot as plt
import pyart,math,sys
from pathlib import Path

directory = Path(__file__).resolve().parent

files = []

xlimit = [10,30]
ylimit = [0,9]

def render_file(fname):
    try:
        radar = pyart.io.read_nexrad_archive(fname)
    except Exception as e:
        print(e,fname)
    xsect = pyart.util.cross_section_ppi(radar, [274,275])
    display = pyart.graph.RadarDisplay(xsect)
    return display

def render_figure(display,product,location):
    fig = plt.figure()
    ax = fig.add_axes()
    display.plot(product,0,ax=ax)
    display.set_limits(ylim=ylimit,xlim=xlimit,ax=ax)
    fig.savefig(location)

def render_frames(display,fname):
    keys = list(display.fields.keys())
    for i in range(len(keys)):
        render_figure(display,keys[i],str(directory/"figures"/f"{fname.name}_{keys[i]}"))

def render_frame(display,fname,product):
    if product not in display.fields.keys():
        raise IndexError("key not in fields: \n got {} \n wanted {}".format(product,display.fields.keys()))
    render_figure(display,product,str(directory/"figures"/f"{fname.name}_{product}"))

"""def render_frame(display,fname,product):
    if product not in display.fields.keys():
        raise IndexError("key not in fields: \n got {} \n wanted {}".format(product,display.fields.keys()))
    date = fname.name.split("_")[0][4:]
    y,m,d = date[:4],date[4:6],date[6:]
    f = str(directory/"figures"/y/m/d/f"{fname.name}_{product}")
    render_figure(display,product,f)"""

def plotter(display,fig,gs,idx):
    keys = list(display.fields.keys())
    subs = []
    for i in range(len(keys)):
        subs.append(fig.add_subplot(gs[i,idx]))
    for i in range(len(keys)):
        display.plot(keys[i],0,ax=subs[i])
        display.set_limits(ylim=ylimit,xlim=xlimit,ax=subs[i])
        subs[i].set_title("")
        subs[i].set_xlabel("")
        subs[i].set_ylabel("")
        subs[i].set_ylabel("")


def plot_single(display,product,fig,gs,x,y):
    ax = fig.add_subplot(gs[x,y])
    display.plot(product,0,ax=ax)
    display.set_limits(ylim=ylimit,xlim=xlimit,ax=ax)

def plot_all(objs):
    fig = plt.figure()
    gs = fig.add_gridspec(6,len(objs))
    for i in range(len(objs)):
        display = render_file(objs[i])
        plotter(display,fig,gs,i)
    plt.show()

def plot_same_product(objs,product):
    fig = plt.figure()
    w = math.floor(len(objs)/2) if len(objs) % 2 == 0 else math.floor(len(objs)/3)
    #w = len(objs)
    h = math.floor(len(objs)/2)
    gs = fig.add_gridspec(w,h)
    print(w,gs)
    for y in range(h):
        for x in range(w):
            f = objs[x+y]
            display = render_file(f)
            print(f,x,y)
            plot_single(display,product,fig,gs,x,y) 
    plt.show()

def render_same_product(objs,product):
    for f in objs:
        display = render_file(f)
        render_frame(display,f,product)

def plotted(objs,product):
    fig = plt.figure()
    gs = fig.add_gridspec(2,2)
    x1 = render_file(getfile(objs[0]))
    x2 = render_file(getfile(objs[1]))
    x3 = render_file(getfile(objs[2]))
    x4 = render_file(getfile(objs[3]))
    plot_single(x1,product,fig,gs,0,0)
    plot_single(x2,product,fig,gs,0,1)
    plot_single(x3,product,fig,gs,1,0)
    plot_single(x4,product,fig,gs,1,1)
    plt.show()

def load_files():
    return list((directory / "radars").glob("*_V06"))

if __name__ == "__main__":
    files = load_files()
    #objs = ["2019100","2019101","2019050","2019051"]
    #objs1 = ["2019050","2019051","2019100","2019101","201902"]
    #plot_same_product(objs,"differential_phase")
    #plot_same_product(objs1,"differential_phase")
    render_same_product(files,sys.argv[1])
    #plotted(objs,"differential_phase")
    #plot_all(objs)
    #display = render_file(getfile("2019102"))
    #render_frames(display,getfile("2019102"))
    #render_same_product(objs,"velocity")