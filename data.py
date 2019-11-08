from core import load_file,render_file,_get_b64
from pathlib import Path
from base64 import b64decode as decode

def printer(xsect):
    print(xsect.info())

def iterator(xsect):
    products = ["reflectivity","velocity","differential_reflectivity","differential_phase","spectrum_width","cross_correlation_ratio"]
    z = zip(*[xsect.iter_field(prod) for prod in products])
    d = z.__next__()
    print(d)
    print(len(d))

if __name__ == "__main__":
    fl = Path("./radars") / "KVBX20150819_095530_V06.gz-MjAxNSA4IDE5IDMgMwo="
    xsect = load_file(fl)
    print(decode(_get_b64(fl)).decode())
    #printer(xsect)
    iterator(xsect)