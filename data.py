from core import load_file,render_file,_get_b64
import numpy as np
import dataplot as dp
from pathlib import Path
from base64 import b64decode as decode
from collections import defaultdict
from operator import countOf

products = ["reflectivity","velocity","differential_reflectivity","differential_phase","spectrum_width","cross_correlation_ratio"]

def printer(xsect):
    print(xsect.fields.keys())

def processor(*args):
    x = defaultdict(tuple)
    for i in range(len(products)):
        x[products[i]] = args[i]
    return x


def iterator(xsect):
    iterator = lambda x: xsect.iter_field(x)
    z = map(processor,*[iterator(prod) for prod in products])
    prods = z.__next__()
    return prods
    

'''def test_iterators(xsect):
    product = "differential_phase"
    print("iter_azimuth().__next__()")
    print(xsect.iter_azimuth().__next__())
    print("iter_elevation().__next__()")
    print(xsect.iter_elevation().__next__())
    print("iter_end().__next__()")
    print(xsect.iter_end().__next__())
    print("iter_field('differential_phase').__next__()")
    print(xsect.iter_field(product).__next__())
    print("iter_slice().__next__()")
    print(xsect.iter_slice().__next__())
    print("iter_start().__next__()")
    print(xsect.iter_start().__next__())
    print("iter_start_end().__next__()")
    print(xsect.iter_start_end().__next__())'''

def main(filename):
    xsect = load_file(filename)
    products = list(xsect.fields.keys())
    x = iterator(xsect)
    dp.from_masked(x["reflectivity"])
    dp.from_masked(x["velocity"])
    #test_iterators(xsect)

if __name__ == "__main__":
    fl = Path("./radars") / "KVBX20150819_095530_V06.gz-MjAxNSA4IDE5IDMgMwo="
    print(decode(_get_b64(fl)).decode())
    main(fl)
