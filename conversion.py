import numpy as np

"""
Thank you to Gareth Rees at Stackoverflow for the solution here: https://codereview.stackexchange.com/a/195947
Thank you to lumberjack4 at Stackoverflow for the solution here: https://stackoverflow.com/a/3713058
"""

a = 6378137 #earth semimajor axis
rf = 298.257223563 # semi-major axis, reciprocal flattening

def RAEtoECEF(objLLA,objRAE):
    # Range Azimuth Elevation to Earth-Centered Earth Fixed
    # ty lumberjack4
    sez = RAEtoSEZ(objRAE)
    fin_ecr = SEZtoECEF(sez,objLLA)
    return fin_ecr


def RAEtoSEZ(radarObj):
    # Range Azimuth Elevation to South East Zenith
    radar_range = radarObj["range"]
    radar_azimuth = radarObj["azimuth"]
    radar_elevation = radarObj["elevation"]

    azimuth = np.deg2rad(radar_azimuth)
    elevation = np.deg2rad(radar_elevation)

    south = -radar_range * np.cos(radar_elevation) * np.cos(radar_azimuth)
    east = radar_range * np.cos(radar_elevation) * np.sin(radar_azimuth)
    zenith = radar_range * np.sin(radar_elevation)

    return {"south": south, "east": east, "zenith": zenith}

def SEZtoECEF(sezObj,siteObj):
    # South East Zenith to Earth Centered, Earth Fixed
    site_x,site_y,site_z = geodetic_to_geocentric(siteObj)

    south = sezObj["south"]
    east = sezObj["east"]
    zenith = sezObj["zenith"]

    sinLat = np.sin(np.deg2rad(siteObj["lat"]))
    sinLon = np.sin(np.deg2rad(siteObj["lon"]))
    cosLat = np.cos(np.deg2rad(siteObj["lat"]))
    cosLon = np.cos(np.deg2rad(siteObj["lon"]))

    x = ( sinLat * cosLon * south) + (-sinLon * east) + (cosLat * cosLon * zenith) + site_x
    y = ( sinLat * sinLon * south) + ( cosLon * east) + (cosLat * sinLon * zenith) + site_y
    z = (-cosLat *        south) + ( sinLat * zenith) + site_z

    return x,y,z

def geodetic_to_geocentric(siteObj):
    """Return geocentric (Cartesian) Coordinates x, y, z corresponding to
    the geodetic coordinates given by latitude and longitude (in
    degrees) and height above ellipsoid. The ellipsoid must be
    specified by a pair (semi-major axis, reciprocal flattening).
    ty Gareth Rees
    """
    latitude = siteObj["lat"]
    longitude = siteObj["lon"]
    height = siteObj["alt"]
    φ = np.radians(latitude)
    λ = np.radians(longitude)
    sin_φ = np.sin(φ)
    e2 = 1 - (1 - 1 / rf) ** 2  # eccentricity squared
    n = a / np.sqrt(1 - e2 * sin_φ ** 2) # prime vertical radius
    r = (n + height) * np.cos(φ)   # perpendicular distance from z axis
    x = r * np.cos(λ)
    y = r * np.sin(λ)
    z = (n * (1 - e2) + height) * sin_φ
    return x, y, z

def conv_from_cart(x,y,z):

    # converting FROM cartesian is correct, no changes needed.
    f = 1/rf # WGS84 Flatteing
    b = a*(1-f) # Semiminor axis
    #print(f"semiminor axis: {b}, x: {x}, y: {y}, semimajor: {a}")
    z = np.sqrt(b**2*(1-((x**2+y**2)/a**2))) # Solving for the positive z value on the ellipsoid
    p = np.sqrt(x**2+y**2) # Distance from the z-axis
    #print(f"z solving for positive z value: {z}, p distance from z-axis: {p}, flattening: {f}")
    Lat = np.arctan(z/(p*(1-f)**2))*180/np.pi # Solving the latitude value
    Long = np.arctan2(y,x)*180/np.pi
    return {"lat": Lat, "lon": Long}


def radar_to_latlon(raz,rel,rrng,slat,slon,sel):
    radarObj = {"azimuth": raz, "elevation": rel, "range": rrng}
    siteObj = {"lat": slat, "lon": slon, "alt": sel}
    x,y,z = RAEtoECEF(siteObj,radarObj)
    return conv_from_cart(x,y,z)


if __name__ == "__main__":
    WGS84 = 6378137, 298.257223563
    radarObj = {"azimuth": 139.25994873046875, "elevation": 0.3790283203125, "range": 2000}
    siteObj = {"lat": 34.838314, "lon": -120.397780, "alt": 376 }
    print("truth","(-2651949.38180034, -4520539.58365707, 3623373.83213543)")
    print(radarObj)
    print(siteObj)
    x,y,z = RAEtoECEF(siteObj,radarObj)
    print("range azimuth elevation to ecef -- latlon")
    print(conv_from_cart(x,y,z))
    print("truth to geo")
    x2,y2,z2 = (-2651949.38180034, -4520539.58365707, 3623373.83213543)
    print(conv_from_cart(x2,y2,z2))
    print("geodetic to geocentric")
    x3,y3,z3 = geodetic_to_geocentric(siteObj)
    print(f"({x3},{y3},{z3})")
    print(conv_from_cart(x3,y3,z3))

