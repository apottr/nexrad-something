import matplotlib.pyplot as plt
import math,sys
from pathlib import Path
from base64 import b64decode as decode
from core import render_file

directory = Path(__file__).resolve().parent

files = []

xlimit = [15,20]
ylimit = [0,10]

def decoder(b64):
    d = decode(b64).decode()
    e = d.strip().split(" ")
    return str("{}-{}-{}T{}:{}:00-0700".format(e[0],e[1],e[2],e[3],e[4]))

def render_figure(display,product,location,b64):
    sweep = 0
    fig = plt.figure()
    ax = fig.add_axes()
    title=(display.generate_title(product,sweep)+" "+decoder(b64))
    display.plot_rhi(product,sweep,ax=ax,title=title)
    display.set_limits(ylim=ylimit,xlim=xlimit,ax=ax)

    fig.savefig(location)
    plt.close(fig)

def render_frames(display,fname,b64):
    keys = list(display.fields.keys())
    for i in range(len(keys)):
        render_figure(display,keys[i],str(directory/"figures"/f"{fname.name}_{keys[i]}"))

def render_frame(display,fname,product,b64):
    nme = fname.name
    if product not in display.fields.keys():
        raise IndexError("key not in fields: \n got {} \n wanted {}".format(product,display.fields.keys()))
    render_figure(display,product,str(directory/"figures"/f"{nme[0]}_{product}"),b64)

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

def one_plot(display,product):
    fig = plt.figure()
    ax = fig.add_axes()
    display.plot(product,0,ax=ax)
    display.set_limits(ylim=ylimit,xlim=xlimit,ax=ax)
    plt.show()
    

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
        display,b64 = render_file(f)
        render_frame(display,f,product,b64)

def render_single(f,product):
    display = render_file(f)
    one_plot(display,product)

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
    return list((directory / "radars").glob("*_V06*"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        product = sys.argv[1]
        files = load_files()
    else:
        print("Please include product name as sys.argv[1] for proper function.")
        sys.exit(1)
    #objs = ["2019100","2019101","2019050","2019051"]
    #objs1 = ["2019050","2019051","2019100","2019101","201902"]
    #plot_same_product(objs,"differential_phase")
    #plot_same_product(objs1,"differential_phase")
    render_same_product(files,product)
    #render_single(files[0],product)
    #hydro_class(files[0])
    #plotted(objs,"differential_phase")
    #plot_all(objs)
    #display = render_file(getfile("2019102"))
    #render_frames(display,getfile("2019102"))
    #render_same_product(objs,"velocity")