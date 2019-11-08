from core import load_file,render_file
from pathlib import Path

def printer(xsect):
    print(xsect.info())

def iterator(xsect):
    print(xsect.iter_field("spectrum_width").__next__())
    print(xsect.iter_field("spectrum_width"))

if __name__ == "__main__":
    fl = Path("./radars") / "KVBX20150819_095530_V06.gz-MjAxNSA4IDE5IDMgMwo="
    xsect = load_file(fl)
    #printer(xsect)
    iterator(xsect)