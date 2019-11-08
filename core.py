from pyart.io import read_nexrad_archive
from pyart.util import cross_section_ppi
from pyart.graph import RadarDisplay

def load_file(fname):
    try:
        radar = read_nexrad_archive(fname)
    except Exception as e:
        print(e,fname)
    xsect = cross_section_ppi(radar, [274])
    return xsect

def _get_b64(fname):
    return fname.name.split("-")[1]

def render_file(fname):
    b64 = _get_b64(fname)
    xsect = load_file(fname)
    display = RadarDisplay(xsect)
    return display,b64